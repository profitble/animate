"""
One-time model download for BBQ Animate.

Setup (once):
  modal run modal/models.py::download_models
"""

import modal
import os

app = modal.App("bbq-animate")
model_volume = modal.Volume.from_name("bbq-models", create_if_missing=True)


@app.function(volumes={"/workspace/models": model_volume}, timeout=7200)
def download_models():
    import subprocess

    for d in [
        "/workspace/models/diffusion_models",
        "/workspace/models/text_encoders",
        "/workspace/models/clip_vision",
        "/workspace/models/vae",
        "/workspace/models/loras",
        "/workspace/models/detection",
        "/workspace/models/rife",
    ]:
        os.makedirs(d, exist_ok=True)

    HF     = "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"
    HF_HDR = f"Authorization: Bearer {HF}"

    models = [
        ("/workspace/models/text_encoders/EchoVault_T9.safetensors",
         "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/EchoVault_T9.safetensors", HF_HDR),
        ("/workspace/models/clip_vision/IronSight_V7.safetensors",
         "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/IronSight_V7.safetensors", HF_HDR),
        ("/workspace/models/vae/GlassRoot_D2.safetensors",
         "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/GlassRoot_D2.safetensors", HF_HDR),
        ("/workspace/models/loras/SolarFlint_L2.safetensors",
         "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/SolarFlint_L2.safetensors", HF_HDR),
        ("/workspace/models/loras/VelvetRush_Q4.safetensors",
         "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/VelvetRush_Q4.safetensors", HF_HDR),
        ("/workspace/models/loras/FrostByte_K7.safetensors",
         "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/FrostByte_K7.safetensors", HF_HDR),
        ("/workspace/models/loras/PhantomWeave_R5.safetensors",
         "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/PhantomWeave_R5.safetensors", HF_HDR),
        ("/workspace/models/loras/NovaMind_X1.safetensors",
         "https://huggingface.co/thatboymentor/wan2.2carbonarapackAN/resolve/main/NovaMind_X1.safetensors", HF_HDR),
        ("/workspace/models/loras/BouncyWalk02_HighWan2_2.safetensors",
         "https://civitai.com/api/download/models/2261902?type=Model&format=SafeTensor",
         "Authorization: Bearer aebf66107262778cc460e8f79e6322a0"),
        ("/workspace/models/diffusion_models/wan2.2_animate_14B_bf16.safetensors",
         "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_animate_14B_bf16.safetensors", HF_HDR),
        ("/workspace/models/detection/vitpose_h_wholebody_data.bin",
         "https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_data.bin", HF_HDR),
        ("/workspace/models/detection/vitpose_h_wholebody_model.onnx",
         "https://huggingface.co/Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_model.onnx", HF_HDR),
        ("/workspace/models/detection/yolov10m.onnx",
         "https://huggingface.co/Wan-AI/Wan2.2-Animate-14B/resolve/main/process_checkpoint/det/yolov10m.onnx", HF_HDR),
    ]

    total = len(models)
    for i, (dest, url, header) in enumerate(models, 1):
        name = os.path.basename(dest)
        if os.path.exists(dest):
            print(f"  [{i}/{total}] skip   {name}")
            continue
        print(f"  [{i}/{total}] downloading  {name} ...")
        subprocess.run(["wget", "--progress=bar:force", "--header", header, "-O", dest, url], check=True)
        print(f"  [{i}/{total}] done         {name}")

    print("\n  Committing to volume ...")
    model_volume.commit()
    print("  All models ready.\n")
