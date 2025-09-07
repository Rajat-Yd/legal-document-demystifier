# Overview

Legal Document Demystifier is a Flask-based web application that transforms complex legal documents into plain, understandable language using AI. Users can upload PDF or TXT legal documents and choose from three actions: simplify the text into plain English, generate a summary, or ask specific questions about the document. The application leverages OpenAI's GPT-5 model to provide intelligent analysis, identifying risks, obligations, and key points in legal documents.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses a traditional server-side rendered architecture with Flask templates and Bootstrap for styling. The frontend consists of:
- **Template Engine**: Jinja2 templates with Bootstrap 5 dark theme for responsive UI
- **Interactive Components**: JavaScript handles action card selection, form validation, and loading states
- **Styling**: Custom CSS animations and Bootstrap components for professional appearance
- **User Flow**: Single-page upload interface that redirects to results page after processing

## Backend Architecture
**Web Framework**: Flask application with modular utility structure
- **Main Application** (`app.py`): Handles routing, file uploads, and user sessions
- **Document Processing** (`utils/document_processor.py`): Extracts text from PDF and TXT files using PyPDF2
- **AI Processing** (`utils/ai_processor.py`): Interfaces with OpenAI API for text analysis

**File Handling**: 
- Temporary file storage in system temp directory
- 16MB file size limit with security validation
- Support for PDF and TXT formats only

**Session Management**:
- Flask sessions with configurable secret key
- Flash messaging for user feedback
- ProxyFix middleware for deployment compatibility

## AI Integration Architecture
**OpenAI Integration**: Direct API calls to GPT-5 model with structured prompts
- **Three Processing Modes**: Simplification, summarization, and question-answering
- **Structured Responses**: JSON format responses for consistent data handling
- **Error Handling**: Comprehensive logging and fallback mechanisms

**Processing Pipeline**:
1. File upload and validation
2. Text extraction based on file type
3. AI processing with role-specific prompts
4. Structured JSON response parsing
5. Results presentation with formatted output

# External Dependencies

## Core Dependencies
- **Flask**: Web framework for routing and templating
- **OpenAI API**: GPT-5 model for legal document analysis and simplification
- **PyPDF2**: PDF text extraction library
- **Werkzeug**: WSGI utilities and secure file handling

## Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme
- **Font Awesome**: Icon library for visual elements
- **Custom JavaScript**: Form interactions and loading states

## Infrastructure Requirements
- **OpenAI API Key**: Required environment variable for AI processing
- **Session Secret**: Configurable environment variable for Flask sessions
- **Temporary Storage**: System temp directory for file processing

## File Processing Limitations
- Maximum file size: 16MB
- Supported formats: PDF, TXT
- Text extraction depends on PDF structure and quality