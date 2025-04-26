import os
import requests
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler
)

# .env fayldan tokenlarni yuklash
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def ask_groq(question):
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

def get_inline_keyboard():
    keyboard = [
        [InlineKeyboardButton("📚 Yordam", callback_data="help")],
        [InlineKeyboardButton("ℹ️ Bot haqida", callback_data="about")],
        [InlineKeyboardButton("📝 Fikr bildirish", callback_data="feedback")],
        [InlineKeyboardButton("❓ Savol berish", callback_data="ask")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        reply_markup = get_inline_keyboard()
        
        if update.message:
            await update.message.reply_text(
                "👋 Salom! Men Groq AI yordamida ishlayman.",
                reply_markup=reply_markup
            )
    except Exception as e:
        print(f"/start xatosi: {e}")
        if update.message:
            await update.message.reply_text("😢 Botni ishga tushirib bo'lmadi.")

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
    if update.callback_query:
        await update.callback_query.message.reply_text(help_text, parse_mode="HTML", reply_markup=get_inline_keyboard())
    elif update.message:
        await update.message.reply_text(help_text, parse_mode="HTML", reply_markup=get_inline_keyboard())

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "🤖 <b>Groq AI Bot haqida</b>\n\n"
        "📅 Yaratilgan sana: 2024-yil\n"
        "🧠 AI model: Llama 3-70B (Groq API)\n"
        "⚡ Tezlik: 500+ tok/s\n"
        "👨‍💻 Dasturchi: Ismailov Sarvar(@ismailovsarvarbek)\n\n"
        "Bu bot Groq AI yordamida savollarga javob beradi."
    )
    if update.callback_query:
        await update.callback_query.message.reply_text(about_text, parse_mode="HTML", reply_markup=get_inline_keyboard())
    elif update.message:
        await update.message.reply_text(about_text, parse_mode="HTML", reply_markup=get_inline_keyboard())

async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📝 Iltimos, botimiz haqidagi fikr-mulohazalaringizni yozib qoldiring.\n\n"
        "Har qanday taklif, shikoyat yoki tushuntirish uchun xabar yuboring.\n"
        "Biz sizning fikringizni qadrlaymiz!"
    )
    if update.callback_query:
        await update.callback_query.message.reply_text(msg, reply_markup=get_inline_keyboard())
        context.user_data['waiting_for_feedback'] = True
    elif update.message:
        await update.message.reply_text(msg, reply_markup=get_inline_keyboard())
        context.user_data['waiting_for_feedback'] = True

async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text(
                "Iltimos, savolingizni yozing. Misol: /ask Pythonda ro'yxatni qanday saralash mumkin?",
                reply_markup=get_inline_keyboard()
            )
            return
        
        question = " ".join(context.args)
        reply = ask_groq(question)
        
        # Javob bilan birga tugmalar ham yuboriladi
        await update.message.reply_text(
            reply[:4000],
            reply_markup=get_inline_keyboard()
        )
    except Exception as e:
        print(f"/ask komandasida xato: {e}")
        await update.message.reply_text(
            "😢 Savolingizni qayta ishlashda xato yuz berdi.",
            reply_markup=get_inline_keyboard()
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        
        if query.data == "help":
            await help_command(update, context)
        elif query.data == "about":
            await about_command(update, context)
        elif query.data == "feedback":
            await feedback_command(update, context)
        elif query.data == "ask":
            await ask_command(update, context)
    except Exception as e:
        print(f"Tugma bosishda xato: {e}")
        if update.callback_query and update.callback_query.message:
            await update.callback_query.message.reply_text("😢 Bu amalni bajarib bo'lmadi. Iltimos, /start ni bosing.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if 'waiting_for_feedback' in context.user_data and context.user_data['waiting_for_feedback']:
            print(f"Foydalanuvchi {update.message.from_user.id} fikri: {update.message.text}")
            await update.message.reply_text("✅ Fikringiz uchun rahmat! Sizning fikringiz biz uchun muhim.")
            context.user_data['waiting_for_feedback'] = False
            return
        
        user_input = update.message.text
        reply = ask_groq(user_input)
        await update.message.reply_text(reply[:4000], reply_markup=get_inline_keyboard())
    except Exception as e:
        print(f"Xabar qayta ishlashda xato: {e}")
        if update.message:
            await update.message.reply_text("😢 Xabaringizni qayta ishlashda xato yuz berdi.", reply_markup=get_inline_keyboard())

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    try:
        error_msg = f"⚠️ Xato yuz berdi: {context.error}"
        print(error_msg)
        
        if isinstance(update, Update):
            if update.message:
                await update.message.reply_text("😢 Kechirasiz, texnik nosozlik yuz berdi. Iltimos, keyinroq urinib ko'ring.", reply_markup=get_inline_keyboard())
            elif update.callback_query and update.callback_query.message:
                await update.callback_query.message.reply_text("😢 Kechirasiz, xato yuz berdi. Iltimos, /start ni bosing.", reply_markup=get_inline_keyboard())
    except Exception as e:
        print(f"Xatoni bartaraf etishda xato: {e}")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("ask", ask_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("feedback", feedback_command))
    
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    
    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
