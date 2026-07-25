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

def scanner_loop():
    send_telegram("Bot is running successfully!")
    history_signals = {}

    while True:
        try:
            res_info = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo", timeout=10)
            if res_info.status_code != 200:
                time.sleep(30)
                continue
            
            exchange_info = res_info.json()
            symbols = [s['symbol'] for s in exchange_info.get('symbols', []) if s['symbol'].endswith('USDT') and s['status'] == 'TRADING']

            for symbol in symbols[:25]:
                formatted_symbol = f"#{symbol}.P"
                
                for timeframe, interval_val in INTERVALS.items():
                    try:
                        klines_url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval_val}&limit=10"
                        res = requests.get(klines_url, timeout=5)
                        if res.status_code != 200:
                            continue
                        candles = res.json()
                        if len(candles) < 5:
                            continue

                        curr = candles[-1]
                        open_p = float(curr[1])
                        high_p = float(curr[2])
                        low_p = float(curr[3])
                        close_p = float(curr[4])

                        body = abs(close_p - open_p)
                        total_range = high_p - low_p
                        if total_range == 0:
                            continue

                        body_ratio = body / total_range
                        change_pct = ((close_p - open_p) / open_p) * 100

                        if body_ratio >= 0.6 and abs(change_pct) >= 2.0:
                            abs_change = abs(change_pct)
                            if abs_change >= 5.0 or body_ratio >= 0.8:
                                strength_val = min(int(85 + (abs_change - 5.0) * 3), 100)
                                strength_desc = "Strong"
                            elif abs_change >= 3.0:
                                strength_val = int(60 + (abs_change - 3.0) * 10)
                                strength_desc = "Medium"
                            else:
                                strength_val = int(40 + (abs_change - 2.0) * 15)
                                strength_desc = "Weak"

                            signal_type = "BULLISH" if close_p > open_p else "BEARISH"
                            candle_time_stamp = candles[-1][0]
                            sig_key = f"{symbol}_{timeframe}_{candle_time_stamp}"
                            
                            if history_signals.get(sig_key):
                                continue
                            history_signals[sig_key] = True

                            current_time_str = get_saudi_time()
                            price_str = "{:.5f}".format(close_p)

                            if signal_type == "BULLISH":
                                p1 = "GOLDEN BULLISH - LIVE\n\nCoin: " + formatted_symbol + "\n"
                                p2 = "Timeframe: " + timeframe + "\n"
                                p3 = "Price: " + price_str + "\n\n"
                                p4 = "Golden Bullish Candle Appeared Now\n"
                                p5 = "Golden Candle Time: " + current_time_str + "\n"
                                p6 = "Candle Still Forming\nCandle Confirmed\n\n"
                                p7 = "Signal Strength: " + strength_desc + " - " + str(strength_val) + "%\n\n"
                                p8 = current_time_str + " (Saudi Arabia)\n\n"
                                p9 = "Binance Futures | TradingView\n\nAhmed Pro Ultimate Signals"
                                msg = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
                            else:
                                p1 = "GOLDEN BEARISH - LIVE\n\nCoin: " + formatted_symbol + "\n"
                                p2 = "Timeframe: " + timeframe + "\n"
                                p3 = "Price: " + price_str + "\n\n"
                                p4 = "Golden Bearish Candle Appeared Now\n"
                                p5 = "Golden Candle Time: " + current_time_str + "\n"
                                p6 = "Candle Still Forming\nCandle Confirmed\n\n"
                                p7 = "Signal Strength: " + strength_desc + " - " + str(strength_val) + "%\n\n"
                                p8 = current_time_str + " (Saudi Arabia)\n\n"
                                p9 = "Binance Futures | TradingView\n\nAhmed Pro Ultimate Signals"
                                msg = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9

                            send_telegram(msg)
                            time.sleep(2)
                    except Exception:
                        continue

            time.sleep(30)

        except Exception as e:
            print(f"Scanner error: {e}")
            time.sleep(30)

threading.Thread(target=scanner_loop, daemon=True).start()

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
