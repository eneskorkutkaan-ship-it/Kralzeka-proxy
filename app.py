from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Herkese açık çalışan model (Gemma 2B)
MODEL_URL = "https://api-inference.huggingface.co/models/google/gemma-2b-it"

@app.route("/")
def home():
    return "🤖 KralZeka Gemma Proxy Aktif ve Tokensiz Çalışıyor!"

@app.route("/api", methods=["POST"])
def api():
    data = request.get_json(force=True, silent=True) or {}
    user_input = data.get("prompt")

    if not user_input:
        return jsonify({"error": "Lütfen bir prompt gönderin!"}), 400

    body = {
        "inputs": user_input,
        "parameters": {"max_new_tokens": 256}
    }

    try:
        response = requests.post(MODEL_URL, json=body)
        if response.status_code != 200:
            return jsonify({
                "error": "Model isteği başarısız.",
                "details": response.text,
                "status": response.status_code
            }), response.status_code

        result = response.json()
        # Yanıt metnini çek
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            reply = result[0]["generated_text"]
        else:
            reply = str(result)

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": f"Sunucu hatası: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
