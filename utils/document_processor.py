import os
import logging
from typing import Optional
import PyPDF2
import io

logger = logging.getLogger(__name__)

def extract_text_from_file(filepath: str) -> str:
    """
    Extract text content from uploaded file (PDF or TXT).
    
    Args:
        filepath: Path to the uploaded file
        
    Returns:
        str: Extracted text content
        
    Raises:
        Exception: If file processing fails
    """
    try:
        file_extension = os.path.splitext(filepath)[1].lower()
        
        if file_extension == '.pdf':
            return extract_text_from_pdf(filepath)
        elif file_extension == '.txt':
            return extract_text_from_txt(filepath)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
            
    except Exception as e:
        logger.error(f"Error extracting text from {filepath}: {str(e)}")
        raise Exception(f"Failed to extract text from document: {str(e)}")

def extract_text_from_pdf(filepath: str) -> str:
    """
    Extract text from PDF file.
    
    Args:
        filepath: Path to the PDF file
        
    Returns:
        str: Extracted text content
    """
    try:
        text_content = ""
        
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract text from all pages
            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        text_content += f"\n--- Page {page_num} ---\n"
                        text_content += page_text + "\n"
                except Exception as e:
                    logger.warning(f"Could not extract text from page {page_num}: {str(e)}")
                    continue
        
        if not text_content.strip():
            raise Exception("No readable text found in PDF. The document might be image-based or corrupted.")
        
        return text_content.strip()
        
    except Exception as e:
        logger.error(f"Error processing PDF {filepath}: {str(e)}")
        raise Exception(f"Failed to process PDF file: {str(e)}")

def extract_text_from_txt(filepath: str) -> str:
    """
    Extract text from TXT file.
    
    Args:
        filepath: Path to the TXT file
        
    Returns:
        str: File content
    """
    try:
        # Try different encodings
        encodings = ['utf-8', 'utf-16', 'latin-1', 'ascii']
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as file:
                    content = file.read()
                    if content.strip():
                        return content.strip()
            except UnicodeDecodeError:
                continue
        
        raise Exception("Could not decode text file with any supported encoding")
        
    except Exception as e:
        logger.error(f"Error processing TXT {filepath}: {str(e)}")
        raise Exception(f"Failed to process text file: {str(e)}")

def validate_document_content(text: str) -> bool:
    """
    Validate that the extracted text contains meaningful content.
    
    Args:
        text: Extracted text content
        
    Returns:
        bool: True if content appears valid
    """
    if not text or not text.strip():
        return False
    
    # Check minimum length
    if len(text.strip()) < 50:
        return False
    
    # Check for meaningful words (basic heuristic)
    words = text.split()
    if len(words) < 10:
        return False
    
    return True

def truncate_text_for_api(text: str, max_tokens: int = 15000) -> str:
    """
    Truncate text to fit within API token limits.
    Rough estimate: 1 token ≈ 4 characters
    
    Args:
        text: Input text
        max_tokens: Maximum number of tokens allowed
        
    Returns:
        str: Truncated text
    """
    max_chars = max_tokens * 4
    
    if len(text) <= max_chars:
        return text
    
    # Truncate at word boundary
    truncated = text[:max_chars]
    last_space = truncated.rfind(' ')
    
    if last_space > max_chars * 0.8:  # If we found a space in the last 20%
        truncated = truncated[:last_space]
    
    return truncated + "\n\n[Note: Document was truncated due to length limits]"
