# 🏥 MedraN - Medical Assistant

A powerful, self-hosted medical AI assistant designed for healthcare professionals and medical students. Features advanced document processing with OCR preprocessing, RAG (Retrieval-Augmented Generation) for medical literature, and multi-modal search functionality tailored for medical documentation and research.

## ✨ Features

### 🏥 Medical-Specific Capabilities
- **📖 Medical Literature Processing**: Optimized for medical journals, research papers, and clinical documentation
- **🔬 Research Assistant**: Query complex medical texts and get contextual answers
- **📋 Clinical Documentation**: Process patient notes, medical reports, and diagnostic imaging reports
- **🎓 Medical Education**: Perfect for medical students and residents studying from textbooks and case studies
- **🔍 Symptom & Treatment Lookup**: Fast retrieval from medical knowledge bases

### 🤖 Core AI Features
- **🔍 Advanced OCR Processing**: Automatically enhances text extraction from medical documents, including scanned medical texts and complex layouts
- **📚 RAG (Retrieval-Augmented Generation)**: Upload medical documents and get contextual, citation-backed answers
- **🧠 Conversation Memory**: Maintains context across medical consultations and study sessions
- **🎙️ Voice Transcription**: Speech-to-text for medical dictation and note-taking (supports WAV, MP3, M4A, FLAC, OGG)
- **🖼️ Multi-modal Search**: Text and image retrieval from medical documents and imaging reports
- **🌐 Web Interface**: Clean, responsive UI designed for healthcare professionals
- **🐳 Docker-First**: Fully containerized for easy deployment in medical environments
- **🏗️ Multi-Architecture**: Builds natively on both AMD64 and ARM64 systems
- **🔧 Self-Hosted**: Complete control over sensitive medical data - fully HIPAA-compliant when properly configured

## 🚀 Quick Start

**The absolute easiest way to get started:**

### 1. Install Docker Desktop
- **Windows/Mac**: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: Follow [official Docker installation guide](https://docs.docker.com/engine/install/)

### 2. Get MedraN
```bash
git clone https://github.com/dralexlup/MedraN-Medical-Assistant.git
cd MedraN-Medical-Assistant
```

### 3. Start MedraN (One Command!) ✨
```bash
./start-medran.sh
```

### 4. Open Your Browser
Visit: **http://localhost:3000** 🎉

---

**That's it!** The startup script handles everything automatically:
- ✅ Checks Docker installation
- ✅ Detects GPU capabilities  
- ✅ Downloads required models
- ✅ Starts all services
- ✅ Provides health checks
- ✅ Opens browser (optional)

### Advanced Usage (Optional)

For manual control, you can still use the traditional commands:

```bash
# 🎆 Smart Docker launcher with automatic GPU detection
./docker-start.sh

# Option A: Use external LLM server (LM Studio, Ollama, etc.)
./docker-start.sh  # Automatically detects GPU and adds appropriate compose files

# Option B: Use containerized LM Studio with Google Gemma 3n-E4B (RECOMMENDED)
./docker-start.sh -f docker-compose.lmstudio.yml

# Manual docker compose (if you prefer):
docker compose up --build -d
```

### Prerequisites (Handled Automatically)
- **Docker** and **Docker Compose** (checked by startup script)
- **8GB+ RAM** recommended for optimal performance
- **NVIDIA Container Toolkit** (auto-detected for GPU acceleration on Linux)
- **Local LLM Server** (LM Studio, Ollama, etc.) OR containerized setup

## 🚀 Smart Docker Launcher

The `./docker-start.sh` script provides intelligent platform and GPU detection with automatic compose file selection:

### ✨ Features
- **🔍 Automatic GPU Detection**: Detects NVIDIA GPUs and NVIDIA Container Toolkit
- **🎯 Smart Compose Files**: Automatically adds appropriate GPU compose files when available
- **🤖 Command Auto-completion**: Adds `up` command when not explicitly provided
- **🎛️ User Control**: Respects user-specified compose files with `-f` flags
- **🌐 Cross-platform**: Works on Linux, macOS, and Windows

### 📖 Usage Examples

```bash
# Basic usage - Auto-detects GPU and starts default services
./docker-start.sh

# Containerized LM Studio - Uses only specified files
./docker-start.sh -f docker-compose.lmstudio.yml

# Multiple compose files - User has full control
./docker-start.sh -f docker-compose.yml -f docker-compose.lmstudio.yml -f docker-compose.gpu.yml

# With explicit docker compose commands
./docker-start.sh ps              # Show running services
./docker-start.sh logs -f api     # Follow API logs
./docker-start.sh down            # Stop all services
```

### 🔧 How it Works

1. **Platform Detection**: Identifies Linux, macOS, or Windows
2. **GPU Detection**: 
   - **Linux**: Checks for `nvidia-smi` and `nvidia-container-runtime`
   - **macOS**: Detects Apple Silicon for MPS support
3. **Compose File Logic**:
   - **No `-f` specified**: Uses `docker-compose.yml` + GPU files if available
   - **User specifies `-f`**: Respects user choice, doesn't auto-add files
4. **Command Handling**: Adds `up` unless explicit command provided (`ps`, `down`, `logs`, etc.)

### 2. Access the System

🚀 **Single Entry Point**: Everything accessible via port 3000!

- **Web UI**: http://localhost:3000/
- **API**: http://localhost:3000/api/...
- **Health Check**: http://localhost:3000/health
- **MinIO Console**: http://localhost:3000/minio-console/ (if needed for storage management)
- **ChromaDB**: http://localhost:3000/chroma/ (optional)

> **Note**: If MinIO console doesn't work perfectly through the proxy, you can enable direct access by temporarily adding `ports: ["9001:9001"]` to the minio service in docker-compose.yml and accessing it at http://localhost:9001

### 3. Upload Documents

1. Open the web UI at http://localhost:3000
2. Click "Upload Document" 
3. Select a PDF file
4. Wait for processing (OCR enhancement will automatically improve text extraction)
5. Start chatting with your documents!

## 🏥 Medical Use Cases

### For Healthcare Professionals
- **📋 Clinical Decision Support**: Upload medical guidelines and get evidence-based recommendations
- **🔬 Research Literature Review**: Process multiple research papers and extract key findings
- **📊 Case Study Analysis**: Upload patient cases and get diagnostic insights
- **💊 Drug Information**: Query pharmaceutical references for dosing, interactions, and contraindications

### For Medical Students & Residents
- **📚 Textbook Study Assistant**: Upload medical textbooks and get interactive Q&A
- **🎯 Exam Preparation**: Practice with case-based questions from your study materials
- **🧠 Concept Clarification**: Get detailed explanations of complex medical concepts
- **📖 Literature Review**: Quickly extract relevant information from research papers

### Example Medical Queries
```
"What are the contraindications for this medication?"
"Summarize the key findings from this clinical trial"
"What are the differential diagnoses for these symptoms?"
"Explain the pathophysiology of this condition"
"What are the current treatment guidelines for this disease?"
```

## 🛠️ Configuration

### Environment Variables

The system uses these key environment variables (configurable in `docker-compose.yml`):

```yaml
# LLM Configuration
OPENAI_BASE_URL: "http://host.docker.internal:1234/v1"  # Your local LLM server
OPENAI_CHAT_MODEL: "your-model-name"                     # Model name from your LLM server

# Model Configuration  
EMBEDDING_MODEL: "bge-m3"                                # Text embedding model
IMAGE_EMBEDDING_MODEL: "clip-ViT-L-14"                  # Image embedding model
OCR_MODEL: "microsoft/trocr-base-printed"               # OCR model for text extraction

# Storage
MINIO_BUCKET: "medrandocs"                              # Document storage bucket
MAX_CONTEXT_CHARS: "120000"                            # Maximum context window
```

### Supported LLM Servers

- **LM Studio**: Default configuration (port 1234)
- **Containerized LM Studio**: Fully self-contained (see below)
- **Ollama**: Change `OPENAI_BASE_URL` to `http://host.docker.internal:11434/v1`
- **OpenAI Compatible APIs**: Any OpenAI-compatible endpoint

### 🐳 Containerized Setup with Google Gemma 3n-E4B (RECOMMENDED)

**NEW**: We now provide a fully containerized setup with Google's latest medical-oriented model!

#### 🩺 Google Gemma 3n-E4B Model Features:
- **6.9B parameters** - Optimized for medical and healthcare tasks
- **Instruction-tuned** - Specifically trained for conversational medical AI
- **Q4_K_M quantization** - Perfect balance of quality and performance (3.95GB)
- **Automatic download** - No manual model management required
- **Cross-platform** - Works on macOS (Apple Silicon + Intel), Linux (ARM64 + x86_64)

#### 🚀 One-Command Setup:
```bash
git clone https://github.com/dralexlup/MedraN-Medical-Assistant.git
cd MedraN-Medical-Assistant

# Start everything with Google Gemma 3n-E4B model
docker-compose -f docker-compose.lmstudio.yml up --build -d

# Access at http://localhost:3000 - that's it! 🎉
```

#### ✨ What Happens Automatically:
1. **Builds optimized llama.cpp** with CMake for your platform
2. **Downloads Google Gemma 3n-E4B** model (first startup only)
3. **Starts all services** with proper health checks and dependencies
4. **Ready in ~5 minutes** - fully plug-and-play experience

#### 💻 Platform Support:
- ✅ **macOS Apple Silicon** (M1/M2/M3) - CPU optimized
- ✅ **macOS Intel** - CPU optimized  
- ✅ **Linux ARM64** - CPU optimized
- ✅ **Linux x86_64** - CPU + GPU optimized (CUDA support with auto-detection)
- ✅ **Windows** - Via Docker Desktop

#### 🔧 Benefits:
- ✅ **No external dependencies** - Everything containerized
- ✅ **Medical AI optimized** - Google Gemma 3n-E4B excels at healthcare tasks
- ✅ **Plug-and-play setup** - No manual configuration
- ✅ **Persistent storage** - Models downloaded once, kept forever
- ✅ **Health monitoring** - Automatic container health checks
- ✅ **Production ready** - Robust, scalable architecture

### 🐳 Custom Model Setup (Advanced)

If you prefer to use your own GGUF model:

1. **Place your model**:
   ```bash
   # Create models directory and add your GGUF model
   mkdir -p models
   cp your-model.gguf models/model.gguf
   ```

2. **Start with custom model**:
   ```bash
   docker-compose -f docker-compose.lmstudio.yml up --build -d
   ```

3. **Access the system**: http://localhost:3000

## 📋 API Endpoints

### Core Functionality

- `GET /api/healthz` - Health check
- `POST /api/ingest` - Upload and process documents (with OCR enhancement)
- `POST /api/chat` - Chat with your knowledge base
- `POST /api/transcribe` - Voice-to-text transcription
- `GET /health` - System health check (reverse proxy)

### Example Usage

```bash
# Health check
curl http://localhost:3000/health
curl http://localhost:3000/api/healthz

# Upload a document
curl -X POST "http://localhost:3000/api/ingest" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F "title=My Document"

# Chat with the document
curl -X POST "http://localhost:3000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main topics covered?",
    "user_id": "user123",
    "k": 6,
    "return_images": true,
    "remember": true
  }'
```

## 🏗️ Architecture

```
                    ┌─────────────────┐
                    │ Nginx Proxy     │ ←── Single Entry Point
                    │ (Port 3000)     │     http://localhost:3000
                    └─────────┬───────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
    ┌─────────────────┐ ┌──────────────┐ ┌─────────────────┐
    │   Web UI        │ │   FastAPI    │ │   LLM Server    │
    │   (Internal)    │ │ (Internal)   │ │   (Port 1234)   │
    └─────────────────┘ └──────┬───────┘ └─────────────────┘
                               │
                   ┌───────────┼───────────┐
                   │           │           │
           ┌───────▼────┐ ┌────▼────┐ ┌───▼──────┐
           │  ChromaDB  │ │  Redis  │ │  MinIO   │
           │ (Internal) │ │(Internal)│ │(Internal)│
           └────────────┘ └─────────┘ └──────────┘
```

## 🔧 Advanced Configuration

### Custom Models

You can customize the models by editing `docker-compose.yml`:

```yaml
environment:
  EMBEDDING_MODEL: "your-preferred-embedding-model"
  OCR_MODEL: "your-preferred-ocr-model"
  IMAGE_EMBEDDING_MODEL: "your-preferred-image-model"
```

### Resource Requirements

- **Minimal**: 2GB RAM, 2 CPU cores
- **Recommended**: 4GB RAM, 4 CPU cores
- **Production**: 8GB+ RAM, 8+ CPU cores

### GPU Support

The system **automatically detects and uses GPU acceleration** when available:
- **CUDA GPUs**: Automatically detected for NVIDIA cards
- **Apple Silicon (MPS)**: Automatically detected for M1/M2/M3 Macs
- **CPU Fallback**: Uses CPU when no GPU is available

For Docker GPU access (NVIDIA only), add to your `docker-compose.yml`:

```yaml
api:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

**Note**: Apple Silicon GPU support works automatically without Docker configuration.

## 🐛 Troubleshooting

### Common Issues

1. **"Cannot connect to LLM server" (httpx.ConnectError)**
   - Ensure LM Studio is running and **"Allow network access"** is enabled
   - Verify the model is loaded in LM Studio
   - Check that LM Studio is running on port 1234
   - On Linux: Use your host IP instead of `host.docker.internal`

2. **"CLIPConfig object has no attribute 'hidden_size'"**
   - This is fixed in the latest version with updated CLIP model
   - If still occurring, try: `docker compose down && docker compose up --build`

3. **Large file upload failures**
   - The system now supports uploads up to 500MB
   - Files that timeout during upload may need LM Studio to be started first

4. **Out of memory during model loading**
   - Increase Docker memory limits to 4GB+
   - GPU acceleration reduces memory usage significantly

5. **Slow document processing**
   - GPU acceleration now automatic when available
   - OCR processing is CPU-intensive on CPU-only systems

6. **"Embedding dimension X does not match collection dimensionality Y" error**
   - This occurs when switching between different embedding models
   - **Automatic fix**: The startup script asks if you want to reset collections
   - **Manual fix**: Run the collection clearing utility:
     ```bash
     # Start services first
     ./docker-start.sh
     
     # Clear collections
     docker exec -it medran-api python clear_collections.py
     
     # Restart API
     docker restart medran-api
     ```

7. **Docker-start.sh script issues**
   - **"NVIDIA Docker runtime not detected"**: Install `nvidia-container-toolkit` package
   - **"Usage: docker compose [OPTIONS] COMMAND"**: Use the fixed version with automatic `up` command
   - **"service has neither an image nor a build context"**: Make sure to specify compose files correctly with `-f`
   - **Permission denied**: Add your user to the `docker` group: `sudo usermod -aG docker $USER`

### Logs

```bash
# View all service logs
docker compose logs -f

# View specific service logs  
docker compose logs -f api
docker compose logs -f chroma
```

## 📊 Performance

### OCR Enhancement

The system automatically uses OCR when it detects that it can significantly improve text extraction:

- **Smart Enhancement**: Only uses OCR when beneficial (20%+ text improvement)
- **Fallback**: Works without OCR if models fail to load
- **Logging**: Monitor OCR usage via API logs

### Benchmarks

On a modern system (M1 MacBook Pro):
- **Document Ingestion**: ~2-3 pages/second with OCR
- **Query Response**: ~500ms average
- **Memory Usage**: ~1.5GB per service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `docker compose up --build`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Issues**: Create an issue on GitHub
- **Documentation**: Check `DEPLOYMENT.md` for advanced deployment options
- **Community**: Join discussions in GitHub Discussions

## 🎯 Roadmap

- [ ] Web UI improvements and dark mode
- [ ] Support for more document formats (DOCX, TXT, etc.)
- [ ] Advanced OCR models (table extraction, formula recognition)
- [ ] Multi-language support
- [ ] Plugin system for custom tools
- [ ] Cloud deployment templates (AWS, GCP, Azure)

---

**Made with ❤️ for the open-source community**

*Self-hosted AI that respects your privacy and gives you full control over your data.*
