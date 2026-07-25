import os
import time
import threading
import requests
from datetime import datetime, timedelta, timezone
from flask import Flask

app = Flask("app")

TOKEN = "7924553793:AAH_bk0YoW0EqTqQpjKS77n3WiWW0V9Yfag"
CHAT = "-1003805942629"

INTERVALS = {
    "15m": "15m",
    "1h": "1h",
    "4h": "4h",
    "d": "1d",
    "w": "1w"
}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT, "text": message})
    except Exception as e:
        print(f"Telegram error: {e}")

@app.route("/")
def home():
    return "Ahmed Pro Ultimate Signals Bot is running 24/7!"

def get_saudi_time():
    saudi_tz = timezone(timedelta(hours=3))
    return datetime.now(saudi_tz).strftime('%d-%m-%Y %H:%M:%S')

def calculate_golden_candle(candles):
    if len(candles) < 5:
        return None, 0, 0.0

    curr = candles[-1]
    open_p = float(curr[1])
    high_p = float(curr[2])
    low_p = float(curr[3])
    close_p = float(curr[4])

    body = abs(close_p - open_p)
    total_range = high_p - low_p
    if total_range == 0:
        return None, 0, 0.0

    body_ratio = body / total_range
    change_pct = ((close_p - open_p) / open_p) * 100

    if body_ratio >= 0.6 and abs(change_pct) >= 2.0:
        abs_change = abs(change_pct)
        if abs_change >= 5.0 or body_ratio >= 0.8:
            strength_val = min(int(85 + (abs_change - 5.0) * 3), 100)
        elif abs_change >= 3.0:
            strength_val = int(60 + (abs_change - 3.0) * 10)
        else:
            strength_val = int(40 + (abs_change - 2.0) * 15)

        signal_type = "BULLISH" if close_p > open_p else "BEARISH"
        return signal_type, strength_val, close_p

    return None, 0, 0.0

def scanner_loop():
    send_telegram("🚀 تم تشغيل بوت الشموع الذهبية بالمؤشر المخصص والفريمات المتعددة بنجاح!")
    history_signals = {}

    while True:
        try:
            exchange_info = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo", timeout=10).json()
            symbols = [s['symbol'] for s in exchange_info.get('symbols', []) if s['symbol'].endswith('USDT') and s['status'] == 'TRADING']

            for symbol in symbols[:30]:
                formatted_symbol = f"#{symbol}.P"
                
                for timeframe, interval_val in INTERVALS.items():
                    try:
                        klines_url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval_val}&limit=10"
                        res = requests.get(klines_url, timeout=5)
                        if res.status_code != 200:
                            continue
                        candles = res.json()

                        signal_type, strength_val, current_price = calculate_golden_candle(candles)
                        if not signal_type:
                            continue

                        candle_time_stamp = candles[-1][0]
                        sig_key = f"{symbol}_{timeframe}_{candle_time_stamp}"
                        if history_signals.get(sig_key):
                            continue
                        history_signals[sig_key] = True

                        if strength_val >= 85:
                            strength_desc = "قوية"
                        elif strength_val >= 60:
                            strength_desc = "متوسطة"
                        else:
                            strength_desc = "ضعيفة"

                        current_time_str = get_saudi_time()

                        if signal_type == "BULLISH":
                            msg = "🟡 GOLDEN BULLISH — LIVE\n\n"
                            msg += f"💰 العملة: {formatted_symbol}\n"
                            msg += f"⏰ الفريم: {timeframe}\n"
                            msg += f"💲 السعر: {current_price:.5f}\n\n"
                            msg += "✅ ظهرت شمعة ذهبية صاعده الآن\n"
                            msg += f"⚡ وقت ظهور الشمعة الذهبية: {current_time_str}\n"
                            msg += "⏳ الشمعة ما زالت قيد التكوين\n"
