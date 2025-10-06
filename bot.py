from telethon import TelegramClient, events
import os
import asyncio
from flask import Flask
from threading import Thread
import logging

# Setup detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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
    logger.info(f"🌐 Web server starting on port {port}")
    app.run(host='0.0.0.0', port=port)

# Get environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
source_group = os.environ['SOURCE_GROUP']
dest_group = os.environ['DEST_GROUP']

logger.info(f"🔧 Config - Source: {source_group}, Dest: {dest_group}")

client = TelegramClient('koyeb_session', api_id, api_hash)

async def verify_groups():
    """Verify we can access both groups"""
    try:
        logger.info("🔍 Verifying group access...")
        
        source_entity = await client.get_entity(source_group)
        logger.info(f"✅ Source group: {source_entity.title} (ID: {source_entity.id})")
        
        dest_entity = await client.get_entity(dest_group)
        logger.info(f"✅ Destination group: {dest_entity.title} (ID: {dest_entity.id})")
        
        return True
    except Exception as e:
        logger.error(f"❌ Group verification failed: {e}")
        return False

@client.on(events.NewMessage(chats=source_group))
async def handler(event):
    logger.info(f"📨 MESSAGE RECEIVED!")
    logger.info(f"   From: {event.sender_id}")
    logger.info(f"   Text: {event.text}")
    logger.info(f"   Chat ID: {event.chat_id}")
    
    try:
        await event.forward_to(dest_group)
        logger.info("✅ SUCCESS: Message forwarded!")
    except Exception as e:
        logger.error(f"❌ Forward failed: {e}")

async def telegram_main():
    await client.start()
    logger.info("🤖 Telegram client started!")
    
    me = await client.get_me()
    logger.info(f"🔑 Logged in as: {me.first_name} (ID: {me.id})")
    
    if await verify_groups():
        logger.info("🎯 Starting to listen for messages...")
        logger.info("💡 Send a test message to your source group now!")
        await client.run_until_disconnected()
    else:
        logger.error("🚫 Cannot start listening - group access failed")

def start_bot():
    asyncio.run(telegram_main())

if __name__ == '__main__':
    logger.info("🚀 Starting Telegram forwarder bot...")
    
    # Start web server for health checks
    web_thread = Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Start Telegram bot
    start_bot()