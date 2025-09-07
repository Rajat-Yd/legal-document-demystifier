---
title: Legal Document Demystifier
emoji: ⚖️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app_hf.py
pinned: false
license: mit
---

# Legal Document Demystifier

A GenAI-powered web application that transforms complex legal documents into plain, understandable language. Built for the "Demystifying Legal Documents" hackathon challenge.

## Features

- **Simplify**: Convert complex legal language into plain English
- **Summarize**: Generate executive summaries with key risks and obligations
- **Q&A**: Ask specific questions about legal documents
- **Risk Detection**: Automatically identify potential risks and red flags
- **Hidden Clauses**: Highlight important clauses that are easy to miss

## How to Use

1. Upload a PDF or TXT legal document (up to 16MB)
2. Choose your action: Simplify, Summarize, or Ask a Question
3. Get instant AI-powered analysis

## Technology Stack

- Flask web framework
- Google Gemini AI for document analysis
- Bootstrap for responsive UI
- PyPDF2 for document processing

Built with ❤️ for making legal documents accessible to everyone.

## 🚀 Local Development Setup

### Prerequisites
- Python 3.11+
- Gemini API Key (free from [Google AI Studio](https://ai.google.dev/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/legal-document-demystifier.git
cd legal-document-demystifier
```

2. **Install dependencies**
```bash
pip install flask gunicorn google-genai pypdf2 werkzeug
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

4. **Run the application**
```bash
# For Flask version
python app.py

# For Gradio version (Hugging Face Spaces)
python app_hf.py

# For production with Gunicorn
gunicorn --bind 0.0.0.0:5000 main:app
```

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `SESSION_SECRET`: Flask session secret (optional)

## 📁 Project Structure
```
legal-document-demystifier/
├── app.py                 # Flask web application
├── app_hf.py             # Gradio version for HF Spaces
├── main.py               # WSGI entry point
├── utils/
│   ├── document_processor.py  # PDF/TXT text extraction
│   └── ai_processor.py        # Gemini AI integration
├── templates/            # HTML templates
├── static/              # CSS, JS, assets
└── .env.example         # Environment variables template
```

## 🔒 Security Note
Never commit your API keys to version control. Always use environment variables and keep your `.env` file private.