from flask import Flask, request, jsonify
import os
from transformers import pipeline

app = Flask(__name__)

# Load Local LLM Model (Using Hugging Face Transformers Pipeline)
qa_pipeline = pipeline("text-generation", model="distilgpt2", device_map="auto")

@app.route('/api/', methods=['POST'])
def answer_question():
    question = request.form.get('question')
    file = request.files.get('file')
    
    if not question:
        return jsonify({"error": "Missing question parameter"}), 400
    
    if not file:
        return jsonify({"error": "Missing file parameter"}), 400
    
    # Read file content
    file_content = file.read().decode("utf-8", errors="ignore")
    
    # Combine question and file content
    full_input = f"{question}\n{file_content}"
    
    # Send to LLM
    answer = get_llm_answer(full_input)
    return jsonify({"answer": answer})

def get_llm_answer(text):
    try:
        response = qa_pipeline(text, max_length=100, do_sample=True)
        return response[0]['generated_text']
    except Exception as e:
        return f"Error fetching LLM response: {str(e)}"

# Required for Vercel
def handler(event, context):
    return app(event, context)
