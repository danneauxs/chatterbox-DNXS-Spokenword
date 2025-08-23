from dataclasses import dataclass
from pathlib import Path
import os
import logging

import librosa
import torch
import perth
import torch.nn.functional as F
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

from .models.t3 import T3
from .models.s3tokenizer import S3_SR, drop_invalid_tokens
from .models.s3gen import S3GEN_SR, S3Gen
from .models.tokenizers import EnTokenizer
from .models.voice_encoder import VoiceEncoder
from .models.t3.modules.cond_enc import T3Cond


REPO_ID = "ResembleAI/chatterbox"


def punc_norm(text: str) -> str:
    """
        Quick cleanup func for punctuation from LLMs or
        containing chars not seen often in the dataset
    """
    if len(text) == 0:
        return "You need to add some text for me to talk."

    # Capitalise first letter
    if text[0].islower():
        text = text[0].upper() + text[1:]

    # Remove multiple space chars
    text = " ".join(text.split())

    # Replace uncommon/llm punc
    punc_to_replace = [
        ("...", ", "),
        ("…", ", "),
        (":", ","),
        (" - ", ", "),
        (";", ", "),
        ("—", "-"),
        ("–", "-"),
        (" ,", ","),
        (""", '"'),
        (""", '"'),
        ("‘", "'"),
        ("’", "'"),
    ]
    for old_char_sequence, new_char in punc_to_replace:
        text = text.replace(old_char_sequence, new_char)

    # Add full stop if no ending punc
    text = text.rstrip(" ")
    sentence_enders = {".", "!", "?", "-", ","}
    
    # Check for punctuation at end, including inside quotes
    has_ending_punct = False
    if any(text.endswith(p) for p in sentence_enders):
        has_ending_punct = True
    elif len(text) >= 2 and text[-1] in ['"', "'"] and text[-2] in sentence_enders:
        # Check for punctuation before closing quote: ?" or .'
        has_ending_punct = True
    
    if not has_ending_punct:
        text += "."

    return text


@dataclass
class Conditionals:
    """
    Conditionals for T3 and S3Gen
    - T3 conditionals:
        - speaker_emb
        - clap_emb
        - cond_prompt_speech_tokens
        - cond_prompt_speech_emb
        - emotion_adv
    - S3Gen conditionals:
        - prompt_token
        - prompt_token_len
        - prompt_feat
        - prompt_feat_len
        - embedding
    """
    t3: T3Cond
    gen: dict

    def to(self, device):
        self.t3 = self.t3.to(device=device)
        for k, v in self.gen.items():
            if torch.is_tensor(v):
                self.gen[k] = v.to(device=device)
        return self

    def save(self, fpath: Path):
        arg_dict = dict(
            t3=self.t3.__dict__,
            gen=self.gen
        )
        torch.save(arg_dict, fpath)

    @classmethod
    def load(cls, fpath, map_location="cpu"):
        if isinstance(map_location, str):
            map_location = torch.device(map_location)
        kwargs = torch.load(fpath, map_location=map_location, weights_only=True)
        return cls(T3Cond(**kwargs['t3']), kwargs['gen'])


class ChatterboxTTS:
    ENC_COND_LEN = 6 * S3_SR
    DEC_COND_LEN = 10 * S3GEN_SR

    def __init__(
        self,
        t3: T3,
        s3gen: S3Gen,
        ve: VoiceEncoder,
        tokenizer: EnTokenizer,
        device: str,
        conds: Conditionals = None,
    ):
        self.sr = S3GEN_SR  # sample rate of synthesized audio
        self.t3 = t3
        self.s3gen = s3gen
        self.ve = ve
        self.tokenizer = tokenizer
        self.device = device
        self.conds = conds
        self.watermarker = perth.PerthImplicitWatermarker()

    @classmethod
    def from_local(cls, ckpt_dir, device) -> 'ChatterboxTTS':
        ckpt_dir = Path(ckpt_dir)

        # Always load to CPU first for non-CUDA devices to handle CUDA-saved models
        if device in ["cpu", "mps"]:
            map_location = torch.device('cpu')
        else:
            map_location = None

        ve = VoiceEncoder()
        ve.load_state_dict(
            load_file(ckpt_dir / "ve.safetensors")
        )
        ve.to(device).eval()

        t3 = T3()
        t3_state = load_file(ckpt_dir / "t3_cfg.safetensors")
        if "model" in t3_state.keys():
            t3_state = t3_state["model"][0]
        t3.load_state_dict(t3_state)
        t3.to(device).eval()

        s3gen = S3Gen()
        s3gen.load_state_dict(
            load_file(ckpt_dir / "s3gen.safetensors"), strict=False
        )
        s3gen.to(device).eval()

        tokenizer = EnTokenizer(
            str(ckpt_dir / "tokenizer.json")
        )

        conds = None
        if (builtin_voice := ckpt_dir / "conds.pt").exists():
            conds = Conditionals.load(builtin_voice, map_location=map_location).to(device)

        return cls(t3, s3gen, ve, tokenizer, device, conds=conds)

    @classmethod
    def from_pretrained(cls, device) -> 'ChatterboxTTS':
        # Check if MPS is available on macOS
        if device == "mps" and not torch.backends.mps.is_available():
            if not torch.backends.mps.is_built():
                print("MPS not available because the current PyTorch install was not built with MPS enabled.")
            else:
                print("MPS not available because the current MacOS version is not 12.3+ and/or you do not have an MPS-enabled device on this machine.")
            device = "cpu"

        for fpath in ["ve.safetensors", "t3_cfg.safetensors", "s3gen.safetensors", "tokenizer.json", "conds.pt"]:
            local_path = hf_hub_download(repo_id=REPO_ID, filename=fpath)

        return cls.from_local(Path(local_path).parent, device)

    def prepare_conditionals(self, wav_fpath, exaggeration=0.5):
        """Prepare voice conditionals with optional caching for performance optimization"""
        
        # Try to import voice caching functions (with fallback for compatibility)
        try:
            from modules.tts_engine import (
                get_voice_cache_key, 
                _voice_embedding_cache, 
                _cache_memory_usage,
                estimate_cache_memory_mb,
                get_available_memory,
                clear_voice_embedding_cache
            )
            from config.config import (
                ENABLE_VOICE_EMBEDDING_CACHE, 
                VOICE_CACHE_MEMORY_LIMIT_MB, 
                ENABLE_ADAPTIVE_VOICE_CACHE
            )
            caching_available = True
        except ImportError:
            caching_available = False
            logging.warning("Voice embedding caching not available - using standard processing")

        # Check cache if caching is enabled and available
        if caching_available and ENABLE_VOICE_EMBEDDING_CACHE:
            cache_key = get_voice_cache_key(wav_fpath, exaggeration)
            
            # Check if we have cached embeddings
            if cache_key in _voice_embedding_cache:
                try:
                    self.conds = _voice_embedding_cache[cache_key]
                    logging.info("🚀 Using cached voice embeddings - significant speedup!")
                    return
                except Exception as e:
                    logging.warning(f"⚠️ Cache retrieval failed: {e}, computing fresh embeddings")
                    
            # Check memory constraints before caching
            available_memory = get_available_memory()
            if ENABLE_ADAPTIVE_VOICE_CACHE and available_memory < 2048:  # Less than 2GB available
                logging.warning("🧠 Low memory detected - disabling voice embedding cache")
                caching_available = False

        # Original embedding computation (always runs for new voices or cache misses)
        logging.info("🎤 Computing voice embeddings (this may take a moment)")
        
        ## Load reference wav
        s3gen_ref_wav, _sr = librosa.load(wav_fpath, sr=S3GEN_SR)

        ref_16k_wav = librosa.resample(s3gen_ref_wav, orig_sr=S3GEN_SR, target_sr=S3_SR)

        s3gen_ref_wav = s3gen_ref_wav[:self.DEC_COND_LEN]
        s3gen_ref_dict = self.s3gen.embed_ref(s3gen_ref_wav, S3GEN_SR, device=self.device)

        # Speech cond prompt tokens
        if plen := self.t3.hp.speech_cond_prompt_len:
            s3_tokzr = self.s3gen.tokenizer
            t3_cond_prompt_tokens, _ = s3_tokzr.forward([ref_16k_wav[:self.ENC_COND_LEN]], max_len=plen)
            t3_cond_prompt_tokens = torch.atleast_2d(t3_cond_prompt_tokens).to(self.device)

        # Voice-encoder speaker embedding
        ve_embed = torch.from_numpy(self.ve.embeds_from_wavs([ref_16k_wav], sample_rate=S3_SR))
        ve_embed = ve_embed.mean(axis=0, keepdim=True).to(self.device)

        t3_cond = T3Cond(
            speaker_emb=ve_embed,
            cond_prompt_speech_tokens=t3_cond_prompt_tokens,
            emotion_adv=exaggeration * torch.ones(1, 1, 1),
        ).to(device=self.device)
        self.conds = Conditionals(t3_cond, s3gen_ref_dict)

        # Cache the computed embeddings if caching is enabled
        if caching_available and ENABLE_VOICE_EMBEDDING_CACHE:
            try:
                # Check memory usage before caching
                global _cache_memory_usage
                estimated_size = estimate_cache_memory_mb(self.conds)
                
                if _cache_memory_usage + estimated_size <= VOICE_CACHE_MEMORY_LIMIT_MB:
                    cache_key = get_voice_cache_key(wav_fpath, exaggeration)
                    _voice_embedding_cache[cache_key] = self.conds
                    _cache_memory_usage += estimated_size
                    logging.info(f"💾 Voice embeddings cached ({estimated_size}MB, total: {_cache_memory_usage}MB)")
                else:
                    logging.warning("⚠️ Cache memory limit reached - clearing old cache")
                    clear_voice_embedding_cache()
                    # Try caching again after clearing
                    cache_key = get_voice_cache_key(wav_fpath, exaggeration)
                    _voice_embedding_cache[cache_key] = self.conds
                    _cache_memory_usage = estimated_size
                    logging.info(f"💾 Voice embeddings cached after cleanup ({estimated_size}MB)")
                    
            except Exception as e:
                logging.warning(f"⚠️ Caching failed: {e}, continuing without cache")

    def generate(
        self,
        text,
        audio_prompt_path=None,
        exaggeration=0.5,
        cfg_weight=0.5,
        temperature=0.8,
        min_p=0.05,
        top_p=0.8,
        repetition_penalty=2.0,
        seed=0,
    ):
        if audio_prompt_path:
            self.prepare_conditionals(audio_prompt_path, exaggeration=exaggeration)
        else:
            assert self.conds is not None, "Please `prepare_conditionals` first or specify `audio_prompt_path`"

        # Update exaggeration if needed
        if exaggeration != self.conds.t3.emotion_adv[0, 0, 0]:
            _cond: T3Cond = self.conds.t3
            self.conds.t3 = T3Cond(
                speaker_emb=_cond.speaker_emb,
                cond_prompt_speech_tokens=_cond.cond_prompt_speech_tokens,
                emotion_adv=exaggeration * torch.ones(1, 1, 1),
            ).to(device=self.device)

        # Norm and tokenize text
        text = punc_norm(text)
        text_tokens = self.tokenizer.text_to_tokens(text).to(self.device)

        if cfg_weight > 0.0:
            text_tokens = torch.cat([text_tokens, text_tokens], dim=0)  # Need two seqs for CFG

        sot = self.t3.hp.start_text_token
        eot = self.t3.hp.stop_text_token
        text_tokens = F.pad(text_tokens, (1, 0), value=sot)
        text_tokens = F.pad(text_tokens, (0, 1), value=eot)

        with torch.inference_mode():
            speech_tokens = self.t3.inference(
                t3_cond=self.conds.t3,
                text_tokens=text_tokens,
                max_new_tokens=1000,  # TODO: use the value in config
                temperature=temperature,
                cfg_weight=cfg_weight,
                min_p=min_p,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
            )
            # Extract only the conditional batch.
            speech_tokens = speech_tokens[0]

            # TODO: output becomes 1D
            speech_tokens = drop_invalid_tokens(speech_tokens)
            
            speech_tokens = speech_tokens[speech_tokens < 6561]

            speech_tokens = speech_tokens.to(self.device)

            wav, _ = self.s3gen.inference(
                speech_tokens=speech_tokens,
                ref_dict=self.conds.gen,
            )
            wav = wav.squeeze(0).detach().cpu().numpy()
            watermarked_wav = self.watermarker.apply_watermark(wav, sample_rate=self.sr)
        return torch.from_numpy(watermarked_wav).unsqueeze(0)

    def generate_batch(
        self,
        texts: list[str],
        audio_prompt_path=None,
        exaggeration=0.5,
        cfg_weight=0.5,
        temperature=0.8,
        min_p=0.05,
        top_p=0.8,
        repetition_penalty=2.0,
        seed=0,
    ):
        if audio_prompt_path:
            self.prepare_conditionals(audio_prompt_path, exaggeration=exaggeration)
        else:
            assert self.conds is not None, "Please `prepare_conditionals` first or specify `audio_prompt_path`"

        if exaggeration != self.conds.t3.emotion_adv[0, 0, 0]:
            _cond: T3Cond = self.conds.t3
            self.conds.t3 = T3Cond(
                speaker_emb=_cond.speaker_emb,
                cond_prompt_speech_tokens=_cond.cond_prompt_speech_tokens,
                emotion_adv=exaggeration * torch.ones(1, 1, 1),
            ).to(device=self.device)

        norm_texts = [punc_norm(text) for text in texts]
        text_tokens = [self.tokenizer.text_to_tokens(text) for text in norm_texts]

        max_len = max(t.shape[1] for t in text_tokens)
        text_tokens_padded = torch.stack([F.pad(t, (0, max_len - t.shape[1]), value=self.t3.hp.stop_text_token) for t in text_tokens])
        text_tokens_padded = text_tokens_padded.squeeze(1).to(self.device)

        if cfg_weight > 0.0:
            text_tokens_padded = torch.cat([text_tokens_padded, text_tokens_padded], dim=0)

        sot = self.t3.hp.start_text_token
        text_tokens_padded = F.pad(text_tokens_padded, (1, 0), value=sot)

        with torch.inference_mode():
            speech_tokens_batch = self.t3.inference(
                t3_cond=self.conds.t3,
                text_tokens=text_tokens_padded,
                max_new_tokens=1000,
                temperature=temperature,
                cfg_weight=cfg_weight,
                min_p=min_p,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
            )

            wavs = []
            for speech_tokens in speech_tokens_batch:
                speech_tokens = drop_invalid_tokens(speech_tokens)
                speech_tokens = speech_tokens[speech_tokens < 6561]
                speech_tokens = speech_tokens.to(self.device)

                wav, _ = self.s3gen.inference(
                    speech_tokens=speech_tokens,
                    ref_dict=self.conds.gen,
                )
                wav = wav.squeeze(0).detach().cpu().numpy()
                watermarked_wav = self.watermarker.apply_watermark(wav, sample_rate=self.sr)
                wavs.append(torch.from_numpy(watermarked_wav).unsqueeze(0))
        return wavs