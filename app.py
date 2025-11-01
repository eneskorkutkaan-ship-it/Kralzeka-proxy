from flask import Flask, request, jsonify
import requests
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Denenecek modeller (anon erişime açık olanları ilk sıraya koydum)
CANDIDATE_MODELS = [
    "google/gemma-2b-it",
    "bigscience/bloom",
    "distilgpt2",                # küçük, anonim deneme için
    "gpt2"                       # fallback
]

# Eğer Hugging Face token eklediyseniz Render env var adı: HF_TOKEN
HF_TOKEN = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")


@app.route("/")
def home():
    return "✅ KralZeka Proxy (model deneme modunda)."

def hf_inference_call(model_id, prompt, token=None, max_tokens=128):
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": max_tokens}
    }
    try:
        resp = requests.post(url, headers=headers, json=body, timeout=30)
    except Exception as e:
        return {"ok": False, "status": None, "error": f"Request failed: {e}"}
    # try parse JSON (some errors return text)
    text = resp.text
    status = resp.status_code
    try:
        j = resp.json()
    except Exception:
        j = text
    return {"ok": resp.status_code == 200, "status": status, "json": j, "text": text}

@app.route("/api", methods=["POST"])
def api():
    data = request.get_json(force=True, silent=True) or {}
    prompt = data.get("prompt") or data.get("input") or data.get("message") or ""
    if not prompt:
        return jsonify({"error": "Lütfen JSON içinde 'prompt' alanı ile istekte bulunun."}), 400

    # 1) Eğer HF_TOKEN varsa *önce* token ile dener (en güvenli yol)
    tried = []
    if HF_TOKEN:
        for model in CANDIDATE_MODELS:
            result = hf_inference_call(model, prompt, token=HF_TOKEN)
            tried.append({"model": model, "status": result["status"], "ok": result["ok"], "details": result.get("json")})
            if result["ok"]:
                # response format farklı olabilir; normalize
                j = result.get("json")
                # many HF text-generation return list with 'generated_text'
                reply = None
                if isinstance(j, list) and j and isinstance(j[0], dict):
                    reply = j[0].get("generated_text") or j[0].get("text") or str(j[0])
                else:
                    reply = str(j)
                return jsonify({"reply": reply, "model": model, "tried": tried})
        # token var ama tokenli modeller çalışmadı -> dökümle dön
        return jsonify({"error": "Token ile denendi ama modeller yanıt vermedi.", "tried": tried}), 502

    # 2) HF_TOKEN yok -> anonim dene (token olmadan)
    anon_tried = []
    for model in CANDIDATE_MODELS:
        result = hf_inference_call(model, prompt, token=None)
        anon_tried.append({"model": model, "status": result["status"], "ok": result["ok"], "details": result.get("json")})
        if result["ok"]:
            j = result.get("json")
            if isinstance(j, list) and j and isinstance(j[0], dict):
                reply = j[0].get("generated_text") or j[0].get("text") or str(j[0])
            else:
                reply = str(j)
            return jsonify({"reply": reply, "model": model, "tried": anon_tried})

    # 3) Hiçbir anonim model çalışmadı -> kullanıcıyı bilgilendir
    message = {
        "error": "Anonim (tokensiz) istekler başarısız. Lütfen Hugging Face token (HF_TOKEN) ekleyin veya model değiştirin.",
        "hint": "Render > Environment bölümüne HF_TOKEN ekleyin (HuggingFace Access Token).",
        "anon_tried": anon_tried,
        "how_to_get_token": "https://huggingface.co/settings/tokens"
    }
    return jsonify(message), 401


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
