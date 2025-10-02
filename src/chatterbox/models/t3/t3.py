# Copyright (c) 2025 Resemble AI
# MIT License
import logging
from typing import Union, Optional, List

from tqdm import tqdm
import os
import torch
import torch.nn.functional as F
from torch import nn, Tensor
from transformers import LlamaModel, LlamaConfig
from transformers.generation.logits_process import TopPLogitsWarper, MinPLogitsWarper, RepetitionPenaltyLogitsProcessor

from .modules.learned_pos_emb import LearnedPositionEmbeddings

from .modules.cond_enc import T3CondEnc, T3Cond
from .modules.t3_config import T3Config
from .llama_configs import LLAMA_CONFIGS
from .inference.t3_hf_backend import T3HuggingfaceBackend
from .inference.alignment_stream_analyzer import AlignmentStreamAnalyzer


logger = logging.getLogger(__name__)


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def _ensure_BOT_EOT(text_tokens: Tensor, hp):
    B = text_tokens.size(0)
    assert (text_tokens == hp.start_text_token).int().sum() >= B, "missing start_text_token"
    assert (text_tokens == hp.stop_text_token).int().sum() >= B, "missing stop_text_token"


class T3(nn.Module):
    """
    Token-To-Token (T3) TTS model using huggingface transformer models as backbones,
        * tokenization, including start / stop tokens are always added externally to this class
        * conditioning data like CLAP, emotion, etc are all in a separate file for more modularity
        * careful! this class assumes relative positional encoding -- with absolute PE, we would at
            least want to reset the position to 0 when speech tokens begin, and optionally use a
            different PE embedding space for speech.
    """

    def __init__(self, hp=T3Config()):
        super().__init__()
        self.hp = hp
        self.cfg = LlamaConfig(**LLAMA_CONFIGS[hp.llama_config_name])
        # Prefer eager attention for compatibility (export and runtime stability)
        try:
            setattr(self.cfg, "attn_implementation", "eager")
        except Exception:
            pass
        self.tfmr = LlamaModel(self.cfg)
        self.dim = self.cfg.hidden_size
        self.deepspeed_patch_applied = False

        # conditioning / embedding
        self.cond_enc = T3CondEnc(hp)
        self.text_emb = nn.Embedding(hp.text_tokens_dict_size, self.dim)
        self.speech_emb = nn.Embedding(hp.speech_tokens_dict_size, self.dim)

        # custom position embedding
        if hp.input_pos_emb == "learned":
            max_text_seq_len = hp.max_text_tokens + 2
            self.text_pos_emb = LearnedPositionEmbeddings(max_text_seq_len, self.dim)

            max_mel_seq_len = hp.max_speech_tokens + 2 + 2
            self.speech_pos_emb = LearnedPositionEmbeddings(max_mel_seq_len, self.dim)

        # logit projection
        self.text_head = nn.Linear(self.cfg.hidden_size, hp.text_tokens_dict_size, bias=False)
        self.speech_head = nn.Linear(self.cfg.hidden_size, hp.speech_tokens_dict_size, bias=False)
        # ONNX export compatibility flag
        self.onnx_export_mode = False

    @property
    def device(self):
        return self.speech_head.weight.device

    def prepare_conditioning(self, t3_cond: T3Cond):
        """
        Token cond data needs to be embedded, so that needs to be here instead of in `T3CondEnc`.
        """
        if t3_cond.cond_prompt_speech_tokens is not None and t3_cond.cond_prompt_speech_emb is None:
            t3_cond.cond_prompt_speech_emb = self.speech_emb(t3_cond.cond_prompt_speech_tokens) + \
                self.speech_pos_emb(t3_cond.cond_prompt_speech_tokens)
        return self.cond_enc(t3_cond)  # (B, len_cond, dim)

    def prepare_input_embeds(
        self,
        *,
        t3_cond: T3Cond,
        text_tokens: torch.LongTensor,
        speech_tokens: torch.LongTensor,
        cfg_weight: float = 0.0,
    ):
        # prepare input embeddings (skip backbone transformer embeddings)
        # Base (conditional) branch
        cond_emb = self.prepare_conditioning(t3_cond)  # (B, len_cond, dim)
        text_emb = self.text_emb(text_tokens)          # (B, len_text, dim)
        speech_emb = self.speech_emb(speech_tokens)    # (B, len_speech, dim)

        if self.hp.input_pos_emb == "learned":
            text_emb = text_emb + self.text_pos_emb(text_tokens)
            speech_emb = speech_emb + self.speech_pos_emb(speech_tokens)
        len_cond = cond_emb.size(1)

        B = text_emb.size(0)

        if cfg_weight > 0.0:
            # Classifier-Free Guidance: duplicate text/speech to 2×B
            # First B = conditional; Second B = unconditional (zero text embedding)
            uncond_text = torch.zeros_like(text_emb)
            text_emb = torch.cat([text_emb, uncond_text], dim=0)  # (2B, len_text, dim)
            speech_emb = torch.cat([speech_emb, speech_emb], dim=0)  # (2B, len_speech, dim)

        # Ensure cond matches text batch size (handles B==1 and expanded 2B cases)
        if cond_emb.size(0) != text_emb.size(0):
            target_b = text_emb.size(0)
            src_b = cond_emb.size(0)
            if src_b == 1:
                cond_emb = cond_emb.expand(target_b, -1, -1)
            elif target_b % src_b == 0:
                repeat_factor = target_b // src_b
                cond_emb = cond_emb.repeat(repeat_factor, 1, 1)
            else:
                # Fallback: tile to match target batch
                cond_emb = cond_emb.repeat((target_b, 1, 1))[:target_b]

        # Vectorized concat along sequence dimension (export-friendly)
        embeds = torch.cat((cond_emb, text_emb, speech_emb), dim=1)  # (B or 2B, length, dim)
        return embeds, len_cond

    def forward(
        self,
        *,
        t3_cond: T3Cond,
        text_tokens: torch.LongTensor,
        text_token_lens: torch.LongTensor,
        speech_tokens: torch.LongTensor,
        speech_token_lens: torch.LongTensor,
        training=False,
    ):
        if not self.onnx_export_mode:
            _ensure_BOT_EOT(text_tokens, self.hp)

        # prepare custom input embeds
        embeds, len_cond = self.prepare_input_embeds(
            t3_cond=t3_cond,
            text_tokens=text_tokens,
            speech_tokens=speech_tokens,
        )

        # backbone transformer forward
        if self.onnx_export_mode:
            # Simpler export path: no hidden_states list, just last_hidden_state
            tfmr_out = self.tfmr.forward(
                input_ids=None,
                inputs_embeds=embeds,
                output_hidden_states=False,
                return_dict=False,
                use_cache=False,
            )
            # Expected tuple: (last_hidden_state, ...)
            hidden_states = tfmr_out[0]
        else:
            tfmr_out = self.tfmr.forward(
                input_ids=None,
                inputs_embeds=embeds,
                output_hidden_states=True,
                return_dict=True,
                use_cache=(not training),
            )
            hidden_states = tfmr_out.hidden_states[-1]  # final tfmr layer output, (B, seq, dim)

        # post-processing: splice out text and speech parts of hidden states
        len_text = text_tokens.size(1)
        len_speech = speech_tokens.size(1)
        B, _, dim = hidden_states.shape
        device, dtype = hidden_states.device, hidden_states.dtype
        if self.onnx_export_mode:
            # Export-friendly slicing: assume uniform lengths per batch
            text_latents = hidden_states[:, len_cond:len_cond + len_text, :]
            speech_start = len_cond + len_text
            speech_latents = hidden_states[:, speech_start:speech_start + len_speech, :]
        else:
            text_latents = torch.zeros(B, len_text, dim, dtype=dtype, device=device)
            speech_latents = torch.zeros(B, len_speech, dim, dtype=dtype, device=device)
            ttl, stl = text_token_lens, speech_token_lens
            for i in range(B):
                text_end = len_cond + ttl[i].item()
                speech_start = len_cond + text_tokens.size(1)
                speech_end = speech_start + stl[i].item()
                text_latents[i, :ttl[i]] = hidden_states[i, len_cond:text_end]
                speech_latents[i, :stl[i]] = hidden_states[i, speech_start:speech_end]

        # logit projection
        text_logits = self.text_head(text_latents)
        speech_logits = self.speech_head(speech_latents)

        return AttrDict(
            text_logits=text_logits,
            text_latents=text_latents,
            speech_logits=speech_logits,
            speech_latents=speech_latents,
            hidden_states=hidden_states,
        )

    def loss(
        self,
        *,
        t3_cond: T3Cond,
        text_tokens: torch.LongTensor,
        text_token_lens: torch.LongTensor,
        speech_tokens: torch.LongTensor,
        speech_token_lens: torch.LongTensor,
    ):
        "training method"
        len_text = text_tokens.size(1)
        len_speech = speech_tokens.size(1)
        assert len_text == text_token_lens.max()
        assert len_speech == speech_token_lens.max()

        out = self.forward(
            t3_cond=t3_cond,
            text_tokens=text_tokens,
            text_token_lens=text_token_lens,
            speech_tokens=speech_tokens,
            speech_token_lens=speech_token_lens,
            training=True,
        )  # (B, seq, vocab_size)

        # Calc CCE losses
        IGNORE_ID = -100
        device = out.text_logits.device
        mask_text = torch.arange(len_text, device=device)[None] >= text_token_lens[:, None]  # (B, len_text)
        mask_speech = torch.arange(len_speech, device=device)[None] >= speech_token_lens[:, None]  # (B, len_speech)
        masked_text = text_tokens.masked_fill(mask_text, IGNORE_ID)
        masked_speech = speech_tokens.masked_fill(mask_speech, IGNORE_ID)
        loss_text = F.cross_entropy(out.text_logits, masked_text, ignore_index=IGNORE_ID)
        loss_speech = F.cross_entropy(out.speech_logits, masked_speech, ignore_index=IGNORE_ID)

        return loss_text, loss_speech

    @torch.inference_mode()
    def inference(
        self,
        *,
        t3_cond: T3Cond,
        text_tokens: Tensor,
        initial_speech_tokens: Optional[Tensor]=None,

        # misc conditioning
        prepend_prompt_speech_tokens: Optional[Tensor]=None,

        # HF generate args
        num_return_sequences=1,
        max_new_tokens=None,
        stop_on_eos=True,
        do_sample=True,
        temperature=0.8,
        top_p=0.8,
        min_p=0.05,
        length_penalty=1.0,
        repetition_penalty=2.0,
        cfg_weight=0,
        enable_alignment_analysis: bool = False,
    ):
        """
        Args:
            text_tokens: a 1D (unbatched) or 2D (batched) tensor.
        """
        # Validate / sanitize inputs
        assert prepend_prompt_speech_tokens is None, "not implemented"
        _ensure_BOT_EOT(text_tokens, self.hp)
        text_tokens = torch.atleast_2d(text_tokens).to(dtype=torch.long, device=self.device)

        # Default initial speech to a single start-of-speech token
        if initial_speech_tokens is None:
            initial_speech_tokens = self.hp.start_speech_token * torch.ones_like(text_tokens[:, :1])

        # Prepare custom input embeds
        embeds, len_cond = self.prepare_input_embeds(
            t3_cond=t3_cond,
            text_tokens=text_tokens,
            speech_tokens=initial_speech_tokens,
            cfg_weight=cfg_weight,
        )

        # In order to use the standard HF generate method, we need to extend some methods to inject our custom logic
        # Note the llama-specific logic. Other tfmr types can be added later.

        # TODO? synchronize the expensive compile function
        # with self.compile_lock:
        alignment_stream_analyzer = None
        if not hasattr(self, 'patched_model'):
            self.patched_model = T3HuggingfaceBackend(
                config=self.cfg,
                llama=self.tfmr,
                speech_enc=self.speech_emb,
                speech_head=self.speech_head,
                alignment_stream_analyzer=None,
            )

        # Enable per-call alignment analysis only when requested
        if enable_alignment_analysis:
            alignment_stream_analyzer = AlignmentStreamAnalyzer(
                self.tfmr,
                None,
                text_tokens_slice=(len_cond, len_cond + text_tokens.size(-1)),
                alignment_layer_idx=9,  # TODO: hparam or something?
                eos_idx=self.hp.stop_speech_token,
            )
            self.patched_model.alignment_stream_analyzer = alignment_stream_analyzer
        else:
            # Ensure analyzer is disabled when not needed
            self.patched_model.alignment_stream_analyzer = None

        # # Run normal generate method, which calls our custom extended methods
        # return self.patched_model.generate(
        #     inputs=initial_speech_tokens,
        #     decoder_cond=embeds,
        #     bos_token_id=self.hp.start_speech_token,
        #     eos_token_id=(self.hp.stop_speech_token if stop_on_eos else -1),
        #     pad_token_id=self.hp.stop_speech_token,
        #     max_new_tokens=max_new_tokens or self.hp.max_speech_tokens,
        #     num_return_sequences=num_return_sequences,
        #     temperature=temperature,
        #     top_p=top_p,
        #     length_penalty=length_penalty,
        #     repetition_penalty=repetition_penalty,
        #     do_sample=do_sample,
        #     # cache_implementation=None if not self.compiled else "static",
        # )

        device = embeds.device

        # Build BOS per batch item
        B = text_tokens.size(0)
        bos_token = torch.full((B, 1), self.hp.start_speech_token, dtype=torch.long, device=device)
        bos_embed = self.speech_emb(bos_token)  # (B, 1, dim)
        bos_embed = bos_embed + self.speech_pos_emb.get_fixed_embedding(0)

        # Duplicate for CFG (2×B)
        if cfg_weight > 0.0:
            bos_embed = torch.cat([bos_embed, bos_embed], dim=0)

        # Combine condition and BOS token for the initial input if cfg_weight > 0
        if cfg_weight > 0:
            inputs_embeds = torch.cat([embeds, bos_embed], dim=1)
        else:
            inputs_embeds = embeds

        # Preallocate token buffer on device to avoid per‑step tensor cat and Python list growth
        max_steps = int(max_new_tokens)
        token_buffer = torch.empty((B, max_steps + 1), dtype=torch.long, device=device)
        token_buffer[:, 0] = bos_token.squeeze(1)
        generated_len = 0  # number of generated tokens (excludes BOS)

        # A view of the currently generated sequence including BOS for processors
        generated_ids = token_buffer[:, :1]

        # For CFG, track 2×B generated_ids for processors, but only use B for final output
        if cfg_weight > 0.0:
            generated_ids_cfg = torch.cat([generated_ids, generated_ids], dim=0)  # (2B, seq_len)
        else:
            generated_ids_cfg = generated_ids

        # Instantiate the logits processors.
        top_p_warper = TopPLogitsWarper(top_p=top_p)
        min_p_warper = MinPLogitsWarper(min_p=min_p)
        repetition_penalty_processor = RepetitionPenaltyLogitsProcessor(penalty=repetition_penalty)

        # ---- Initial Forward Pass (no kv_cache yet) ----
        output = self.patched_model(
            inputs_embeds=inputs_embeds,
            past_key_values=None,
            use_cache=True,
            output_attentions=False,
            output_hidden_states=False,
            return_dict=True,
        )
        # Initialize kv_cache with the full context.
        past = output.past_key_values

        # ---- Generation Loop using kv_cache ----
        iterator = tqdm(range(max_new_tokens), desc="Sampling", dynamic_ncols=True)
        for i in iterator:
            logits = output.logits[:, -1, :]  # (B or 2B, V)

            # CFG combine per pair
            if cfg_weight > 0.0:
                twoB = logits.size(0)
                assert twoB % 2 == 0, "Expected even batch size for CFG"
                B_eff = twoB // 2
                logits = logits.view(2, B_eff, -1)
                logits_cond = logits[0]
                logits_uncond = logits[1]
                logits = logits_cond + cfg_weight * (logits_cond - logits_uncond)  # (B_eff, V)

            # Apply temperature scaling.
            if temperature != 1.0:
                logits = logits / temperature

            # Apply repetition penalty, min-p, and top‑p filtering.
            # Use the appropriate generated_ids size to match logits batch dimension
            if cfg_weight > 0.0:
                # For CFG, we reduced logits from 2B to B, so use B-sized generated_ids
                logits = repetition_penalty_processor(generated_ids, logits)
            else:
                # For non-CFG, generated_ids and logits are both B-sized
                logits = repetition_penalty_processor(generated_ids_cfg, logits)
            logits = min_p_warper(None, logits)
            logits = top_p_warper(None, logits)

            # Convert logits to probabilities and sample the next token.
            probs = torch.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)  # shape: (B, 1)

            # Append into preallocated buffer without new allocations
            token_buffer[:, generated_len + 1] = next_token.squeeze(1)
            generated_len += 1
            generated_ids = token_buffer[:, :generated_len + 1]

            # Update CFG tracking ids as well
            if cfg_weight > 0.0:
                next_token_cfg = torch.cat([next_token, next_token], dim=0)  # Duplicate for 2B
                generated_ids_cfg = torch.cat([generated_ids_cfg, next_token_cfg], dim=1)
            else:
                generated_ids_cfg = generated_ids

            # Check for EOS token across the batch: stop only if all reached EOS
            if (next_token.view(-1) == self.hp.stop_speech_token).all():
                break

            # Get embedding for the new token.
            next_token_embed = self.speech_emb(next_token)
            next_token_embed = next_token_embed + self.speech_pos_emb.get_fixed_embedding(i + 1)

            # Duplicate for CFG (2×B)
            if cfg_weight > 0.0:
                next_token_embed = torch.cat([next_token_embed, next_token_embed], dim=0)

            # Forward pass with only the new token and the cached past.
            output = self.patched_model(
                inputs_embeds=next_token_embed,
                past_key_values=past,
                output_attentions=False,
                output_hidden_states=False,
                return_dict=True,
            )
            # Update the kv_cache.
            past = output.past_key_values

        # Extract generated tokens from buffer (excluding BOS)
        predicted_tokens = token_buffer[:, 1:generated_len + 1]  # shape: (B, num_tokens)

        # Clean up alignment hook to avoid accumulation across generations
        if alignment_stream_analyzer is not None:
            try:
                alignment_stream_analyzer.close()
            except Exception:
                pass

        return predicted_tokens
