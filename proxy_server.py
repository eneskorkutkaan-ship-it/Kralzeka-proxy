from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/kralzeka', methods=['POST'])
def kralzeka():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        reply = f"KralZeka'dan cevap: {user_message[::-1]}"
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
