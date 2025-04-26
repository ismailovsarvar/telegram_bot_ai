import os
import requests
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

# .env fayldan tokenlarni yuklash
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Groq API orqali javob olish
async def ask_groq(question):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": "Siz foydali va aniq javob beradigan assistantsiz."},
                {"role": "user", "content": question}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"⚠️ Xato: API javob bermadi (Kod: {response.status_code})"
    except Exception as e:
        return f"❌ Xatolik: {str(e)}"


# ReplyKeyboardMarkup yaratish
def get_reply_keyboard():
    keyboard = [
        ["📚 Yordam", "ℹ️ Bot haqida"],
        ["📝 Fikr bildirish", "❓ Savol berish"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# /start komandasi
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "👋 Salom! Men Groq AI yordamida ishlayman.",
            reply_markup=get_reply_keyboard()
        )
    except Exception as e:
        print(f"/start xatosi: {e}")
        await update.message.reply_text("😢 Botni ishga tushirib bo'lmadi.")


# Yordam matni
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🆘 <b>Yordam menyusi</b>\n\n"
        "🔹 <b>Savol berish:</b> Shunchaki xabar yozing\n"
        "🔹 <b>/ask</b> [savol] - Komanda orqali so'rov yuborish\n"
        "🔹 <b>/help</b> - Yordam menyusi\n"
        "🔹 <b>/about</b> - Bot haqida ma'lumot\n"
        "🔹 <b>/feedback</b> - Fikr-mulohaza bildirish\n\n"
        "Bot sizga quyidagi sohalarda yordam bera oladi:\n"
        "- Dasturlash (Python, JavaScript, C++)\n"
        "- Matematika va mantiq masalalari\n"
        "- Til bilish va tarjima\n"
        "- Umumiy bilimlar"
    )
    await update.message.reply_text(help_text, parse_mode="HTML", reply_markup=get_reply_keyboard())


# Bot haqida
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "🤖 <b>Groq AI Bot haqida</b>\n\n"
        "📅 Yaratilgan sana: 2024-yil\n"
        "🧠 AI model: Llama 3-70B (Groq API)\n"
        "⚡ Tezlik: 500+ tok/s\n"
        "👨‍💻 Dasturchi: Ismailov Sarvar (@ismailovsarvarbek)\n\n"
        "Bu bot Groq AI yordamida savollarga javob beradi."
    )
    await update.message.reply_text(about_text, parse_mode="HTML", reply_markup=get_reply_keyboard())


# Fikr-mulohaza uchun
async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📝 Iltimos, botimiz haqidagi fikr-mulohazalaringizni yozib qoldiring.\n\n"
        "Har qanday taklif, shikoyat yoki tushuntirish uchun xabar yuboring.\n"
        "Biz sizning fikringizni qadrlaymiz!"
    )
    await update.message.reply_text(msg, reply_markup=get_reply_keyboard())
    context.user_data['waiting_for_feedback'] = True


# Foydalanuvchi xabarlarini boshqarish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text

        if 'waiting_for_feedback' in context.user_data and context.user_data['waiting_for_feedback']:
            print(f"Foydalanuvchi {update.message.from_user.id} fikri: {text}")
            await update.message.reply_text("✅ Fikringiz uchun rahmat! Sizning fikringiz biz uchun muhim.", reply_markup=get_reply_keyboard())
            context.user_data['waiting_for_feedback'] = False
            return

        if text == "📚 Yordam":
            await help_command(update, context)
        elif text == "ℹ️ Bot haqida":
            await about_command(update, context)
        elif text == "📝 Fikr bildirish":
            await feedback_command(update, context)
        elif text == "❓ Savol berish":
            await update.message.reply_text(
                "✍️ Iltimos, savolingizni yozing.",
                reply_markup=get_reply_keyboard()
            )
        else:
            reply = await ask_groq(text)
            await update.message.reply_text(reply[:4000], reply_markup=get_reply_keyboard())

    except Exception as e:
        print(f"Xabarni qayta ishlashda xato: {e}")
        await update.message.reply_text("😢 Xabaringizni qayta ishlashda xato yuz berdi.", reply_markup=get_reply_keyboard())


# Xatoliklarni ushlash
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    try:
        print(f"⚠️ Xato yuz berdi: {context.error}")

        if isinstance(update, Update):
            if update.message:
                await update.message.reply_text("😢 Texnik xato yuz berdi. Iltimos, keyinroq urinib ko'ring.", reply_markup=get_reply_keyboard())
    except Exception as e:
        print(f"Xatoni bartaraf etishda xato: {e}")


# Botni ishga tushirish
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("feedback", feedback_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    print("🤖 Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
