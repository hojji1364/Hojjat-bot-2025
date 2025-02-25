import logging
import openai
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# تنظیمات لاگ
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# دریافت توکن‌ها از متغیرهای محیطی
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# تنظیم OpenAI
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("سلام! من یک ربات هوشمند هستم. از من هر چیزی بپرس!")

async def chat(update: Update, context: CallbackContext):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # یا "gpt-3.5-turbo"
            messages=[{"role": "user", "content": user_message}]
        )
        reply_text = response["choices"][0]["message"]["content"]
        await update.message.reply_text(reply_text)
    except Exception as e:
        await update.message.reply_text("خطایی رخ داد! لطفاً بعداً امتحان کنید.")
        logging.error(f"خطا در دریافت پاسخ از OpenAI: {e}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("ربات فعال شد!")
    app.run_polling()

if __name__ == "__main__":
    main()
