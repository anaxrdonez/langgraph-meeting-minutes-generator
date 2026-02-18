# 📝 Meeting Minutes Generator (LangGraph + OpenAI)

A production-style LangGraph workflow that analyzes meeting notes or
audio recordings and automatically generates structured outputs
including participants, discussion topics, action items, formal minutes,
and an executive summary.

The system supports both text input and audio/video transcription using
the OpenAI Whisper API.

------------------------------------------------------------------------

## 🚀 Features

-   Built with **LangGraph** (state-driven workflow architecture)
-   Uses **OpenAI GPT models** for structured analysis and text
    generation
-   Supports **audio/video transcription** via Whisper API
-   Clean state-based processing pipeline
-   Modular node-based design
-   Environment variable--based authentication (no API keys stored in
    the repo)

------------------------------------------------------------------------

## 🏗️ Architecture

The workflow is implemented as a LangGraph state machine:

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

Each node updates a shared structured state using a `TypedDict` model.

------------------------------------------------------------------------

## 📦 Requirements

-   Python 3.10+
-   OpenAI API Key

Install dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🔐 Environment Variables

This project requires the following environment variable:

    OPENAI_API_KEY=your_openai_api_key

Set it in your system environment variables before running the
application.

### Windows (PowerShell example)

``` powershell
setx OPENAI_API_KEY "your_api_key_here"
```

Restart your terminal after setting it.

⚠️ Do not hardcode API keys in the source code.\
⚠️ Never commit secrets to version control.

------------------------------------------------------------------------

## ▶️ How to Run

``` bash
python main.py
```

A file picker will open. You can select:

-   Text files (`.txt`, `.md`)
-   Audio/video files (`.mp4`, `.mp3`, `.wav`, `.mov`, etc.)

The system will:

1.  Transcribe audio (if applicable)
2.  Extract structured meeting information
3.  Generate formal minutes
4.  Produce a concise executive summary
5.  Display results in the terminal

------------------------------------------------------------------------

## 📄 Output Overview

The application produces:

-   Structured list of participants\
-   Key discussion topics\
-   Clear action items (with responsible person when mentioned)\
-   Formal meeting minutes (maximum \~150 words)\
-   Two-line executive summary (maximum \~30 words)

------------------------------------------------------------------------

## 🧠 Technologies Used

-   LangGraph\
-   LangChain OpenAI\
-   OpenAI GPT-4o-mini\
-   OpenAI Whisper API\
-   Python (TypedDict state modeling)

------------------------------------------------------------------------

## 🛡️ Security Notes

-   API keys are read from environment variables only.
-   `.gitignore` excludes virtual environments and sensitive files.
-   No secrets are stored in this repository.
-   Always revoke keys immediately if accidentally exposed.

------------------------------------------------------------------------

## 📌 Future Improvements

-   Web interface (Streamlit or FastAPI)
-   Structured JSON output mode
-   Persistent meeting storage (database integration)
-   Automatic PDF export of minutes
-   Multi-language support
-   Docker containerization
-   Unit and integration tests

------------------------------------------------------------------------

## 📜 License

This project is open-source and intended for educational and portfolio
purposes.