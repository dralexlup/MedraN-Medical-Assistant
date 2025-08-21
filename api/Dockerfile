# Use NVIDIA CUDA runtime for GPU acceleration
FROM nvidia/cuda:12.9.0-runtime-ubuntu22.04

# Install Python 3.10 (default for Ubuntu 22.04)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip

# system deps for PDF/image parsing and OCR model
RUN apt-get update && apt-get install -y \
    poppler-utils libgl1 libglib2.0-0 tesseract-ocr ffmpeg \
    git curl wget build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
# Install PyTorch with CUDA support first
RUN pip install --no-cache-dir torch==2.6.0+cu124 torchvision --index-url https://download.pytorch.org/whl/cu124

# Install other requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
