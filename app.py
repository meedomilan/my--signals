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
    return "Gold Candle Bot is running 24/7!"

def scanner_loop():
    send_telegram("🌟 تم تفعيل استراتيجية الشمعة الذهبية بنجاح، وجاري مراقبة السوق...")
    
    while True:
        try:
            url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
            response = requests.get(url)
            data = response.json()
            
            # فحص العملات التي تحقق شروط الزخم أو التغير القوي
            for item in data:
                symbol = item.get('symbol', '')
                # نركز على عقود الفิวشرز التي تنتهي بـ USDT
                if symbol.endswith('USDT'):
                    price_change = float(item.get('priceChangePercent', 0))
                    volume = float(item.get('quoteVolume', 0))
                    
                    # هنا شروط الشمعة الذهبية (كمثال: تغير إيجابي قوي وفوليوم عالي)
                    if price_change >= 5.0 and volume >= 10000000:
                        msg = f"🔥 تنبيه شمعة ذهبية!\n العملة: {symbol}\n التغير: +{price_change}%\n الفوليوم: {int(volume):,}"
                        send_telegram(msg)
                        time.sleep(2) # لتجنب الضغط على إرسال الرسائل
            
        except Exception as e:
            print(f"Scanner error: {e}")
            
        # الفحص كل 5 دقائق لعدم تكرار الإشعارات بشكل مزعج
        time.sleep(300)

threading.Thread(target=scanner_loop, daemon=True).start()

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
