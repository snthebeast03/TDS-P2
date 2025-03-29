from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
API_KEY = os.environ.get("eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjEwMDE1OTlAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.uTR9VdsvciCVXRPPt17VxRA34LK1Xolxom_2QOVMpiA")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

@app.route('/api/', methods=['POST'])
def answer_question():
    question = request.form.get('question')
    file = request.files.get('file')
    
    if not question:
        return jsonify({"error": "Missing question parameter"}), 400
    
    if not file:
        return jsonify({"error": "Missing file parameter"}), 400
    
    file_content = file.read().decode("utf-8", errors="ignore")
    full_input = f"{question}\n\n{file_content}"
    
    answer = get_llm_answer(full_input)
    return jsonify({"answer": answer})

def get_llm_answer(prompt):
    try:
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        response = requests.post(OPENAI_API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error fetching LLM response: {str(e)}"

# Convert Flask app to ASGI for Vercel
from mangum import Mangum
handler = Mangum(app)
