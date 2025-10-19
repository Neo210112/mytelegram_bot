from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
BOT_USERNAME = os.environ.get("BOT_USERNAME", "@MyGpt69_bot")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def ask_chatgpt(prompt):
    res = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",  # ارزان و سریع — یا "gpt-4" اگر خواستی
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512
        }
    )
    if res.ok:
        return res.json()["choices"][0]["message"]["content"].strip()
    else:
        error_msg = res.json().get("error", {}).get("message", "خطا در ارتباط")
        return f"❌ خطا: {error_msg}"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")
        if BOT_USERNAME in text or msg["chat"]["type"] == "private":
            clean = text.replace(BOT_USERNAME, "").strip()
            reply = ask_chatgpt(clean or "سلام!")
            send_message(chat_id, reply)
    return "OK"

if name == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
