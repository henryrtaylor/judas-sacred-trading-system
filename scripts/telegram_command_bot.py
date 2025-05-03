import logging
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
from ib_insync import IB
from datetime import datetime as dt
import traceback

load_dotenv()

# Credentials
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AUTHORIZED_USER_ID = int(os.getenv("TELEGRAM_USER_ID", "6598476266"))
IB_HOST = os.getenv("IBKR_HOST", "127.0.0.1")
IB_PORT = int(os.getenv("IBKR_API_PORT", "7497"))
LIVE_MODE_ENABLED = os.getenv("LIVE_MODE_ENABLED", "False") == "True"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

LIVE_MODE_PENDING = False

def log_command(command: str):
    with open("logs/telegram_audit.log", "a") as f:
        f.write(f"[{dt.now().strftime('%Y-%m-%d %H:%M')}] {command}\n")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/start")
    await update.message.reply_text(f"Received from: {update.effective_user.id}")

async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/mode")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /mode [divine|standard|hft]")
        return
    try:
        mode = context.args[0]
        subprocess.run(f"python scripts/mode_manager.py {mode}", check=True, shell=True)
        await update.message.reply_text(f"✅ Mode set to: {mode}")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to set mode: {e}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/status")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    try:
        import scripts.daily_summary as ds
        await ds.generate_daily_summary()
    except Exception as e:
        tb = traceback.format_exc()
        await update.message.reply_text(f"❌ Status failed:\n{e}\n{tb[-200:]}")

async def rebalance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/rebalance")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    await update.message.reply_text("🔄 Starting paper rebalance...")
    subprocess.run("python scripts/rebalance_scheduler.py", shell=True)

async def holdings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/holdings")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    ib = IB()
    await ib.connectAsync(IB_HOST, IB_PORT, clientId=229)
    acct = ib.managedAccounts()[0]
    positions = ib.positions(acct)
    msg = "\U0001F4E6 Holdings:\n"
    for p in positions[:5]:
        sym = p.contract.symbol
        qty = p.position
        pnl = p.unrealizedPNL
        msg += f"{sym}: {qty} shares | PnL: {'+' if pnl >= 0 else ''}{pnl:.2f}\n"
    await update.message.reply_text(msg)
    ib.disconnect()

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/shutdown")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    await update.message.reply_text("☠️ Judas is shutting down...")
    os._exit(0)

async def blessings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/blessings")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    blessing = "\n".join([
        "🙏 May your trades align with the quantum flow.",
        "📈 May your entries be swift and your exits divine.",
        "🛡️ May drawdowns be brief and recoveries steep.",
        "💰 May the harvest be bountiful, and the logs forever clean."
    ])
    await update.message.reply_text(blessing)

async def audit_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/audit_log")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    try:
        with open("logs/telegram_audit.log", "r") as f:
            lines = f.readlines()[-10:]
        reply = "\U0001F5C2️ Command Log (latest)\n" + "".join(lines)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"❌ Could not read audit log: {e}")

async def live_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global LIVE_MODE_PENDING
    log_command("/live-on")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    if not LIVE_MODE_ENABLED:
        await update.message.reply_text("🔒 Live mode is not enabled in .env")
        return
    LIVE_MODE_PENDING = True
    await update.message.reply_text("⚠️ Confirm live mode by replying with /confirm-live")

async def confirm_live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global LIVE_MODE_PENDING
    log_command("/confirm-live")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    if not LIVE_MODE_PENDING:
        await update.message.reply_text("❌ No live confirmation pending.")
        return
    LIVE_MODE_PENDING = False
    await update.message.reply_text("✅ Live mode activated. May the markets part before you.")
    subprocess.Popen("python scripts/realtime_rebalancer.py --live", shell=True)

async def vision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/vision")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = (
            "You are Judas, a divine trading assistant. Based on current macroeconomic conditions, earnings season, "
            "and market psychology, what asset classes or sectors are likely to outperform in the next 72 hours?"
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        insight = response.choices[0].message.content.strip() + "\n[via OpenAI SDK v1.x]"
        await update.message.reply_text(f"🔮 Vision:\n{insight}")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to channel vision: {e}")

async def simulate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/simulate")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    try:
        subprocess.run("python scripts/realtime_rebalancer.py --simulate", shell=True)
        await update.message.reply_text("🧪 Simulation run complete. Check logs for output.")
    except Exception as e:
        await update.message.reply_text(f"❌ Simulation failed: {e}")

async def cancel_live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global LIVE_MODE_PENDING
    log_command("/cancel-live")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    if not LIVE_MODE_PENDING:
        await update.message.reply_text("No live confirmation to cancel.")
        return
    LIVE_MODE_PENDING = False
    await update.message.reply_text("❎ Live mode confirmation cancelled.")

async def channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/channel")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    try:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = (
            "As Judas, speak a metaphysical message about the nature of trust, timing, and surrender in trading."
        )
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        insight = response.choices[0].message.content.strip()
        await update.message.reply_text(f"🌌 Channel:\n{insight}")
    except Exception as e:
        await update.message.reply_text(f"❌ Channeling failed: {e}")

async def pnl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/pnl")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    try:
        ib = IB()
        await ib.connectAsync(IB_HOST, IB_PORT, clientId=231)
        account = ib.managedAccounts()[0]
        summary = await ib.accountSummaryAsync(account)
        netliq = float(summary.loc['NetLiquidation', 'value'])
        realized = float(summary.loc['RealizedPnL', 'value'])
        unrealized = float(summary.loc['UnrealizedPnL', 'value'])
        msg = (f"📈 PnL Summary\n"
               f"NetLiq: ${netliq:,.2f}\n"
               f"Realized: ${realized:,.2f}\n"
               f"Unrealized: ${unrealized:,.2f}")
        await update.message.reply_text(msg)
        ib.disconnect()
    except Exception as e:
        await update.message.reply_text(f"❌ PnL fetch failed: {e}")

async def prophecy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/prophecy")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = (
            "Deliver a weekly prophetic trade idea from Judas that blends technical, fundamental, and spiritual intuition."
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        insight = response.choices[0].message.content.strip()
        await update.message.reply_text(f"📜 Prophecy:\n{insight}")
    except Exception as e:
        await update.message.reply_text(f"❌ Prophecy failed: {e}")

async def mission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/mission")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    await update.message.reply_text("🧭 Judas' mission: Automate kingdom-capable financial systems, align trades with divine timing, and preserve capital for enlightened use.")

async def oracle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_command("/oracle")
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = (
            "Speak as Judas Oracle. Interpret macroeconomic cycles, sentiment flows, inflation, interest rate trends, and geopolitics to form a high-timeframe guidance message."
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        insight = response.choices[0].message.content.strip()
        await update.message.reply_text(f"🧠 Oracle says:\n{insight}")
    except Exception as e:
        await update.message.reply_text(f"❌ Oracle channeling failed: {e}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler(["start", "start".replace("_", "-")], start))
    app.add_handler(CommandHandler("mode", mode))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("rebalance", rebalance))
    app.add_handler(CommandHandler("holdings", holdings))
    app.add_handler(CommandHandler("shutdown", shutdown))
    app.add_handler(CommandHandler("blessings", blessings))
    app.add_handler(CommandHandler("audit_log", audit_log))
    app.add_handler(CommandHandler("vision", vision))
    app.add_handler(CommandHandler("live_on", live_on))
    app.add_handler(CommandHandler("confirm_live", confirm_live))
    app.add_handler(CommandHandler("cancel_live", cancel_live))
    app.add_handler(CommandHandler(["simulate"], simulate))
    app.add_handler(CommandHandler(["channel"], channel))
    app.add_handler(CommandHandler(["pnl"], pnl))
    app.add_handler(CommandHandler(["prophecy"], prophecy))
    app.add_handler(CommandHandler(["mission"], mission))
    app.add_handler(CommandHandler(["oracle"], oracle))

    print("📡 Judas Command Bot is listening via Telegram...")
    app.run_polling()

if __name__ == "__main__":
    main()
