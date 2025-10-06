# koyeb_auth.py - Run this in Koyeb console
from telethon import TelegramClient
import os
import asyncio

async def main():
    api_id = int(os.environ['API_ID'])
    api_hash = os.environ['API_HASH']
    
    print("🔐 Starting Telegram authentication...")
    print("This will ask for your phone number and verification code.")
    
    client = TelegramClient('koyeb_session', api_id, api_hash)
    await client.start()
    
    me = await client.get_me()
    print(f"✅ Successfully authenticated as: {me.first_name}")
    print("📁 Session file 'koyeb_session.session' has been created!")
    
    # Test group access
    try:
        source_group = os.environ['SOURCE_GROUP']
        source_entity = await client.get_entity(source_group)
        print(f"✅ Can access source group: {source_entity.title}")
    except Exception as e:
        print(f"❌ Cannot access source group: {e}")
    
    try:
        dest_group = os.environ['DEST_GROUP']
        dest_entity = await client.get_entity(dest_group)
        print(f"✅ Can access destination group: {dest_entity.title}")
    except Exception as e:
        print(f"❌ Cannot access destination group: {e}")
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())