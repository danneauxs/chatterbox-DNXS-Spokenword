# chatterbox-vllm.src.chatterbox_vllm.models.t3.entokenizer

## Public API

### Classes
- **EnTokenizer** — A VLLM-compatible tokenizer that wraps the original Tokenizer implementation.  
  Methods: from_pretrained, check_vocabset_sot_eot, get_vocab_size, get_vocab, convert_tokens_to_string, save_pretrained, text_to_tokens, encode, decode, max_token_id

### Functions
- **from_pretrained** — Instantiate a tokenizer from a pretrained model or path.
- **check_vocabset_sot_eot**
- **get_vocab_size**
- **get_vocab**
- **convert_tokens_to_string**
- **save_pretrained** — Save the tokenizer to a directory.
- **text_to_tokens** — Legacy method for backward compatibility
- **encode** — Legacy method for backward compatibility
- **decode** — Legacy method for backward compatibility
- **max_token_id**

## Imports (local guesses)
- logging, os, tokenizers, torch, transformers, typing