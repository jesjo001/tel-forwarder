from telethon import TelegramClient, events
import os
import asyncio
from flask import Flask
from threading import Thread
import logging

# Setup logging
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
source_group = os.environ['SOURCE_GROUP']
dest_group = os.environ['DEST_GROUP']

client = TelegramClient('koyeb_session', api_id, api_hash)

async def check_environment():
    """Check if we have everything needed"""
    logger.info("🔧 Checking environment...")
    
    try:
        # Test if we can access the groups
        source_entity = await client.get_entity(source_group)
        logger.info(f"✅ Source group: {source_entity.title}")
        
        dest_entity = await client.get_entity(dest_group)
        logger.info(f"✅ Destination group: {dest_entity.title}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Environment check failed: {e}")
        logger.info("💡 Run the authentication script in Koyeb console first!")
        return False

@client.on(events.NewMessage(chats=source_group))
async def handler(event):
    logger.info("📨 Message received")
    try:
        await event.forward_to(dest_group)
        logger.info("✅ Message forwarded!")
    except Exception as e:
        logger.error(f"❌ Forward error: {e}")

async def telegram_main():
    await client.start()
    logger.info("🤖 Telegram bot connected!")
    
    if await check_environment():
        logger.info("🎯 Starting to listen for messages...")
        await client.run_until_disconnected()
    else:
        logger.error("🚫 Cannot start - environment check failed")

def start_bot():
    asyncio.run(telegram_main())

if __name__ == '__main__':
    logger.info("🚀 Starting bot...")
    
    # Start web server for health checks
    web_thread = Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Start Telegram bot
    start_bot()