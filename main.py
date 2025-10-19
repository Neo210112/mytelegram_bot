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
# تغییرات برای تشخیص بهتر تگ
   text_lower = text.lower().strip()
   bot_username_lower = BOT_USERNAME.lower().strip()

   if bot_username_lower in text_lower or message.get("chat", {}).get("type") == "private":
      # پاک کردن یوزرنیم از متن (با case-insensitive)
      clean_text = text_lower.replace(bot_username_lower, "").strip()
      # اگر clean_text خالی بود، پیام اولیه رو نمایش بده
      if not clean_text:
        send_message(chat_id, "سلام! یه سوال بپرس تا جواب بدم 🤖")
        return "OK"
            reply = ask_chatgpt(clean or "سلام!")
            send_message(chat_id, reply)
   if "gpt" in text_lower or "سوال" in text_lower or message.get("chat", {}).get("type") == "private":
    clean_text = text_lower.replace("gpt", "").replace("سوال", "").strip()
    if not clean_text:
        clean_text = "سلام!"
    response = ask_chatgpt(clean_text)
    send_message(chat_id, response)
    return "OK"

if name == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
