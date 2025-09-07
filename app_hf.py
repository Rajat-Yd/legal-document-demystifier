import os
import gradio as gr
import tempfile
from utils.document_processor import extract_text_from_file
from utils.ai_processor import simplify_legal_text, summarize_document, answer_question

def process_document(file, action, question=""):
    """Process uploaded document based on selected action"""
    if file is None:
        return "Please upload a file first."
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as temp_file:
            temp_file.write(file.read())
            temp_path = temp_file.name
        
        # Extract text
        document_text = extract_text_from_file(temp_path)
        
        # Clean up temp file
        os.unlink(temp_path)
        
        if not document_text.strip():
            return "Could not extract text from the document. Please check if the file is valid."
        
        # Process based on action
        if action == "Simplify":
            result = simplify_legal_text(document_text)
            if result.get('error'):
                return f"Error: {result['error']}"
            
            output = f"**Simplified Text:**\n{result.get('simplified_text', '')}\n\n"
            if result.get('risks'):
                output += f"**Risks Identified:**\n" + "\n".join([f"• {risk}" for risk in result['risks']]) + "\n\n"
            if result.get('obligations'):
                output += f"**Your Obligations:**\n" + "\n".join([f"• {obligation}" for obligation in result['obligations']]) + "\n\n"
            if result.get('key_points'):
                output += f"**Key Points:**\n" + "\n".join([f"• {point}" for point in result['key_points']])
            return output
            
        elif action == "Summarize":
            result = summarize_document(document_text)
            if result.get('error'):
                return f"Error: {result['error']}"
            
            output = f"**Executive Summary:**\n{result.get('summary', '')}\n\n"
            if result.get('risks'):
                output += f"**Critical Risks:**\n" + "\n".join([f"• {risk}" for risk in result['risks']]) + "\n\n"
            if result.get('obligations'):
                output += f"**Key Obligations:**\n" + "\n".join([f"• {obligation}" for obligation in result['obligations']]) + "\n\n"
            if result.get('key_points'):
                output += f"**Important Points:**\n" + "\n".join([f"• {point}" for point in result['key_points']])
            return output
            
        elif action == "Ask Question":
            if not question.strip():
                return "Please enter a question to get an answer."
            
            result = answer_question(document_text, question)
            if result.get('error'):
                return f"Error: {result['error']}"
            
            output = f"**Answer:**\n{result.get('answer', '')}\n\n"
            if result.get('relevant_clauses'):
                output += f"**Relevant Clauses:**\n" + "\n".join([f"• {clause}" for clause in result['relevant_clauses']]) + "\n\n"
            if result.get('risks'):
                output += f"**Related Risks:**\n" + "\n".join([f"• {risk}" for risk in result['risks']]) + "\n\n"
            if result.get('recommendations'):
                output += f"**Recommendations:**\n" + "\n".join([f"• {rec}" for rec in result['recommendations']])
            return output
            
    except Exception as e:
        return f"Error processing document: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="Legal Document Demystifier", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # ⚖️ Legal Document Demystifier
    
    Transform complex legal documents into plain, understandable language with AI-powered analysis.
    
    **Features:**
    - 🔍 **Simplify**: Convert legalese into plain English
    - 📋 **Summarize**: Get executive summaries with key risks
    - ❓ **Q&A**: Ask specific questions about your document
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(
                label="Upload Legal Document", 
                file_types=[".pdf", ".txt"],
                file_count="single"
            )
            
            action = gr.Radio(
                choices=["Simplify", "Summarize", "Ask Question"],
                label="Choose Action",
                value="Simplify"
            )
            
            question_input = gr.Textbox(
                label="Your Question (for Q&A mode)",
                placeholder="Example: What are my obligations under this contract?",
                lines=2,
                visible=False
            )
            
            submit_btn = gr.Button("Analyze Document", variant="primary")
        
        with gr.Column(scale=2):
            output = gr.Textbox(
                label="Analysis Results",
                lines=20,
                max_lines=30
            )
    
    # Show/hide question input based on action
    def update_question_visibility(action_choice):
        return gr.update(visible=(action_choice == "Ask Question"))
    
    action.change(
        fn=update_question_visibility,
        inputs=[action],
        outputs=[question_input]
    )
    
    # Process document on submit
    submit_btn.click(
        fn=process_document,
        inputs=[file_input, action, question_input],
        outputs=[output]
    )
    
    gr.Markdown("""
    ### How to Use:
    1. Upload a PDF or TXT legal document (max 16MB)
    2. Choose your desired action
    3. For Q&A mode, enter your specific question
    4. Click "Analyze Document" to get results
    
    **Built with Google Gemini AI** • Perfect for contracts, agreements, legal notices, and more!
    """)

if __name__ == "__main__":
    demo.launch()