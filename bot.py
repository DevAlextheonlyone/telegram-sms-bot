from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from twilio.rest import Client
import os
import threading

# ====== ENV ======
BOT_TOKEN = os.environ.get("BOT_TOKEN")

TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH = os.environ.get("TWILIO_AUTH")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")

client = Client(TWILIO_SID, TWILIO_AUTH)

# ====== COMMANDS ======

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📱 SMS Bot\n\n"
        "Use:\n"
        "`/sms +46701234567 Hello`",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 *Help*\n\n"
        "`/sms <phone> <message>`\n\n"
        "Example:\n"
        "`/sms +46701234567 Hi!`",
        parse_mode="Markdown"
    )

async def sms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage: /sms +46701234567 message")
        return

    phone = context.args[0]
    text = " ".join(context.args[1:])

    try:
        message = client.messages.create(
            body=f"From @{update.message.from_user.username}: {text}",
            from_=TWILIO_NUMBER,
            to=phone
        )

        await update.message.reply_text("✅ SMS sent!")

    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{e}")

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("sms", sms_command))

    app.run_polling()

# ====== START BOTH ======
if __name__ == "__main__":
    from web import app
    import threading

    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
