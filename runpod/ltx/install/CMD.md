### Docker
```bash
docker buildx build --platform linux/amd64 --provenance=false --sbom=false -t maxta334/ltx-docker:latest --push .
```

### Verify Models
```bash
for f in /workspace/ComfyUI/models/text_encoders/gemma_3_12B_it.safetensors /workspace/ComfyUI/models/text_encoders/ltx-2.3_text_projection_bf16.safetensors /workspace/ComfyUI/models/checkpoints/ltx-2.3-22b-dev.safetensors /workspace/ComfyUI/models/loras/ltx-2.3-22b-distilled-lora-384-1.1.safetensors /workspace/ComfyUI/models/latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.1.safetensors; do [ -f "$f" ] && echo "FOUND $(du -h "$f" | cut -f1) $f" || echo "MISSING $f"; done
```
