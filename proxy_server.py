from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "KralZeka Ücretsiz Proxy Aktif 🧠🔥"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("prompt")

    if not user_input:
        return jsonify({"error": "Prompt eksik!"}), 400

    # Hugging Face ücretsiz model API'si
    model_url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    
    headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

    body = {"inputs": user_input}

    response = requests.post(model_url, headers=headers, json=body)

    if response.status_code != 200:
        return jsonify({
            "error": "Hugging Face isteği başarısız!",
            "details": response.text
        }), 500

    try:
        answer = response.json()[0]["generated_text"]
    except Exception:
        answer = "Modelden yanıt alınamadı."

    return jsonify({"reply": answer})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
