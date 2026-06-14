### Docker
```bash
docker buildx build --platform linux/amd64 --provenance=false --sbom=false -t maxta334/bbq-docker:latest --push .
```

### Verify Models
```bash
for f in /workspace/ComfyUI/models/text_encoders/EchoVault_T9.safetensors /workspace/ComfyUI/models/clip_vision/IronSight_V7.safetensors /workspace/ComfyUI/models/vae/GlassRoot_D2.safetensors /workspace/ComfyUI/models/loras/SolarFlint_L2.safetensors /workspace/ComfyUI/models/loras/VelvetRush_Q4.safetensors /workspace/ComfyUI/models/loras/FrostByte_K7.safetensors /workspace/ComfyUI/models/loras/PhantomWeave_R5.safetensors /workspace/ComfyUI/models/loras/NovaMind_X1.safetensors /workspace/ComfyUI/models/diffusion_models/wan2.2_animate_14B_bf16.safetensors /workspace/ComfyUI/models/detection/vitpose_h_wholebody_data.bin /workspace/ComfyUI/models/detection/vitpose_h_wholebody_model.onnx /workspace/ComfyUI/models/detection/yolov10m.onnx /workspace/ComfyUI/models/loras/BouncyWalk02_HighWan2_2.safetensors; do [ -f "$f" ] && echo "FOUND $(du -h "$f" | cut -f1) $f" || echo "MISSING $f"; done
```