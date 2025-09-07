import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import tempfile
import traceback

from utils.document_processor import extract_text_from_file
from utils.ai_processor import simplify_legal_text, summarize_document, answer_question

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key_for_hackathon")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        action = request.form.get('action')
        question = request.form.get('question', '').strip()
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        if not allowed_file(file.filename):
            flash('File type not supported. Please upload PDF or TXT files only.', 'error')
            return redirect(url_for('index'))
        
        if not action:
            flash('Please select an action', 'error')
            return redirect(url_for('index'))
        
        if action == 'question' and not question:
            flash('Please enter a question', 'error')
            return redirect(url_for('index'))
        
        # Save uploaded file
        filename = secure_filename(file.filename or '')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from file
        logger.info(f"Extracting text from {filename}")
        document_text = extract_text_from_file(filepath)
        
        if not document_text.strip():
            flash('Could not extract text from the document. Please check if the file is valid.', 'error')
            os.remove(filepath)
            return redirect(url_for('index'))
        
        # Store document text in session for Q&A
        session['document_text'] = document_text
        session['filename'] = filename
        
        # Process based on action
        result = None
        if action == 'simplify':
            logger.info("Simplifying legal text")
            result = simplify_legal_text(document_text)
        elif action == 'summarize':
            logger.info("Summarizing document")
            result = summarize_document(document_text)
        elif action == 'question':
            logger.info(f"Answering question: {question}")
            result = answer_question(document_text, question)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return render_template('results.html', 
                             result=result, 
                             action=action, 
                             filename=filename,
                             question=question if action == 'question' else None)
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        logger.error(traceback.format_exc())
        flash(f'An error occurred while processing your document: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/ask_question', methods=['POST'])
def ask_question():
    try:
        question = request.form.get('question', '').strip()
        document_text = session.get('document_text')
        filename = session.get('filename')
        
        if not question:
            flash('Please enter a question', 'error')
            return redirect(url_for('index'))
        
        if not document_text:
            flash('No document loaded. Please upload a document first.', 'error')
            return redirect(url_for('index'))
        
        logger.info(f"Answering follow-up question: {question}")
        result = answer_question(document_text, question)
        
        return render_template('results.html',
                             result=result,
                             action='question',
                             filename=filename,
                             question=question)
    
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        logger.error(traceback.format_exc())
        flash(f'An error occurred while processing your question: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Please upload a file smaller than 16MB.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
