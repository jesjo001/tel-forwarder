from telethon import TelegramClient, events
from telethon.sessions import StringSession
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
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

# Get environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
session_string = os.environ['SESSION_STRING']  # NEW
source_group = os.environ['SOURCE_GROUP']
dest_group = os.environ['DEST_GROUP']

# Use string session instead of file session
client = TelegramClient(StringSession(session_string), api_id, api_hash)

@client.on(events.NewMessage(chats=source_group))
async def handler(event):
    logger.info(f"📨 Message received: {event.text[:100]}...")
    try:
        await event.forward_to(dest_group)
        logger.info("✅ Message forwarded!")
    except Exception as e:
        logger.error(f"❌ Forward error: {e}")

async def telegram_main():
    await client.start()
    logger.info("🤖 Telegram bot connected!")
    
    # Verify groups
    try:
        source_entity = await client.get_entity(source_group)
        dest_entity = await client.get_entity(dest_group)
        logger.info(f"✅ Source: {source_entity.title}")
        logger.info(f"✅ Destination: {dest_entity.title}")
    except Exception as e:
        logger.error(f"❌ Group access failed: {e}")
        return
    
    logger.info("🎯 Listening for messages...")
    await client.run_until_disconnected()

def start_bot():
    asyncio.run(telegram_main())

if __name__ == '__main__':
    logger.info("🚀 Starting bot with string session...")
    
    # Start web server
    web_thread = Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Start Telegram bot
    start_bot()