from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-70b-8192"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json.get("prompt", "")
    if not prompt:
        return jsonify({"response": "Please ask a question."})

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful AI study assistant for a 14-year-old student."},
            {"role": "user", "content": prompt}
        ]
    }

    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    if res.status_code == 200:
        response_text = res.json()["choices"][0]["message"]["content"]
        return jsonify({"response": response_text})
    else:
        return jsonify({"response": f"Error: {res.text}"}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)


