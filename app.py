import os
import time
import threading
import requests
from datetime import datetime, timedelta, timezone
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
    return "Golden Candle Bot is running 24/7!"

def get_saudi_time():
    saudi_tz = timezone(timedelta(hours=3))
    return datetime.now(saudi_tz).strftime('%d-%m-%Y %H:%M:%S')

def scanner_loop():
    send_telegram("🚀 تم تفعيل بوت الشموع الذهبية وربط الأسعار الحقيقية بنجاح!")
    
    while True:
        try:
            url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
            response = requests.get(url)
            data = response.json()
            
            for item in data:
                symbol = item.get('symbol', '')
                if symbol.endswith('USDT'):
                    formatted_symbol = f"#{symbol}.P"
                    price_change = float(item.get('priceChangePercent', 0))
                    
                    # جلب السعر الصحيح من الحقل المعتمد في باينانس
                    current_price = item.get('lastPrice') or item.get('price', '0')
                    
                    current_time = get_saudi_time()
                    
                    if price_change >= 4.0:
                        msg = f"""🟡 GOLDEN BULLISH — LIVE

💰 العملة: {formatted_symbol}
⏰ الفريم: 1h
💲 السعر: {current_price}

✅ ظهرت شمعة ذهبية صاعدة الآن
⚡ وقت ظهور الشمعة الذهبية: {current_time}
⏳ الشمعة ما زالت قيد التكوين

🔥 قوة الإشارة: قوية — 75%

🕒 {current_time} (السعودية)

🔗 Binance Futures | TradingView

🤖 Ahmed Pro Ultimate Signals"""
                        send_telegram(msg)
                        time.sleep(3)
                        
                    elif price_change <= -4.0:
                        msg = f"""🟡 GOLDEN BEARISH — LIVE

💰 العملة: {formatted_symbol}
⏰ الفريم: 1h
💲 السعر: {current_price}

✅ ظهرت شمعة ذهبية هابطة الآن
⚡ وقت ظهور الشمعة الذهبية: {current_time}
⏳ الشمعة ما زالت قيد التكوين

🔥 قوة الإشارة: قوية — 75%

🕒 {current_time} (السعودية)

🔗 Binance Futures | TradingView

🤖 Ahmed Pro Ultimate Signals"""
                        send_telegram(msg)
                        time.sleep(3)
            
        except Exception as e:
            print(f"Scanner error: {e}")
            
        time.sleep(180)

threading.Thread(target=scanner_loop, daemon=True).start()

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
