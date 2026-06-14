import modal
import json
import time
import os

image = modal.Image.from_dockerfile("Dockerfile")

app = modal.App("bbq-animate", image=image)
model_volume = modal.Volume.from_name("bbq-models", create_if_missing=True)
output_volume = modal.Volume.from_name("bbq-outputs", create_if_missing=True)

_FUNC_KWARGS = dict(
    timeout=86400, memory=65536,
    volumes={
        "/workspace/models":  model_volume,
        "/workspace/outputs": output_volume,
    },
)


@app.function(gpu="H200", **_FUNC_KWARGS)
def generate(workflow_data: dict, image_url: str, video_url: str, job_id: str) -> str:
    import subprocess
    import urllib.request
    import urllib.error
    import datetime
    import shutil

    os.makedirs("/workspace/outputs", exist_ok=True)

    def log(msg=""):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {msg}")

    log(f"Job {job_id} starting ...")

    log("Setting up models symlink ...")
    subprocess.run(
        "rm -rf /comfyui/models && ln -sf /workspace/models /comfyui/models",
        shell=True, check=True,
    )

    log("Downloading inputs ...")
    os.makedirs("/comfyui/input", exist_ok=True)
    subprocess.run(f"wget -q -O /comfyui/input/image.jpeg {image_url}", shell=True, check=True)
    subprocess.run(f"wget -q -O /comfyui/input/video.mp4 {video_url}", shell=True, check=True)
    log("Inputs ready.")

    os.makedirs("/comfyui/custom_nodes/ComfyUI-Frame-Interpolation/ckpts/rife", exist_ok=True)
    rife_src = "/workspace/models/rife/rife49.pth"
    rife_dst = "/comfyui/custom_nodes/ComfyUI-Frame-Interpolation/ckpts/rife/rife49.pth"
    if os.path.exists(rife_src) and not os.path.exists(rife_dst):
        subprocess.run(["cp", rife_src, rife_dst], check=True)

    cmd = ["python", "main.py", "--port", "8188"]
    log(f"Starting ComfyUI: {' '.join(cmd)}")
    proc = subprocess.Popen(cmd, cwd="/comfyui", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    ready = False
    for i in range(120):
        try:
            with urllib.request.urlopen("http://127.0.0.1:8188/system_stats") as r:
                if r.status == 200:
                    ready = True
                    log(f"ComfyUI ready after {i}s")
                    break
        except urllib.error.URLError:
            time.sleep(1)

    if not ready:
        out, _ = proc.communicate(timeout=5)
        proc.terminate()
        raise RuntimeError(f"ComfyUI failed to start.\nLast output:\n{out.decode()[-2000:]}")

    data = json.dumps({"prompt": workflow_data}).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:8188/prompt", data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as r:
            prompt_id = json.loads(r.read())["prompt_id"]
        log(f"Workflow submitted — prompt_id: {prompt_id}")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        proc.terminate()
        raise RuntimeError(f"Failed to submit workflow: HTTP {e.code}\n{body[:3000]}")

    while True:
        line = proc.stdout.readline()
        if line:
            decoded = line.decode(errors="replace").rstrip()
            log(f"[comfy] {decoded}")
            if any(kw in decoded for kw in ("CUDA out of memory", "OutOfMemoryError", "out of memory")):
                proc.terminate()
                raise RuntimeError("OOM during generation.")
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:8188/history/{prompt_id}") as r:
                if prompt_id in json.loads(r.read()):
                    log("Workflow complete.")
                    break
        except urllib.error.URLError:
            pass
        time.sleep(0.5)

    proc.terminate()
    proc.wait()

    dest = f"/workspace/outputs/{job_id}"
    if os.path.exists(dest):
        shutil.rmtree(dest)
    if os.path.exists("/comfyui/output") and os.listdir("/comfyui/output"):
        shutil.copytree("/comfyui/output", dest)

    output_volume.commit()
    log(f"Outputs saved → {dest}")
    return dest
