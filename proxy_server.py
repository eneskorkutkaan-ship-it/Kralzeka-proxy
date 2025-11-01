from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ KralZeka Proxy çalışıyor!"

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    try:
        data = request.get_json()
        user_message = data["messages"][0]["content"]

        # Basit bir cevap örneği:
        response_text = f"KralZeka çevrimiçi! Mesajını aldım: {user_message}"

        return jsonify({
            "id": "chatcmpl-kralzeka001",
            "object": "chat.completion",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text
                    },
                    "finish_reason": "stop"
                }
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
