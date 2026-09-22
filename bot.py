import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from google import genai

TELEGRAM_BOT_TOKEN = "8647926537:AAFiZdHIWltSKFUSY0lotU-WkVUyjFsPolc"
GEMINI_API_KEY = "AQ.Ab8RN6K03zE_VJIzYbMFbu0nk15IzhzuWDljqHLGVro5hkzQ9A"

client = genai.Client(api_key=GEMINI_API_KEY)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا بوت البحث والتحليل الذكي.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=update.message.text,
        )
        reply_text = response.text
    except Exception as e:
        reply_text = "عذراً، حدث خطأ أثناء معالجة طلبك."
        logging.error(f"Error: {e}")
        
    await update.message.reply_text(reply_text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت يعمل الآن بنجاح...")
    app.run_polling()
