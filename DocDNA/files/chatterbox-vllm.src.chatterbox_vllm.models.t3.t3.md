# chatterbox-vllm.src.chatterbox_vllm.models.t3.t3

## Public API

### Classes
- **T3ProcessingInfo**  
  Methods: get_supported_mm_limits
- **T3MultiModalDummyInputsBuilder**  
  Methods: get_dummy_text, get_dummy_mm_data
- **T3MultiModalDataParser**  
  Methods: parse_mm_data
- **ConditionalsEmbeddingItems**  
  Methods: get_count, get, get_processor_data, get_passthrough_data
- **T3MultiModalProcessor**  
  Methods: apply
- **T3VllmModel** — Native vLLM implementation of the Chatterbox T3   
  Methods: load_weights, get_multimodal_embeddings, split_prefill_decode, get_input_embeddings, compute_logits, forward, get_language_model

### Functions
- **create_triangular_matrix**
- **get_supported_mm_limits**
- **get_dummy_text**
- **get_dummy_mm_data**
- **parse_mm_data**
- **get_count**
- **get**
- **get_processor_data**
- **get_passthrough_data**
- **apply** — Process multi-modal inputs to be used in vLLM.
- **load_weights**
- **get_multimodal_embeddings**
- **split_prefill_decode** — vLLM combines the prefill and decode into a single input tensor. We need to split them back
- **get_input_embeddings**
- **compute_logits**
- **forward**
- **get_language_model**

## Imports (local guesses)
- chatterbox_vllm.models.t3.modules.learned_pos_emb, chatterbox_vllm.models.t3.modules.t3_config, os, random, torch, torch.nn, transformers.feature_extraction_utils, typing, vllm.config, vllm.model_executor.layers.logits_processor, vllm.model_executor.layers.vocab_parallel_embedding, vllm.model_executor.models.interfaces, vllm.model_executor.models.interfaces_base, vllm.model_executor.models.llama, vllm.model_executor.sampling_metadata, vllm.multimodal, vllm.multimodal.inputs, vllm.multimodal.parse, vllm.multimodal.processing, vllm.multimodal.profiling, vllm.sequence

## Relative imports
- .modules.cond_enc

## Side-effect signals
- file_io