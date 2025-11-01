from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "🔥 KralZeka Proxy Aktif (Tokensiz Ücretsiz Sürüm) 🔥"

@app.route("/api", methods=["POST"])
def api():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Lütfen bir prompt gönderin!"}), 400

    # Hugging Face’in anonim erişime açık modeli (tokensiz)
    model_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

    response = requests.post(
        model_url,
        headers={},  # Token yok, anonim erişim
        json={"inputs": prompt}
    )

    if response.status_code != 200:
        return jsonify({
            "error": "Model isteği başarısız.",
            "status": response.status_code,
            "details": response.text
        }), response.status_code

    try:
        result = response.json()
        output_text = result[0]["generated_text"]
    except Exception:
        output_text = str(result)

    return jsonify({"reply": output_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
