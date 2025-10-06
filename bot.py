from telethon import TelegramClient, events
import os
import asyncio
from flask import Flask
from threading import Thread
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Forwarder Bot is Running!"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/test')
def test():
    return "Bot is healthy and running!"

def run_web_server():
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🌐 Web server starting on port {port}")
    app.run(host='0.0.0.0', port=port)

# Get environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
source_group = os.environ['SOURCE_GROUP']
dest_group = os.environ['DEST_GROUP']

logger.info(f"🔧 Config loaded: Source={source_group}, Dest={dest_group}")

# Initialize Telegram client
client = TelegramClient('render_session', api_id, api_hash)

async def verify_environment():
    """Verify we can access everything needed"""
    try:
        logger.info("🔍 Verifying environment...")
        
        # Test Telegram connection
        me = await client.get_me()
        logger.info(f"✅ Connected as: {me.first_name}")
        
        # Test source group access
        source_entity = await client.get_entity(source_group)
        logger.info(f"✅ Source group: {source_entity.title}")
        
        # Test destination group access  
        dest_entity = await client.get_entity(dest_group)
        logger.info(f"✅ Destination group: {dest_entity.title}")
        
        logger.info("🎉 All checks passed! Bot is ready.")
        return True
        
    except Exception as e:
        logger.error(f"❌ Environment verification failed: {e}")
        logger.info("💡 Make sure:")
        logger.info("   - Your account is in both groups")
        logger.info("   - Group IDs are correct") 
        logger.info("   - You've authenticated properly")
        return False

@client.on(events.NewMessage(chats=source_group))
async def message_handler(event):
    """Handle new messages from source group"""
    try:
        logger.info(f"📨 Received message: {event.text[:100]}...")
        
        # Forward the message
        await event.forward_to(dest_group)
        logger.info("✅ Message forwarded successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to forward message: {e}")

async def start_telegram_client():
    """Start and maintain Telegram connection"""
    await client.start()
    logger.info("🤖 Telegram client started successfully!")
    
    if await verify_environment():
        logger.info("👂 Starting to listen for messages...")
        logger.info("💡 Send a message to your source group to test!")
        await client.run_until_disconnected()
    else:
        logger.error("🚫 Cannot start due to environment issues")

def main():
    """Main application entry point"""
    logger.info("🚀 Starting Telegram Forwarder Bot on Render...")
    
    # Start web server in background thread for health checks
    web_thread = Thread(target=run_web_server, daemon=True)
    web_thread.start()
    logger.info("✅ Web server started for health checks")
    
    # Start Telegram client
    try:
        asyncio.run(start_telegram_client())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")

if __name__ == '__main__':
    main()