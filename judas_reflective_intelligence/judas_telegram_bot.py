import os
import telebot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AUTHORIZED_USER = int(os.getenv("TELEGRAM_USER_ID"))

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.from_user.id != AUTHORIZED_USER:
        return
    bot.reply_to(message, "🧠 Judas is listening. Available commands:\n/rebalance\n/retry\n/status")

@bot.message_handler(commands=['rebalance'])
def handle_rebalance(message):
    if message.from_user.id != AUTHORIZED_USER:
        return
    os.system("python rebalance_scheduler.py")
    bot.reply_to(message, "✅ Rebalance triggered.")

@bot.message_handler(commands=['retry'])
def handle_retry(message):
    if message.from_user.id != AUTHORIZED_USER:
        return
    os.system("python retry_pending.py")
    bot.reply_to(message, "🔁 Retry of pending IPFS archives triggered.")

@bot.message_handler(commands=['status'])
def handle_status(message):
    if message.from_user.id != AUTHORIZED_USER:
        return
    bot.reply_to(message, "📊 Judas is online and operational. All systems listening.")

print("🤖 Judas Telegram Bot is running...")
bot.infinity_polling()