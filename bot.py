from telethon import TelegramClient, events
import os
import asyncio
from flask import Flask
from threading import Thread

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

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(chats=source_group))
async def handler(event):
    print(f"📨 Message received from {source_group}")
    try:
        await event.forward_to(dest_group)
        print("✅ Message forwarded!")
    except Exception as e:
        print(f"❌ Forward error: {e}")

async def telegram_main():
    await client.start()
    print("🤖 Telegram bot connected!")
    print(f"👂 Listening to: {source_group}")
    print(f"📤 Forwarding to: {dest_group}")
    await client.run_until_disconnected()

def start_bot():
    asyncio.run(telegram_main())

if __name__ == '__main__':
    print("🚀 Starting bot...")
    print(f"Source: {source_group}")
    print(f"Destination: {dest_group}")
    
    # Start web server
    web_thread = Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Start Telegram bot
    start_bot()