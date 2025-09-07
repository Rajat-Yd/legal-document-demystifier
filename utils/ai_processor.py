import os
import json
import logging
from typing import Dict, List, Any, Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

def simplify_legal_text(document_text: str) -> Dict[str, Any]:
    """
    Simplify legal document text into plain language.
    
    Args:
        document_text: Raw legal document text
        
    Returns:
        Dict containing simplified text, risks, obligations, and key points
    """
    try:
        prompt = f"""
        You are a legal expert specializing in translating complex legal documents into plain, understandable language.
        
        Please analyze the following legal document and provide:
        1. A simplified version that explains the content in plain English
        2. Identify key risks and red flags
        3. List important obligations and responsibilities
        4. Highlight key points that need attention
        
        Document to analyze:
        {document_text}
        
        Please respond in JSON format with these fields:
        {{
            "simplified_text": "Plain language explanation of the document",
            "risks": ["List of identified risks and red flags"],
            "obligations": ["List of obligations and responsibilities"],
            "key_points": ["List of important points to note"]
        }}
        """
        
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are a legal expert who specializes in making complex legal documents understandable to everyday people. Always respond in JSON format."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=3000
        )
        
        result = json.loads(response.choices[0].message.content or '{}')
        
        # Format the simplified text with proper HTML formatting
        if result.get('simplified_text'):
            result['simplified_text'] = format_text_with_paragraphs(result['simplified_text'])
        
        return result
        
    except Exception as e:
        logger.error(f"Error simplifying legal text: {str(e)}")
        return {
            "error": f"Failed to simplify document: {str(e)}",
            "simplified_text": None,
            "risks": [],
            "obligations": [],
            "key_points": []
        }

def summarize_document(document_text: str) -> Dict[str, Any]:
    """
    Generate an executive summary of the legal document.
    
    Args:
        document_text: Raw legal document text
        
    Returns:
        Dict containing summary, risks, obligations, and key points
    """
    try:
        prompt = f"""
        You are a legal analyst creating executive summaries for business leaders.
        
        Please analyze the following legal document and provide:
        1. A concise executive summary (3-5 paragraphs max)
        2. Critical risks that need immediate attention
        3. Key obligations and deadlines
        4. Important clauses and terms
        
        Focus on what a business executive needs to know to make informed decisions.
        
        Document to analyze:
        {document_text}
        
        Please respond in JSON format with these fields:
        {{
            "summary": "Executive summary of the document",
            "risks": ["List of critical risks"],
            "obligations": ["List of key obligations and deadlines"],
            "key_points": ["List of important clauses and terms"]
        }}
        """
        
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior legal analyst who creates executive summaries for C-level executives. Focus on business impact and decision-making insights. Always respond in JSON format."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=2500
        )
        
        result = json.loads(response.choices[0].message.content or '{}')
        
        # Format the summary with proper HTML formatting
        if result.get('summary'):
            result['summary'] = format_text_with_paragraphs(result['summary'])
        
        return result
        
    except Exception as e:
        logger.error(f"Error summarizing document: {str(e)}")
        return {
            "error": f"Failed to summarize document: {str(e)}",
            "summary": None,
            "risks": [],
            "obligations": [],
            "key_points": []
        }

def answer_question(document_text: str, question: str) -> Dict[str, Any]:
    """
    Answer specific questions about the legal document.
    
    Args:
        document_text: Raw legal document text
        question: User's question about the document
        
    Returns:
        Dict containing the answer and related information
    """
    try:
        prompt = f"""
        You are a legal expert answering questions about a specific legal document.
        
        Document:
        {document_text}
        
        Question: {question}
        
        Please provide a comprehensive answer that:
        1. Directly addresses the question
        2. References specific sections or clauses if relevant
        3. Explains any legal implications
        4. Identifies related risks or considerations
        5. Suggests next steps if applicable
        
        Please respond in JSON format with these fields:
        {{
            "answer": "Comprehensive answer to the question",
            "relevant_clauses": ["List of relevant document sections or clauses"],
            "risks": ["Any risks related to this question"],
            "recommendations": ["Suggested actions or considerations"]
        }}
        """
        
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior legal counsel providing detailed answers about legal documents. Be thorough, accurate, and practical in your responses. Always respond in JSON format."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=2000
        )
        
        result = json.loads(response.choices[0].message.content or '{}')
        
        # Format the answer with proper HTML formatting
        if result.get('answer'):
            result['answer'] = format_text_with_paragraphs(result['answer'])
        
        return result
        
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        return {
            "error": f"Failed to answer question: {str(e)}",
            "answer": None,
            "relevant_clauses": [],
            "risks": [],
            "recommendations": []
        }

def format_text_with_paragraphs(text: str) -> str:
    """
    Format text with proper HTML paragraph tags for better display.
    
    Args:
        text: Raw text content
        
    Returns:
        str: HTML formatted text
    """
    if not text:
        return ""
    
    # Split text into paragraphs and wrap each in <p> tags
    paragraphs = text.split('\n\n')
    formatted_paragraphs = []
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph:
            # Handle bullet points
            if paragraph.startswith('- ') or paragraph.startswith('• '):
                lines = paragraph.split('\n')
                bullet_list = []
                for line in lines:
                    line = line.strip()
                    if line.startswith('- ') or line.startswith('• '):
                        bullet_list.append(f"<li>{line[2:].strip()}</li>")
                    elif line and bullet_list:
                        bullet_list[-1] = bullet_list[-1].replace('</li>', f" {line}</li>")
                
                if bullet_list:
                    formatted_paragraphs.append(f"<ul>{''.join(bullet_list)}</ul>")
            else:
                # Regular paragraph
                formatted_paragraphs.append(f"<p>{paragraph}</p>")
    
    return ''.join(formatted_paragraphs)

def validate_openai_connection() -> bool:
    """
    Validate that OpenAI API is accessible and working.
    
    Returns:
        bool: True if connection is successful
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": "Test connection"}],
            max_tokens=10
        )
        return True
    except Exception as e:
        logger.error(f"OpenAI connection failed: {str(e)}")
        return False
