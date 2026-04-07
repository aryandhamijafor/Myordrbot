import requests
from telegram.ext import Updater, CommandHandler

# Your bot token from BotFather
BOT_TOKEN = "8557923203:AAEvQ_NEdAKTPiRrqoxPEWfvU-ihlWBpiCM"
API_URL = "https://getsolditems-mvuynfmg6a-uc.a.run.app"

def top_sellers(update, context):
    try:
        response = requests.post(API_URL).json()
        items = sorted(response["data"], key=lambda x: x["Sold"], reverse=True)[:3]
        msg = "\n".join([f"{i['Item']} - {i['Sold']} sold" for i in items])
        update.message.reply_text(f"Top 3 sellers:\n{msg}")
    except Exception as e:
        update.message.reply_text(f"Error fetching data: {e}")

def slow_movers(update, context):
    try:
        response = requests.post(API_URL).json()
        items = [i for i in response["data"] if i["Sold"] < 10]
        if not items:
            update.message.reply_text("No slow movers found.")
            return
        msg = "\n".join([f"{i['Item']} - {i['Sold']} sold" for i in items[:10]])
        update.message.reply_text(f"Slow movers (under 10 sales):\n{msg}")
    except Exception as e:
        update.message.reply_text(f"Error fetching data: {e}")

def start(update, context):
    update.message.reply_text("Welcome! Use /topsellers or /slowmovers to test.")

updater = Updater(BOT_TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("topsellers", top_sellers))
dp.add_handler(CommandHandler("slowmovers", slow_movers))

updater.start_polling()
updater.idle()
