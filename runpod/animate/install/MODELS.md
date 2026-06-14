# Runpod Model Download Guide

13 models. SAM2 auto-downloads at runtime.

## STEP 1: Create directories

```bash
cd /workspace && mkdir -p ComfyUI/models/{diffusion_models,vae,clip_vision,loras,text_encoders,detection}
```

## STEP 2: Download models 1–3

```bash
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/text_encoders/EchoVault_T9.safetensors "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/EchoVault_T9.safetensors" && \
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/clip_vision/IronSight_V7.safetensors "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/IronSight_V7.safetensors" && \
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/vae/GlassRoot_D2.safetensors "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/GlassRoot_D2.safetensors"
```

## STEP 3: Download models 4–6

```bash
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/loras/SolarFlint_L2.safetensors "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/SolarFlint_L2.safetensors" && \
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/loras/VelvetRush_Q4.safetensors "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/VelvetRush_Q4.safetensors" && \
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/loras/FrostByte_K7.safetensors "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/FrostByte_K7.safetensors"
```

## STEP 4: Download models 7–9

```bash
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/loras/PhantomWeave_R5.safetensors "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/PhantomWeave_R5.safetensors" && \
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/loras/NovaMind_X1.safetensors "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/NovaMind_X1.safetensors" && \
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/diffusion_models/wan2.2_animate_14B_bf16.safetensors "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_animate_14B_bf16.safetensors"
```

## STEP 5: Download models 10–12

```bash
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/detection/vitpose_h_wholebody_data.bin "https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_data.bin" && \
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/detection/vitpose_h_wholebody_model.onnx "https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_model.onnx" && \
wget --header="Authorization: Bearer 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" --progress=bar:force -O /workspace/ComfyUI/models/detection/yolov10m.onnx "https://huggingface.co/Wan-AI/Wan2.2-Animate-14B/resolve/main/process_checkpoint/det/yolov10m.onnx"
```

## STEP 6: Download model 13

```bash
wget --header="Authorization: Bearer aebf66107262778cc460e8f79e6322a0" -O /workspace/ComfyUI/models/loras/BouncyWalk02_HighWan2_2.safetensors "https://civitai.com/api/download/models/2261902?type=Model&format=SafeTensor"
```
