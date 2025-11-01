from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # Ücretsiz, güçlü model

@app.route("/")
def home():
    return "🔥 KralZeka HuggingFace Proxy Aktif 🔥"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("prompt")

    if not user_input:
        return jsonify({"error": "Prompt eksik!"}), 400

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": user_input,
        "parameters": {"max_new_tokens": 200}
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return jsonify({
            "error": "Hugging Face isteği başarısız!",
            "details": response.text
        }), 500

    result = response.json()
    try:
        reply = result[0]["generated_text"]
    except Exception:
        reply = str(result)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
