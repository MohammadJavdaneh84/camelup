from tel import api
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# حالت‌ها رو برای هر کاربر ذخیره می‌کنیم
user_states = {}



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # اگر اولین بارشه که پیام می‌ده، مقادیر اولیه رو ست کن
    if user_id not in user_states:
        user_states[user_id] = {
            "request": "/start",
            "status": {
                "position": {
                    "blue": 0,
                    "green": -1,
                    "red": -2,
                    "yellow": -3,
                    "white": -4,
                    "pond": [],
                    "desert": []
                },
                "DiceRolled": {
                    "blue": False,
                    "green": False,
                    "red": False,
                    "yellow": False,
                    "white": False
                }
            }
        }

    # استفاده از ورودی جدید به عنوان request
    user_states[user_id]["request"] = text
    request = user_states[user_id]["request"]
    status = user_states[user_id]["status"]

    # صدا زدن تابع api
    response = api(request, status)
    answer = response["answer"]
    user_states[user_id]["status"] = response["status"]

    # ارسال پاسخ
    await update.message.reply_text(answer)

# راه‌اندازی ربات
def main():
    app = ApplicationBuilder().token("8312118898:AAEuakt9CL1Rlgy3pG52237ecNjQxQZ-A6Y").build()

    message_handler = MessageHandler(filters.TEXT, handle_message)
    app.add_handler(message_handler)

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
