from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# OpenAI veya başka bir API'ye proxy yönlendirme örneği
# Buraya kendi API anahtarını eklersen çalışır
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY_HERE")

@app.route('/')
def home():
    return "✅ KralZeka Proxy çalışıyor!"

# Chat proxy endpointi
@app.route('/v1/chat/completions', methods=['POST'])
def chat_proxy():
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = request.get_json()

        # Orijinal OpenAI endpointine yönlendir
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )

        return (response.text, response.status_code, response.headers.items())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render için gerekli
    app.run(host='0.0.0.0', port=port)
