# bot.py for Render
from telethon import TelegramClient, events
import os
import asyncio
from flask import Flask
from threading import Thread
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Bot is Running!"

@app.route('/health')
def health():
    return "OK", 200

def run_web_server():
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🌐 Web server on port {port}")
    app.run(host='0.0.0.0', port=port)

# Get environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
source_group = os.environ['SOURCE_GROUP']
dest_group = os.environ['DEST_GROUP']

client = TelegramClient('render_session', api_id, api_hash)

@client.on(events.NewMessage(chats=source_group))
async def handler(event):
    logger.info(f"📨 Message received")
    try:
        await event.forward_to(dest_group)
        logger.info("✅ Message forwarded!")
    except Exception as e:
        logger.error(f"❌ Forward error: {e}")

async def telegram_main():
    await client.start()
    logger.info("🤖 Telegram bot connected!")
    logger.info(f"👂 Listening to: {source_group}")
    logger.info(f"📤 Forwarding to: {dest_group}")
    await client.run_until_disconnected()

def start_bot():
    asyncio.run(telegram_main())

if __name__ == '__main__':
    logger.info("🚀 Starting on Render...")
    
    # Start web server
    web_thread = Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Start Telegram bot
    start_bot()