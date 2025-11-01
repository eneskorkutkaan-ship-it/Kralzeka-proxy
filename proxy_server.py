from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Kralzeka Proxy Aktif 🔥"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("prompt")

    if not user_input:
        return jsonify({"error": "Prompt eksik!"}), 400

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_input}]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        return jsonify({"error": "OpenAI isteği başarısız!", "details": response.text}), 500

    answer = response.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": answer})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
