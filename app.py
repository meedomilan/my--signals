import os
import time
import threading
import requests
from flask import Flask, jsonify

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "7924553793:AAH_bk0YoW0EqTqQpjKS77n3WiWW0V9Yfag"
TELEGRAM_CHAT_ID = "-1003805942629"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error: {e}")

@app.route("/", methods=["GET"])
def home():
    return "Bot is running 24/7!"

def binance_scanner():
    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    while True:
        try:
            requests.get(url)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)

if name == "__main__":
    scanner_thread = threading.Thread(target=binance_scanner)
    scanner_thread.daemon = True
    scanner_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
