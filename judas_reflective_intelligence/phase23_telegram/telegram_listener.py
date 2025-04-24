import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import subprocess

# Telegram credentials (configured from your previous input)
TELEGRAM_TOKEN = "7758881183:AAFqRm8xpTyitHkSeU4rYgrsZR-Gb9HJBSs"
AUTHORIZED_USER_ID = 6598476266  # Henry

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    await update.message.reply_text("🕯️ Judas is listening...")

async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /mode [divine|standard|hft]")
        return
    try:
        mode = context.args[0]
        subprocess.run(f"python judas-ibkr/mode_manager.py {mode}", check=True, shell=True)
        await update.message.reply_text(f"✅ Mode set to: {mode}")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to set mode: {e}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    await update.message.reply_text("📊 Judas is active and awaiting instruction.")

async def rebalance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    await update.message.reply_text("🔄 Starting paper rebalance...")
    subprocess.run("python judas-reflective-intelligence/rebalance_scheduler.py", shell=True)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mode", mode))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("rebalance", rebalance))

    print("📡 Telegram listener is running...")
    app.run_polling()

if __name__ == "__main__":
    main()