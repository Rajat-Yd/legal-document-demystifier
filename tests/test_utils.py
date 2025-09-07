import pytest
import tempfile
import os
from utils.document_processor import (
    extract_text_from_file, 
    extract_text_from_txt, 
    validate_document_content,
    truncate_text_for_api
)

def test_extract_text_from_txt():
    """Test text extraction from TXT file"""
    # Create a temporary text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is a test legal document with some content.")
        temp_path = f.name
    
    try:
        text = extract_text_from_txt(temp_path)
        assert "This is a test legal document" in text
        assert len(text.strip()) > 0
    finally:
        os.unlink(temp_path)

def test_validate_document_content():
    """Test document content validation"""
    # Valid content
    valid_text = "This is a legal document with sufficient content for processing. " * 10
    assert validate_document_content(valid_text) == True
    
    # Invalid content (too short)
    invalid_text = "Short"
    assert validate_document_content(invalid_text) == False
    
    # Empty content
    assert validate_document_content("") == False
    assert validate_document_content(None) == False

def test_truncate_text_for_api():
    """Test text truncation for API limits"""
    # Short text should remain unchanged
    short_text = "This is a short document."
    result = truncate_text_for_api(short_text, max_tokens=1000)
    assert result == short_text
    
    # Long text should be truncated
    long_text = "This is a very long document. " * 1000
    result = truncate_text_for_api(long_text, max_tokens=100)
    assert len(result) < len(long_text)
    assert "[Note: Document was truncated due to length limits]" in result

def test_extract_text_from_unsupported_file():
    """Test extraction from unsupported file type"""
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as f:
        temp_path = f.name
    
    try:
        with pytest.raises(Exception) as exc_info:
            extract_text_from_file(temp_path)
        assert "Unsupported file type" in str(exc_info.value)
    finally:
        os.unlink(temp_path)