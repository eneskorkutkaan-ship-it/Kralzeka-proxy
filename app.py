from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔹 Açık ve ücretsiz bir model kullanıyoruz (TinyLlama)
MODEL_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# 🔹 Hugging Face Token (isteğe bağlı — eğer özel model kullanırsan gerekli)
HF_TOKEN = os.environ.get("HF_TOKEN")

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

@app.route("/")
def home():
    return "🤖 KralZeka Mistral-7B Proxy Çalışıyor!"

@app.route("/api", methods=["POST"])
def api():
    try:
        data = request.get_json(force=True, silent=True) or {}
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "Bir prompt girmen gerekiyor."}), 400

        payload = {"inputs": prompt}
        response = requests.post(MODEL_URL, headers=HEADERS, json=payload)

        if response.status_code != 200:
            return jsonify({
                "error": "Model isteği başarısız.",
                "details": response.text,
                "status": response.status_code
            }), response.status_code

        result = response.json()

        # Hugging Face formatına göre metni ayıklama
        if isinstance(result, list) and len(result) > 0:
            output = result[0].get("generated_text", "")
        elif isinstance(result, dict) and "generated_text" in result:
            output = result["generated_text"]
        else:
            output = result

        return jsonify({"response": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
