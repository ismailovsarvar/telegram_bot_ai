# 🤖 Groq AI Telegram Bot

Bu Telegram bot foydalanuvchilarning savollariga **Groq AI (LLaMA3-70B modeli)** yordamida javob beradi. Bot foydalanuvchi bilan muloqot qiladi, tugmalar orqali yordam beradi va fikr-mulohaza qabul qiladi.

---

## 📦 Loyihada ishlatilgan texnologiyalar

- Python
- `python-telegram-bot` (v20+)
- Groq API
- Dotenv (`.env` orqali maxfiy ma'lumotlar)
- Asinxron funksiyalar (`async/await` bilan)

---

## ⚙️ O‘rnatish

1. Loyihani yuklab oling:
```bash
git clone https://github.com/foydalanuvchi/groq-telegram-bot.git
cd groq-telegram-bot
```

2. Virtual muhit yaratish (ixtiyoriy, lekin tavsiya etiladi):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Zarur kutubxonalarni o‘rnatish:
```bash
pip install -r requirements.txt
```

4. `.env` faylini yarating va quyidagilarni qo‘shing:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Botni ishga tushirish

```bash
python bot.py
```

Ekranda quyidagicha chiqadi:
```
🤖 Bot ishga tushdi...
```

---

## 📌 Foydalanuvchi komandalar

| Komanda     | Tavsifi                                    |
|-------------|---------------------------------------------|
| `/start`    | Botni ishga tushirish va tugmalarni ko‘rsatish |
| `/help`     | Yordam menyusi                              |
| `/about`    | Bot haqida ma'lumot                         |
| `/feedback` | Fikr bildirish imkoniyati                   |
| `/ask`      | Maxsus savol berish (masalan: `/ask Python nima`) |

---

## 💡 Qo‘shimcha

- Tugmalar orqali ham `/help`, `/about`, `/feedback` komandalarini ishlatish mumkin.
- Oddiy xabar yuborilsa, bot avtomatik tarzda Groq AI yordamida javob beradi.
- Fikr-mulohaza yuborilganda `✅ Fikringiz uchun rahmat!` deb javob beradi.

---

## 🧑‍💻 Muallif

**Ismailov Sarvar**  
Telegram: @ismailovsarvarbek (https://t.me/ismailovsarvarbek)

