# 📝 Meeting Minutes Generator (LangGraph + OpenAI)

A production-style LangGraph workflow that analyzes meeting notes or audio recordings and automatically generates:

- 👥 Participants list  
- 📌 Main discussion topics  
- ✅ Action items (with responsible person when available)  
- 📄 Formal meeting minutes  
- 💡 Executive summary  

The system supports both text input and audio/video transcription using OpenAI Whisper.

---

## 🚀 Features

- Built using **LangGraph**
- Uses **OpenAI GPT models** for structured analysis
- Supports **audio/video transcription** via Whisper API
- Clean state-based workflow architecture
- Modular node-based processing
- No API keys stored in the repository

---

## 🏗️ Architecture

The workflow is built as a LangGraph state machine:

START
↓
Participants Extraction
↓
Topics Identification
↓
Action Items Extraction
↓
Minutes Generation
↓
Executive Summary
↓
END


Each node updates a shared structured state.

---

## 📦 Requirements

- Python 3.10+
- OpenAI API Key

Install dependencies:

```bash
pip install -r requirements.txt
