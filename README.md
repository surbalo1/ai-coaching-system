<div align="center">

# 🚀 Autonomous AI Coaching Ecosystem

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![OpenAI](https://img.shields.io/badge/GPT--4-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**A full-stack AI automation platform for high-ticket coaching businesses.**

*Multi-agent systems • RAG knowledge base • Video processing • CRM automation*

</div>

---

## 📋 Overview

A comprehensive AI ecosystem that combines multi-agent systems, RAG (Retrieval Augmented Generation), and video processing into a unified dashboard. Designed specifically for coaches, consultants, and course creators who want to scale their business with AI automation.

---

## 🌟 Modules

<div align="center">

| Module | Name | Description |
|:------:|------|-------------|
| 🧠 **A** | Speaker Sourcing | Automated podcast scraping & guest outreach |
| 🤖 **B** | AI Coach (RAG) | 24/7 conversational agent with knowledge base |
| 🎬 **C** | Content Engine | Viral clip detection & video processing |
| 📧 **D** | Outreach & CRM | Multi-step campaigns & webhook automation |
| 🖥️ **F** | Dashboard | Premium React UI with dark mode |
| 📱 **G** | Digital Twin | WhatsApp/Telegram chatbot API |

</div>

---

## 🏗️ System Architecture

```mermaid
flowchart TB
    subgraph Frontend["🖥️ Frontend (React + Vite)"]
        UI[Premium Dashboard]
        DM[Dark Mode UI]
    end

    subgraph Backend["⚙️ Backend (FastAPI)"]
        API[REST API]
        DB[(SQLite DB)]
    end

    subgraph Modules["🧠 AI Modules"]
        RSS[RSS Scraper]
        RAG[RAG Engine]
        VIDEO[Video Processor]
        CRM[CRM Agent]
        TWIN[Digital Twin]
    end

    subgraph AI["🤖 AI Services"]
        GPT[OpenAI GPT-4]
        GROQ[Groq Llama 3]
        CHROMA[(ChromaDB)]
        WHISPER[Whisper]
        FFMPEG[FFmpeg]
    end

    UI <--> API
    API <--> DB
    API <--> RSS
    API <--> RAG
    API <--> VIDEO
    API <--> CRM
    API <--> TWIN

    RSS --> GPT
    RAG --> CHROMA
    RAG --> GPT
    VIDEO --> WHISPER
    VIDEO --> FFMPEG
    CRM --> GPT
    TWIN --> GROQ
```

---

## ✨ Module Details

### 🧠 Module A: AI Speaker Sourcing

| Feature | Description |
|---------|-------------|
| **RSS Monitoring** | Automated scraping of podcast feeds |
| **Guest Analysis** | LLM-powered bio extraction & relevance scoring |
| **Outreach** | Hyper-personalized invitation emails |

### 🤖 Module B: AI Coach (RAG)

| Feature | Description |
|---------|-------------|
| **Knowledge Ingestion** | PDFs, transcripts, manuals |
| **Semantic Search** | ChromaDB vector database |
| **24/7 Chat** | Conversational agent for client Q&A |

### 🎬 Module C: Viral Content Engine

| Feature | Description |
|---------|-------------|
| **Video Upload** | Drag & drop long-form content |
| **AI Clipping** | Identifies viral moments via sentiment analysis |
| **Export** | FFmpeg cuts ready for TikTok/Reels |

### 📧 Module D: CRM & Outreach

| Feature | Description |
|---------|-------------|
| **Email Sequences** | Multi-step campaigns with delays |
| **Webhook Listener** | GoHighLevel integration |
| **Follow-up Automation** | AI-triggered task creation |

### 📱 Module G: Digital Twin API

| Feature | Description |
|---------|-------------|
| **Chatbot API** | WhatsApp/Telegram endpoint |
| **Style Mimicking** | Replicates your coaching voice |

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technologies |
|-------|--------------|
| **Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white) |
| **Frontend** | ![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black) ![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white) ![Framer](https://img.shields.io/badge/Framer_Motion-0055FF?style=flat-square&logo=framer&logoColor=white) |
| **AI/ML** | ![OpenAI](https://img.shields.io/badge/GPT--4o-412991?style=flat-square&logo=openai&logoColor=white) ![Groq](https://img.shields.io/badge/Llama_3-FF6B35?style=flat-square) ![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6B6B?style=flat-square) |
| **Media** | ![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?style=flat-square&logo=ffmpeg&logoColor=white) ![Whisper](https://img.shields.io/badge/Whisper-412991?style=flat-square&logo=openai&logoColor=white) |

</div>

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- API Keys: OpenAI, Groq (optional)

### 1️⃣ Clone & Setup

```bash
git clone https://github.com/surbalo1/ai-coaching-system.git
cd ai-coaching-system

# Create environment file
cp .env.example .env
# Add your keys: OPENAI_API_KEY=sk-...
```

### 2️⃣ Run Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python3 -m uvicorn app.main:app --reload
```

📍 **API Docs:** http://localhost:8000/docs

### 3️⃣ Run Frontend

```bash
cd frontend
npm install
npm run dev
```

📍 **Dashboard:** http://localhost:5173

---

## 📁 Project Structure

```
ai-coaching-system/
├── 🐍 app/                    # FastAPI backend
│   ├── main.py                # Entry point
│   ├── routers/               # API endpoints
│   ├── services/              # Business logic
│   └── models/                # Data models
│
├── ⚛️ frontend/               # React + Vite
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── pages/             # Route pages
│   │   └── services/          # API client
│   └── package.json
│
├── 📁 data/                   # Knowledge base files
├── 🗄️ database.db             # SQLite database
├── 📄 requirements.txt        # Python dependencies
└── 📄 .env.example            # Environment template
```

---

## 🔧 Verification Scripts

Test each module independently:

```bash
python verify_rss.py      # RSS scraping
python verify_rag.py      # RAG knowledge base
python verify_crm.py      # CRM integration
python verify_twin.py     # Digital twin API
python verify_outreach.py # Email outreach
python verify_full.py     # Full system test
```

---

## 💡 Use Cases

- **Coaches** - Automate client onboarding & Q&A
- **Course Creators** - 24/7 student support
- **Consultants** - Scale outreach & lead nurturing
- **Podcasters** - Guest sourcing & content repurposing

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

<div align="center">

**Built with ❤️ for coaches & creators**

[![GitHub](https://img.shields.io/badge/Star_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/surbalo1/ai-coaching-system)

</div>
