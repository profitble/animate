import modal
import json
import re
import time
import os
from pathlib import Path

image = modal.Image.from_dockerfile("Dockerfile")

app = modal.App("ltx", image=image)
model_volume = modal.Volume.from_name("ltx-models", create_if_missing=True)
output_volume = modal.Volume.from_name("ltx-outputs", create_if_missing=True)

_FUNC_KWARGS = dict(
    timeout=86400, memory=65536,
    volumes={
        "/workspace/models":  model_volume,
        "/workspace/outputs": output_volume,
    },
)


@app.function(gpu="H200", **_FUNC_KWARGS)
def generate(workflow_data: dict, image_url: str, prompt: str, job_id: str, negative_prompt: str | None = None) -> str:
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
    log("Inputs ready.")

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

    workflow_data["222"]["inputs"]["image"] = "image.jpeg"
    workflow_data["200"]["inputs"]["prompt"] = prompt
    if negative_prompt is not None:
        workflow_data["223:206"]["inputs"]["text"] = negative_prompt

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


WORKFLOW = Path(__file__).parent.parent / "workflows" / "ltx-api.json"


@app.local_entrypoint()
def test(test_file: str = "../../test.md"):
    text = Path(test_file).read_text().strip()
    image_m = re.search(r"^image:\s*(\S+)", text, re.M)
    image_url = image_m.group(1) if image_m else text.splitlines()[0].strip()
    prompt_m = re.search(r"^(?:prompt|positive):\s*(.+?)(?=^(?:negative_prompt|negative):|\Z)", text, re.M | re.S)
    neg_m = re.search(r"^(?:negative_prompt|negative):\s*(.+)", text, re.M | re.S)
    prompt = prompt_m.group(1).strip()
    negative_prompt = neg_m.group(1).strip() if neg_m else None
    workflow_data = json.loads(WORKFLOW.read_text())
    result = generate.remote(workflow_data, image_url, prompt, "test", negative_prompt)
    print(f"\ndone → {result}")
    print("get outputs: modal volume get ltx-outputs / .")
