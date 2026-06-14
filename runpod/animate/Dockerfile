# June 10, 2026 Working

FROM nvidia/cuda:12.6.2-cudnn-devel-ubuntu22.04

ARG COMFYUI_COMMIT=master
ARG VIDEOHELPERSUITE_COMMIT=HEAD

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_PREFER_BINARY=1 \
    PYTHONUNBUFFERED=1 \
    CMAKE_BUILD_PARALLEL_LEVEL=8 \
    PIP_NO_INPUT=1 \
    PIP_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cu124 \
    PATH=/opt/venv/bin:/root/.local/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LD_LIBRARY_PATH=/usr/local/cuda/lib64/stubs:/usr/local/cuda/lib64:${LD_LIBRARY_PATH:-} \
    LIBRARY_PATH=/usr/local/cuda/lib64/stubs:/usr/local/cuda/lib64:${LIBRARY_PATH:-}

# ── System dependencies ───────────────────────────────────────────────────────

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        python3 python3-venv python3-pip \
        git wget curl ffmpeg \
        libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip \
    && apt-get autoremove -y && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# ── uv + venv ─────────────────────────────────────────────────────────────────

RUN wget -qO- https://astral.sh/uv/install.sh | sh \
    && ln -sf /root/.local/bin/uv /usr/local/bin/uv \
    && ln -sf /root/.local/bin/uvx /usr/local/bin/uvx

RUN uv venv /opt/venv

# ── ComfyUI ───────────────────────────────────────────────────────────────────

WORKDIR /comfyui
RUN git clone https://github.com/comfyanonymous/ComfyUI.git . \
    && git checkout ${COMFYUI_COMMIT}

RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install --upgrade pip setuptools wheel \
    && /opt/venv/bin/pip install -r requirements.txt \
    && /opt/venv/bin/pip install torch torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/cu124

RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install \
        requests websocket-client fastapi[standard] uvicorn \
        onnxruntime-gpu taichi

RUN sed -i '1s/^/import sys\nsys.setrecursionlimit(10000)\n/' /comfyui/execution.py

# ── Custom nodes ──────────────────────────────────────────────────────────────

WORKDIR /comfyui/custom_nodes

# 1. ComfyUI-WanVideoWrapper
ARG WANVIDEO_CACHEBUST=2
RUN git clone --depth 1 https://github.com/kijai/ComfyUI-WanVideoWrapper
RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install -r ComfyUI-WanVideoWrapper/requirements.txt || true

# 2. ComfyUI-VideoHelperSuite
RUN git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite \
    && cd ComfyUI-VideoHelperSuite && git checkout ${VIDEOHELPERSUITE_COMMIT}
RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install imageio-ffmpeg opencv-python \
    && /opt/venv/bin/pip install -r ComfyUI-VideoHelperSuite/requirements.txt

# 3. ComfyUI-KJNodes
RUN git clone --depth 1 https://github.com/kijai/ComfyUI-KJNodes
RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install -r ComfyUI-KJNodes/requirements.txt || true

# 4. ComfyUI-Frame-Interpolation
RUN git clone --depth 1 https://github.com/Fannovel16/ComfyUI-Frame-Interpolation
RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install -r ComfyUI-Frame-Interpolation/requirements.txt || true

# 5. ComfyUI-segment-anything-2 (kijai)
RUN git clone --depth 1 https://github.com/kijai/ComfyUI-segment-anything-2
RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install -r ComfyUI-segment-anything-2/requirements.txt || true

# 6. rgthree-comfy
RUN git clone --depth 1 https://github.com/rgthree/rgthree-comfy
RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install -r rgthree-comfy/requirements.txt || true

# 7. ComfyUI-Custom-Scripts
RUN git clone --depth 1 https://github.com/pythongosssss/ComfyUI-Custom-Scripts

# 8. ComfyUI-Easy-Use
RUN git clone --depth 1 https://github.com/yolain/ComfyUI-Easy-Use
RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install -r ComfyUI-Easy-Use/requirements.txt

# 9. comfyui-propost
RUN git clone --depth 1 https://github.com/digitaljohn/comfyui-propost
RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install -r comfyui-propost/requirements.txt

# 10. ComfyMath
RUN git clone --depth 1 https://github.com/evanspearman/ComfyMath
RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install -r ComfyMath/requirements.txt || true

# 11. CRT-Nodes
RUN git clone --depth 1 https://github.com/PGCRT/CRT-Nodes
RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install -r CRT-Nodes/requirements.txt

# 12. ComfyUI-WanAnimatePreprocess
RUN git clone --depth 1 https://github.com/kijai/ComfyUI-WanAnimatePreprocess
RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install -r ComfyUI-WanAnimatePreprocess/requirements.txt || true

# ── Entrypoint ────────────────────────────────────────────────────────────────

WORKDIR /comfyui
EXPOSE 8188

RUN --mount=type=cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install --force-reinstall \
    torch==2.4.1+cu124 \
    torchvision==0.19.1+cu124 \
    torchaudio==2.4.1+cu124 \
    --index-url https://download.pytorch.org/whl/cu124

ENTRYPOINT []
CMD ["sh", "-c", "\
  rm -rf /comfyui/models && ln -sf /workspace/ComfyUI/models /comfyui/models; \
  mkdir -p /workspace/ComfyUI/models/detection; \
  mkdir -p /comfyui/custom_nodes/ComfyUI-Frame-Interpolation/ckpts/rife; \
  [ -f /workspace/ComfyUI/models/rife/rife49.pth ] && \
    cp /workspace/ComfyUI/models/rife/rife49.pth \
    /comfyui/custom_nodes/ComfyUI-Frame-Interpolation/ckpts/rife/rife49.pth || true; \
  exec /usr/bin/python main.py --listen 0.0.0.0 --port 8188 --enable-manager"]