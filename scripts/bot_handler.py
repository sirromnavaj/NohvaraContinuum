#!/usr/bin/env python3
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Load token from environment variable
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN not found.")
    exit(1)

bot = telegram.Bot(token=BOT_TOKEN)

def start(update, context):
    update.message.reply_text("🔥 Nohvara Continuum Bot Active!")

def sync_git(update, context):
    os.system("$HOME/NohvaraContinuum/scripts/auto_git_sync.sh")
    update.message.reply_text("✅ Git repo synced!")

def unknown(update, context):
    update.message.reply_text("⚠️ Unknown command. Use /sync to sync Git.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("sync", sync_git))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
