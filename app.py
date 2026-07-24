import os
import time
import threading
import requests
from flask import Flask

app = Flask("app")

TOKEN = "7924553793:AAH_bk0YoW0EqTqQpjKS77n3WiWW0V9Yfag"
CHAT = "-1003805942629"

@app.route("/")
def home():
    return "Running"

def job():
    while True:
        try:
            requests.get("https://fapi.binance.com/fapi/v1/ticker/24hr")
        except:
            pass
        time.sleep(60)

threading.Thread(target=job, daemon=True).start()

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
