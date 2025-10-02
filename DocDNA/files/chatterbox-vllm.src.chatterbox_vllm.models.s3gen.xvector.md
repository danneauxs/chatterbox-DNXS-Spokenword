# chatterbox-vllm.src.chatterbox_vllm.models.s3gen.xvector

## Public API

### Classes
- **BasicResBlock**  
  Methods: forward
- **FCM**  
  Methods: forward
- **StatsPool**  
  Methods: forward
- **TDNNLayer**  
  Methods: forward
- **CAMLayer**  
  Methods: forward, seg_pooling
- **CAMDenseTDNNLayer**  
  Methods: bn_function, forward
- **CAMDenseTDNNBlock**  
  Methods: forward
- **TransitLayer**  
  Methods: forward
- **DenseLayer**  
  Methods: forward
- **CAMPPlus**  
  Methods: forward, inference

### Functions
- **pad_list** — Perform padding for the list of tensors.
- **extract_feature**
- **get_nonlinear**
- **statistics_pooling**
- **forward**
- **forward**
- **forward**
- **forward**
- **forward**
- **seg_pooling**
- **bn_function**
- **forward**
- **forward**
- **forward**
- **forward**
- **forward**
- **inference**

## Imports (local guesses)
- collections, torch, torch.nn.functional, torch.utils.checkpoint, torchaudio.compliance.kaldi