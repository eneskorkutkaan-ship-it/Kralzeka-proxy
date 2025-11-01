from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Kralzeka Proxy çalışıyor! 👑"

@app.route('/test')
def test():
    return jsonify({"status": "alive", "message": "Kralzeka Proxy aktif 🔥"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
