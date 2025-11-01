from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Hugging Face Token (buraya senin tokenin gelecek)
HF_TOKEN = "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"

# Kullanmak istediğin model
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

@app.route('/')
def home():
    return "KralZeka API çalışıyor! 👑"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Lütfen bir mesaj gönder."}), 400

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": user_message,
        "parameters": {"max_new_tokens": 200}
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL}",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return jsonify({
            "error": "Model isteği başarısız.",
            "status": response.status_code,
            "details": response.text
        }), response.status_code

    result = response.json()
    answer = result[0]["generated_text"] if isinstance(result, list) else result
    return jsonify({"reply": answer})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
