import pytest
import os
import tempfile
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_index_page(client):
    """Test that the main page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Legal Document Demystifier' in response.data
    assert b'Upload Your Legal Document' in response.data

def test_upload_without_file(client):
    """Test upload endpoint without file"""
    response = client.post('/upload', data={
        'action': 'simplify'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'No file selected' in response.data

def test_upload_invalid_file_type(client):
    """Test upload with invalid file type"""
    data = {
        'file': (tempfile.NamedTemporaryFile(suffix='.doc'), 'test.doc'),
        'action': 'simplify'
    }
    response = client.post('/upload', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'File type not supported' in response.data

def test_upload_without_action(client):
    """Test upload without selecting an action"""
    data = {
        'file': (tempfile.NamedTemporaryFile(suffix='.txt'), 'test.txt')
    }
    response = client.post('/upload', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Please select an action' in response.data

def test_question_action_without_question(client):
    """Test Q&A action without providing a question"""
    data = {
        'file': (tempfile.NamedTemporaryFile(suffix='.txt'), 'test.txt'),
        'action': 'question',
        'question': ''
    }
    response = client.post('/upload', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Please enter a question' in response.data

def test_ask_question_without_document(client):
    """Test asking question without uploaded document"""
    response = client.post('/ask_question', data={
        'question': 'What is this about?'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'No document loaded' in response.data

def test_file_too_large_handler(client):
    """Test file size limit error handler"""
    # This tests the error handler function
    with app.test_request_context():
        from werkzeug.exceptions import RequestEntityTooLarge
        error = RequestEntityTooLarge()
        response = app.handle_http_exception(error)
        # The handler should redirect, so we expect a 302 status code
        assert response.status_code == 302