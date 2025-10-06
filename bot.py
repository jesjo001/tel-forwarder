from telethon import TelegramClient, events
import os
import asyncio
from flask import Flask
from threading import Thread
import time

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

@client.on(events.NewMessage(chats=source_group))
async def handler(event):
    print(f"📨 Message received")
    try:
        await event.forward_to(dest_group)
        print("✅ Message forwarded!")
    except Exception as e:
        print(f"❌ Forward error: {e}")

async def connect_with_retry():
    max_retries = 5
    retry_delay = 10  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"🔄 Connection attempt {attempt + 1}/{max_retries}...")
            await client.start()
            print("✅ Connected to Telegram!")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                print("🚫 All connection attempts failed")
                return False

async def telegram_main():
    if await connect_with_retry():
        print("🤖 Telegram bot connected!")
        print(f"👂 Listening to: {source_group}")
        print(f"📤 Forwarding to: {dest_group}")
        await client.run_until_disconnected()
    else:
        print("💡 Tips: Try a different hosting provider or check if Telegram is blocking this IP")

def start_bot():
    asyncio.run(telegram_main())

if __name__ == '__main__':
    print("🚀 Starting bot...")
    
    # Start web server
    web_thread = Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Start Telegram bot
    start_bot()