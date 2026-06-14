"""
One-time model download for LTX.

Setup (once):
  modal run modal/ltx/models.py::download_models
"""

import modal
import os

app = modal.App("ltx")
image = modal.Image.debian_slim().apt_install("wget")
model_volume = modal.Volume.from_name("ltx-models", create_if_missing=True)


@app.function(image=image, volumes={"/workspace/models": model_volume}, timeout=7200)
def download_models():
    import subprocess

    for d in [
        "/workspace/models/text_encoders",
        "/workspace/models/checkpoints",
        "/workspace/models/loras",
        "/workspace/models/latent_upscale_models",
    ]:
        os.makedirs(d, exist_ok=True)

    HF     = "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"
    HF_HDR = f"Authorization: Bearer {HF}"

    models = [
        ("/workspace/models/text_encoders/gemma_3_12B_it.safetensors",
         "https://huggingface.co/Comfy-Org/ltx-2/resolve/main/split_files/text_encoders/gemma_3_12B_it.safetensors", HF_HDR),
        ("/workspace/models/text_encoders/ltx-2.3_text_projection_bf16.safetensors",
         "https://huggingface.co/Kijai/LTX2.3_comfy/resolve/main/text_encoders/ltx-2.3_text_projection_bf16.safetensors", HF_HDR),
        ("/workspace/models/checkpoints/ltx-2.3-22b-dev.safetensors",
         "https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-22b-dev.safetensors", HF_HDR),
        ("/workspace/models/loras/ltx-2.3-22b-distilled-lora-384-1.1.safetensors",
         "https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-22b-distilled-lora-384-1.1.safetensors", HF_HDR),
        ("/workspace/models/latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.1.safetensors",
         "https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-spatial-upscaler-x2-1.1.safetensors", HF_HDR),
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
