# Antigravity AI: Autonomous Coaching Ecosystem 🚀🤖

![Project Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-009688)
![React](https://img.shields.io/badge/React-Vite-61DAFB)
![License](https://img.shields.io/badge/License-MIT-green)

> **A Full-Stack AI Automation Platform specialized for High-Ticket Coaching Businesses.**
> Integrates Multi-Agent Systems, RAG (Retrieval Augmented Generation), and Video Processing into a unified dashboard.

---

## 🌟 Features / Modules

### 🧠 Module A: AI Speaker Sourcing
*   **Automated Scraping**: Monitors Podcast RSS feeds for new episodes.
*   **Guest Analysis**: Uses LLMs (`GPT-4o` / `Groq Llama 3`) to extract guest bio, relevance, and contact info.
*   **Outreach**: Generates hyper-personalized invitation emails automatically.

### 🤖 Module B: The AI Coach (RAG)
*   **Knowledge Base**: Ingests PDFs, Transcripts, and Manuals.
*   **Semantic Search**: Uses Vector Database (`ChromaDB`) to retrieve context.
*   **Chat Interface**: Conversational agent that answers client questions 24/7 based on your proprietary methods.

### 🎬 Module C: Viral Content Engine
*   **Video Processing**: Drag & drop long-form interviews.
*   **AI Clipping**: Automatically identifies "viral moments" based on sentiment and hook strength.
*   **FFmpeg Integration**: physically cuts and exports the MP4 clip ready for TikTok/Reels.

### 📧 Module D: Cold Outreach & CRM
*   **Campaigns**: Manage multi-step email sequences (Email 1 -> Wait -> Follow-up).
*   **CRM Agent**: Listens to webhooks (e.g., from GoHighLevel), analyzes sales call notes, and triggers follow-up tasks.

### 🖥️ Module F: Premium Dashboard
*   **React + Vite**: A modern, high-performance Single Page Application.
*   **Dark Mode UI**: Glassmorphism design for a premium user experience.

### 📱 Module G: Digital Twin API
*   **WhatsApp/Telegram**: Exposes a simplified API endpoint for connecting Chatbots that mimic your coaching style.

---

## 🛠️ Tech Stack

*   **Backend**: Python, FastAPI, SQLModel (SQLite), Pydantic.
*   **Frontend**: React, Vite, Framer Motion, Axios.
*   **AI/ML**: OpenAI API (GPT-4o), Groq API (Llama 3 / Mixtral), ChromaDB (Vector Store).
*   **Media**: FFmpeg, OpenAI Whisper.

---

## ⚡ Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/surbalo1/ai-coaching-system.git
cd ai-coaching-system

# Create .env file
cp .env.example .env
# Add your Keys: OPENAI_API_KEY=gsk_...
```

### 2. Run Backend (The Brain)
```bash
python3 -m uvicorn app.main:app --reload
```
*API Documentation available at: `http://localhost:8000/docs`*

### 3. Run Frontend (The Face)
```bash
cd frontend
npm install
npm run dev
```
*Access the Dashboard at: `http://localhost:5173`*

---

## 🏷️ Hashtags & Topics
#python #fastapi #react #ai-agents #automation #rag #openai #groq-api #software-architecture #saas #coaching-business #crm-automation #fullstack #portfolio

---

**Created by [surbalo1](https://github.com/surbalo1)**
