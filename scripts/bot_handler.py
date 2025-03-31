import os
import logging
import json
import subprocess
import datetime
import psutil
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPEN_WEBUI_URL = os.getenv("OPEN_WEBUI_URL")  # Example: "http://localhost:5001/api/chat"

# Ensure required environment variables are set
if not BOT_TOKEN or not OPEN_WEBUI_URL:
    raise ValueError("Error: Required environment variables not set. Ensure TELEGRAM_BOT_TOKEN and OPEN_WEBUI_URL are configured.")

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# File Paths
DATA_DIR = "/data/data/com.termux/files/home/NohvaraContinuumOS/data"
CHECKIN_FILE = f"{DATA_DIR}/checkin_log.json"
TIMECOIN_FILE = f"{DATA_DIR}/timecoin_log.json"
NOBLE_FILE = f"{DATA_DIR}/noble_system.json"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# --- SYSTEM FUNCTIONS ---

# Command: /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("🔹 **NohvaraContinuum OS Bot Activated** 🔹\nUse /help for available commands.")

# Command: /help
async def help_command(update: Update, context: CallbackContext):
    help_text = ("🔹 **NohvaraContinuum OS Commands** 🔹\n\n"
                 "/checkin - Log daily system check-in\n"
                 "/timecoin - View earned Time Coins\n"
                 "/noble - View Noble System progress\n"
                 "/status - Monitor system performance\n"
                 "/forecast - AI-powered decision forecasting\n"
                 "/ask <query> - Ask Open-WebUI anything\n"
                 "/update - Sync latest Git updates\n")
    await update.message.reply_text(help_text)

# Command: /checkin
async def checkin(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Load check-in data
    checkin_data = {}
    if os.path.exists(CHECKIN_FILE):
        with open(CHECKIN_FILE, "r") as file:
            checkin_data = json.load(file)

    # Log check-in
    checkin_data[user_id] = {"last_checkin": now}
    with open(CHECKIN_FILE, "w") as file:
        json.dump(checkin_data, file, indent=4)

    await update.message.reply_text(f"✅ **Check-in Successful:** {now}")

# Command: /timecoin
async def timecoin(update: Update, context: CallbackContext):
    if os.path.exists(TIMECOIN_FILE):
        with open(TIMECOIN_FILE, "r") as file:
            timecoin_data = json.load(file)
        await update.message.reply_text(f"🔹 **Time Coins Earned:** {timecoin_data.get('coins', 0)}")
    else:
        await update.message.reply_text("⏳ No Time Coin data found.")

# Command: /noble
async def noble(update: Update, context: CallbackContext):
    if os.path.exists(NOBLE_FILE):
        with open(NOBLE_FILE, "r") as file:
            noble_data = json.load(file)
        progress = noble_data.get("progress", "Foot Soldier Level 1")
        await update.message.reply_text(f"🔹 **Noble System Progress:** {progress}")
    else:
        await update.message.reply_text("⏳ No Noble System data found.")

# Command: /status
async def system_status(update: Update, context: CallbackContext):
    uptime = subprocess.getoutput("uptime -p")
    cpu_usage = psutil.cpu_percent(interval=1)
    mem_info = psutil.virtual_memory()
    memory_usage = f"{mem_info.percent}% used"

    status_msg = (f"🔹 **System Status** 🔹\n"
                  f"⏳ **Uptime:** {uptime}\n"
                  f"⚙️ **CPU Usage:** {cpu_usage}%\n"
                  f"💾 **Memory:** {memory_usage}")

    await update.message.reply_text(status_msg)

# Command: /forecast (AI-powered decision-making)
async def forecast(update: Update, context: CallbackContext):
    user_input = "Predict my best course of action for today based on my system logs."
    
    response = requests.post(
        OPEN_WEBUI_URL,
        json={"message": user_input}
    )
    
    if response.status_code == 200:
        ai_response = response.json().get("reply", "No response from AI.")
        await update.message.reply_text(f"🔮 **AI Forecast:**\n{ai_response}")
    else:
        await update.message.reply_text("⚠️ Error fetching forecast.")

# Command: /ask (General AI queries)
async def ask(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("🔹 Usage: `/ask <question>`")
        return

    user_query = " ".join(context.args)
    
    response = requests.post(
        OPEN_WEBUI_URL,
        json={"message": user_query}
    )
    
    if response.status_code == 200:
        ai_response = response.json().get("reply", "No response from AI.")
        await update.message.reply_text(f"🤖 **AI Response:**\n{ai_response}")
    else:
        await update.message.reply_text("⚠️ Error communicating with AI.")

# Command: /update
async def update_system(update: Update, context: CallbackContext):
    await update.message.reply_text("🔄 Syncing system updates from Git...")
    subprocess.run(["bash", "/data/data/com.termux/files/home/NohvaraContinuumOS/scripts/auto_git_sync.sh"])
    await update.message.reply_text("✅ System updated successfully!")

# --- BOT SETUP ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("checkin", checkin))
    app.add_handler(CommandHandler("timecoin", timecoin))
    app.add_handler(CommandHandler("noble", noble))
    app.add_handler(CommandHandler("status", system_status))
    app.add_handler(CommandHandler("forecast", forecast))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("update", update_system))

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
