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

- **Flask** - Python web framework
- **Google Gemini AI** - Advanced document analysis
- **Bootstrap 5** - Responsive dark theme UI
- **PyPDF2** - PDF text extraction
- **Gunicorn** - Production WSGI server

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
# OR using the project's package manager
uv sync
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

4. **Run the application**
```bash
# Development server
python app.py

# Production server with Gunicorn
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `SESSION_SECRET`: Flask session secret (optional)

## 📁 Project Structure
```
legal-document-demystifier/
├── app.py                 # Main Flask web application
├── main.py               # WSGI entry point for deployment
├── utils/
│   ├── document_processor.py  # PDF/TXT text extraction
│   └── ai_processor.py        # Gemini AI integration
├── templates/
│   ├── index.html        # Upload and action selection page
│   └── results.html      # Analysis results display
├── static/
│   ├── style.css         # Custom styles and animations
│   └── script.js         # Frontend interactions
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
└── pyproject.toml       # Project dependencies
```

## 🔒 Security Note
Never commit your API keys to version control. Always use environment variables and keep your `.env` file private.