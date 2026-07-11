FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# The prebuilt CPU wheel index tops out at 0.2.62, which predates full
# Qwen2 architecture support in llama.cpp and segfaults on inference
# (verified empirically - loads fine, crashes on first generate call).
# Compile a current version from source instead.
RUN apt-get update && apt-get install -y --no-install-recommends build-essential cmake \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir llama-cpp-python

COPY router/ ./router/
COPY main.py .
COPY models/ ./models/

# The harness mounts /input and /output; ensure they exist so a missing
# mount doesn't crash us before we even read the tasks file.
RUN mkdir -p /input /output

ENTRYPOINT ["python", "main.py"]
