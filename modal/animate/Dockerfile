# June 10, 2026 Working
# NOTE: Modal's image builder does not support --mount=type=cache, so none are used here.

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

RUN apt-get update && apt-get install -y --no-install-recommends \
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
    && ln -sf /root/.local/bin/uvx /usr/local/bin/uvx \
    && uv venv /opt/venv

# ── ComfyUI ───────────────────────────────────────────────────────────────────

WORKDIR /comfyui
RUN git clone https://github.com/comfyanonymous/ComfyUI.git . \
    && git checkout ${COMFYUI_COMMIT}

RUN uv pip install --python /opt/venv --upgrade pip setuptools wheel \
    && uv pip install --python /opt/venv -r requirements.txt \
    && uv pip install --python /opt/venv torch==2.4.1+cu124 torchvision==0.19.1+cu124 torchaudio==2.4.1+cu124 \
        --index-url https://download.pytorch.org/whl/cu124

RUN uv pip install --python /opt/venv \
        requests websocket-client fastapi[standard] uvicorn \
        onnxruntime-gpu taichi nvidia-ml-py

RUN sed -i '1s/^/import sys\nsys.setrecursionlimit(10000)\n/' /comfyui/execution.py

# ── Custom nodes ──────────────────────────────────────────────────────────────

WORKDIR /comfyui/custom_nodes

RUN git clone --depth 1 https://github.com/kijai/ComfyUI-WanVideoWrapper \
    && uv pip install --python /opt/venv -r ComfyUI-WanVideoWrapper/requirements.txt || true

RUN git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite \
    && cd ComfyUI-VideoHelperSuite && git checkout ${VIDEOHELPERSUITE_COMMIT} \
    && uv pip install --python /opt/venv imageio-ffmpeg opencv-python \
    && uv pip install --python /opt/venv -r requirements.txt

RUN git clone --depth 1 https://github.com/kijai/ComfyUI-KJNodes \
    && uv pip install --python /opt/venv -r ComfyUI-KJNodes/requirements.txt || true

RUN git clone --depth 1 https://github.com/Fannovel16/ComfyUI-Frame-Interpolation \
    && uv pip install --python /opt/venv -r ComfyUI-Frame-Interpolation/requirements.txt || true

RUN git clone --depth 1 https://github.com/kijai/ComfyUI-segment-anything-2 \
    && uv pip install --python /opt/venv -r ComfyUI-segment-anything-2/requirements.txt || true

RUN git clone --depth 1 https://github.com/rgthree/rgthree-comfy \
    && uv pip install --python /opt/venv -r rgthree-comfy/requirements.txt || true

RUN git clone --depth 1 https://github.com/pythongosssss/ComfyUI-Custom-Scripts

RUN git clone --depth 1 https://github.com/yolain/ComfyUI-Easy-Use \
    && uv pip install --python /opt/venv -r ComfyUI-Easy-Use/requirements.txt

RUN git clone --depth 1 https://github.com/digitaljohn/comfyui-propost \
    && uv pip install --python /opt/venv -r comfyui-propost/requirements.txt

RUN git clone --depth 1 https://github.com/evanspearman/ComfyMath \
    && uv pip install --python /opt/venv -r ComfyMath/requirements.txt || true

RUN git clone --depth 1 https://github.com/PGCRT/CRT-Nodes \
    && uv pip install --python /opt/venv -r CRT-Nodes/requirements.txt

RUN git clone --depth 1 https://github.com/kijai/ComfyUI-WanAnimatePreprocess \
    && uv pip install --python /opt/venv -r ComfyUI-WanAnimatePreprocess/requirements.txt || true

# ── Opt 8: SageAttention + Triton (uncomment to enable, then re-run test) ────
# RUN pip install triton==3.3.1
# RUN pip install sageattention==2.1.1

# ── Opt 9: TeaCache (uncomment to enable, then re-run test) ──────────────────
# RUN git clone --depth 1 https://github.com/welltop-cn/ComfyUI-TeaCache

WORKDIR /comfyui
EXPOSE 8188
ENTRYPOINT []
CMD ["python", "main.py", "--listen", "0.0.0.0", "--port", "8188"]
