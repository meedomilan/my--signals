import os
import time
import threading
import requests
from flask import Flask

app = Flask("app")

TOKEN = "7924553793:AAH_bk0YoW0EqTqQpjKS77n3WiWW0V9Yfag"
CHAT = "-1003805942629"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT, "text": message})
    except Exception as e:
        print(f"Telegram error: {e}")

@app.route("/")
def home():
    return "Bot is running 24/7!"

def scanner_loop():
    # رسالة لتأكدك أن الفاحص بدأ العمل
    send_telegram("🚀 تم تشغيل بوت فحص الأسواق بنجاح وهو الآن مراقب للسوق 24/7!")
    
    while True:
        try:
            url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
            response = requests.get(url)
            data = response.json()
            
            # هنا يمكنك وضع شروطك لاحقاً (مثلاً نسبة التغير، الصعود القوي، إلخ)
            # كمثال تجريبي، السيرفر يعمل الآن ويتحقق من البيانات كل دقيقة
            
        except Exception as e:
            print(f"Scanner error: {e}")
            
        time.sleep(60)

# تشغيل الفاحص في الخلفية
threading.Thread(target=scanner_loop, daemon=True).start()

if name == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
