from telethon import TelegramClient, events
import os
import asyncio

# Get credentials from environment
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
source_group = os.getenv('SOURCE_GROUP')
dest_group = os.getenv('DEST_GROUP')

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(chats=source_group))
async def message_handler(event):
    print(f"📨 Received: {event.text}")
    
    # Your simple forwarding logic
    if "important" in event.text.lower():
        await event.forward_to(dest_group)
        print("✅ Forwarded important message!")

async def main():
    await client.start()
    print("🤖 Bot is running forever!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())