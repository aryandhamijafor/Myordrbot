import requests
from telegram.ext import ApplicationBuilder, CommandHandler

BOT_TOKEN = "8557923203:AAEvQ_NEdAKTPiRrqoxPEWfvU-ihlWBpiCM"
API_URL = "https://getsolditems-mvuynfmg6a-uc.a.run.app"

async def topsellers(update, context):
    try:
        response = requests.post(API_URL).json()
        items = sorted(response["data"], key=lambda x: x["Sold"], reverse=True)[:3]
        msg = "\n".join([f"{i['Item']} - {i['Sold']} sold" for i in items])
        await update.message.reply_text(f"Top 3 sellers:\n{msg}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching data: {e}")

async def slowmovers(update, context):
    try:
        response = requests.post(API_URL).json()
        items = [i for i in response["data"] if i["Sold"] < 10]
        if not items:
            await update.message.reply_text("No slow movers found.")
            return
        msg = "\n".join([f"{i['Item']} - {i['Sold']} sold" for i in items[:10]])
        await update.message.reply_text(f"Slow movers (under 10 sales):\n{msg}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching data: {e}")

async def start(update, context):
    await update.message.reply_text("Welcome! Use /topsellers or /slowmovers to test.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("topsellers", topsellers))
    app.add_handler(CommandHandler("slowmovers", slowmovers))
    app.run_polling()

if __name__ == "__main__":
    main()
