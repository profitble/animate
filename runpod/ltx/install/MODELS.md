# Runpod Model Download Guide

5 models.

## STEP 1: Create directories

```bash
cd /workspace && mkdir -p ComfyUI/models/{text_encoders,checkpoints,loras,latent_upscale_models}
```

## STEP 2: Download models 1–3

```bash
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/text_encoders/gemma_3_12B_it.safetensors "https://huggingface.co/Comfy-Org/ltx-2/resolve/main/split_files/text_encoders/gemma_3_12B_it.safetensors" && \
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/text_encoders/ltx-2.3_text_projection_bf16.safetensors "https://huggingface.co/Kijai/LTX2.3_comfy/resolve/main/text_encoders/ltx-2.3_text_projection_bf16.safetensors" && \
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/checkpoints/ltx-2.3-22b-dev.safetensors "https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-22b-dev.safetensors"
```

## STEP 3: Download models 4–5

```bash
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/loras/ltx-2.3-22b-distilled-lora-384-1.1.safetensors "https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-22b-distilled-lora-384-1.1.safetensors" && \
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.1.safetensors "https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-spatial-upscaler-x2-1.1.safetensors"
```
