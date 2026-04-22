import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import subprocess
import os
from pathlib import Path

# Bot Token من @BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # احصل عليه من @BotFather


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 BEKO Agent جاهز!\nأرسل أمر مثل:\nRUN PRODUCT INTELLIGENCE حقائب جلدية"
    )


async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text

    # Write goal
    goal_file = Path("goal.txt")
    goal_file.write_text(cmd)

    # Run BEKO
    process = subprocess.Popen(
        ["python", "beko-agent-main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    await update.message.reply_text("🚀 BEKO يشتغل... انتظر النتيجة")

    # Get result
    stdout, stderr = process.communicate()
    result = stdout.decode() if stdout else "تم!"

    await update.message.reply_text(f"✅ تم الإنجاز!\n{result[:2000]}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_command))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
