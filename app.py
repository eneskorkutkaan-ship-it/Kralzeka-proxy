from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Tokensiz model (Gemma 2B)
MODEL_URL = "https://api-inference.huggingface.co/models/google/gemma-2b-it"

@app.route("/")
def home():
    return "✅ KralZeka Tokensiz Gemma Proxy Aktif!"

@app.route("/api", methods=["POST"])
def api():
    data = request.get_json(force=True, silent=True) or {}
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Lütfen prompt girin."}), 400

    # Hugging Face'e istek at
    body = {"inputs": prompt, "parameters": {"max_new_tokens": 100}}
    response = requests.post(MODEL_URL, json=body)

    if response.status_code != 200:
        return jsonify({
            "error": "Model isteği başarısız.",
            "status": response.status_code,
            "details": response.text
        }), response.status_code

    result = response.json()
    if isinstance(result, list) and "generated_text" in result[0]:
        reply = result[0]["generated_text"]
    else:
        reply = str(result)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
