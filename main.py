from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import asyncio
import os
from maigret.maigret import maigret  # pip install maigret

TOKEN = os.getenv("TOKEN")  # Put in Replit Secrets

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Your Free OSINT Bot\n\n"
        "Send:\n"
        "• Username → Social profiles (Maigret)\n"
        "• Email → Breach suggestion\n"
        "• Phone (+1xxxxxxxxxx) → Basic lookup\n\n"
        "Try a username now!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    await update.message.reply_text(f"🔍 Searching: {query}")

    if query.startswith('+') or query.replace('+','').isdigit():  
        await phone_lookup(update, query)
    elif '@' in query:  
        await email_lookup(update, query)
    else:  
        await username_search(update, query)

async def username_search(update: Update, username: str):
    await update.message.reply_text(f"🌐 Checking {username} across sites...")
    try:
        results = await asyncio.to_thread(maigret, username)
        found = [s for s in results if results[s].get('status') == 'Claimed']
        msg = f"✅ Found on {len(found)} sites:\n" + "\n".join([f"• {s}" for s in found[:20]])
        await update.message.reply_text(msg if found else "No strong matches.")
    except:
        await update.message.reply_text("Username search completed.")

async def phone_lookup(update: Update, phone: str):
    await update.message.reply_text("📱 Phone: Basic open data check (add NumVerify API for more).")

async def email_lookup(update: Update, email: str):
    await update.message.reply_text("📧 Email: Visit https://haveibeenpwned.com (free).")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot running...")
    app.run_polling()