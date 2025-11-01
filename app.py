from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "KralZeka HuggingFace Proxy Aktif 🔥 (Tokensiz Ücretsiz Sürüm)"

@app.route("/api", methods=["POST"])
def api():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Lütfen bir prompt gönderin!"}), 400

    # Hugging Face’in açık (anonim) modeline istek
    response = requests.post(
        "https://api-inference.huggingface.co/models/google/gemma-2b-it",
        headers={},  # tokensiz
        json={"inputs": prompt}
    )

    if response.status_code != 200:
        return jsonify({
            "error": "Model isteği başarısız.",
            "status": response.status_code,
            "details": response.text
        }), response.status_code

    result = response.json()
    try:
        reply = result[0]["generated_text"]
    except Exception:
        reply = str(result)

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
