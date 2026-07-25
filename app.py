import os
import threading
import time
import ccxt
import requests
from flask import Flask

# إعدادات البوت والتلجرام
TELEGRAM_TOKEN = '7924553793:AAH_bk0YoW0EqTqQpjKS77n3WiWW0V9Yfag'
CHAT_ID = '-1003805942629'

app = Flask(__name__)


def send_telegram_message(message):
  """دالة لإرسال الرسائل مباشرة إلى تلجرام"""
  url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
  payload = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
  try:
    response = requests.post(url, json=payload)
    if response.status_code != 200:
      print(f'فشل إرسال رسالة تلجرام: {response.text}')
  except Exception as e:
    print(f'خطأ في الاتصال بتلجرام: {e}')


@app.route('/')
def home():
  return 'Bot is running and monitoring Binance Futures!'


# ==========================================
# دالة مراقبة السوق المرنة والفحص المستمر
# ==========================================
def market_monitoring_loop():
  print('Starting market monitoring background thread...')

  # تهيئة منصة باينانس للفيوتشر
  exchange = ccxt.binance({
      'enableRateLimit': True,
      'options': {'defaultType': 'future'},
  })

  while True:
    try:
      print('جاري فحص السوق وجلب بيانات باينانس والتنبيهات...')

      # جلب أسواق الفيوتشر
      markets = exchange.load_markets()
      symbols = [
          symbol for symbol in markets if symbol.endswith('/USDT:USDT')
      ]

      # سنقوم باختبار فحص عينة من العملات أو العملات النشطة للتأكد من وصول التنبيهات
      # (شروط مرنة جداً للتجربة والتأكد من عمل البوت وإرساله للتنبيهات)
      signal_sent_count = 0

      for symbol in symbols[
          :15
      ]:  # فحص أول 15 عملة كمثال للتأكد من السرعة والوصول
        try:
          # جلب شموع فريم 15 دقيقة
          ohlcv = exchange.fetch_ohlcv(symbol, timeframe='15m', limit=5)
          if len(ohlcv) < 5:
            continue

          # حساب التغير البسيط في السعر للشمعة الأخيرة (شروط مرنة لتوليد إشارة تجريبية)
          prev_close = ohlcv[-2][4]
          current_close = ohlcv[-1][4]
          price_change = ((current_close - prev_close) / prev_close) * 100

          # شرط مرن جداً (مثلاً أي تغير بنسبة أكبر من 0.1% أو للتجربة الفورية)
          if abs(price_change) >= 0.1:
            message = (
                f'🚨 **تنبيه شمعة ذهبية (مرن)** 🚨\n\n'
                f'🪙 العملة: `{symbol}`\n'
                f'📊 الفريم: 15m\n'
                f'💰 السعر الحالي: `{current_close}`\n'
                f'📈 نسبة التغير: `{price_change:.2f}%`\n'
                f'⚡️ الحالة: إشارة جديدة تم رصدها بنجاح!'
            )
            send_telegram_message(message)
            signal_sent_count += 1
            time.sleep(1)  # تجنب حظر تلجرام عند إرسال أكثر من رسالة
        except Exception as inner_e:
          # تجاهل أخطاء العملة الفردية والاستمرار لباقي العملات
          continue

      print(
          f'تم فحص السوق بنجاح. تم إرسال {signal_sent_count} تنبيه. في انتظار'
          ' الدورة القادمة.'
      )

    except Exception as e:
      print(f'حدث خطأ في حلقة المراقبة العامة: {e}')

    # الانتظار لمدة دقيقة (60 ثانية) قبل الفحص التالي
    time.sleep(60)


# ==========================================
# نقطة بداية تشغيل التطبيق
# ==========================================
if __name__ == '__main__':
  # 1. تشغيل دالة فحص السوق في خيط خلفي (Background Thread)
  bot_thread = threading.Thread(target=market_monitoring_loop, daemon=True)
  bot_thread.start()

  # 2. تشغيل خادم الويب (Flask) ليبقى التطبيق نشطاً على منصة Railway
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)
