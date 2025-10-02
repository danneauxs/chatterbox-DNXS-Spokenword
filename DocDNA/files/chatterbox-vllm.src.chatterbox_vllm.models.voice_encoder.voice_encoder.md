# chatterbox-vllm.src.chatterbox_vllm.models.voice_encoder.voice_encoder

## Public API

### Classes
- **VoiceEncoder**  
  Methods: device, forward, inference, utt_to_spk_embed, voice_similarity, embeds_from_mels, embeds_from_wavs

### Functions
- **pack** — Given a list of length B of array-like objects of shapes (Ti, ...), packs them in a single tensor of
- **get_num_wins**
- **get_frame_step**
- **stride_as_partials** — Takes unscaled mels in (T, M) format
- **device**
- **forward** — Computes the embeddings of a batch of partial utterances.
- **inference** — Computes the embeddings of a batch of full utterances with gradients.
- **utt_to_spk_embed** — Takes an array of L2-normalized utterance embeddings, computes the mean embedding and L2-normalize it to get a
- **voice_similarity** — Cosine similarity for L2-normalized utterance embeddings or speaker embeddings
- **embeds_from_mels** — Convenience function for deriving utterance or speaker embeddings from mel spectrograms.
- **embeds_from_wavs** — Wrapper around embeds_from_mels

## Imports (local guesses)
- librosa, numpy, numpy.lib.stride_tricks, torch, torch.nn.functional, typing

## Relative imports
- .config, .melspec