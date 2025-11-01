from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Açık, herkese açık çalışan model (senin seçtiğin: Mistral)
MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

# Eğer token eklersen Render'da HUGGINGFACE_TOKEN olarak ekle (opsiyonel)
HF_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")

@app.route("/")
def home():
    return "🤖 KralZeka Mistral-7B Proxy Çalışıyor!"

@app.route("/api", methods=["POST"])
def api():
    data = request.get_json(force=True, silent=True) or {}
    user_input = data.get("input") or data.get("prompt") or ""
    if not user_input:
        return jsonify({"error": "Girdi (input) boş olamaz."}), 400

    payload = {"inputs": user_input}
    headers = {"Content-Type": "application/json"}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"

    resp = requests.post(MODEL_URL, json=payload, headers=headers, timeout=120)

    if resp.status_code != 200:
        return jsonify({
            "error": "Model isteği başarısız.",
            "status": resp.status_code,
            "details": resp.text
        }), resp.status_code

    out = resp.json()
    text = ""
    if isinstance(out, list) and len(out) > 0:
        # Genel HF response formatlarını güvenli çek
        text = out[0].get("generated_text") or out[0].get("text") or str(out[0])
    else:
        text = str(out)

    return jsonify({"response": text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
