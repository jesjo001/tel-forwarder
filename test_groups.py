# test_groups.py - Run this in Koyeb console
from telethon import TelegramClient
import os
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test():
    api_id = int(os.environ['API_ID'])
    api_hash = os.environ['API_HASH']
    source_group = os.environ['SOURCE_GROUP']
    dest_group = os.environ['DEST_GROUP']
    
    client = TelegramClient('koyeb_session', api_id, api_hash)
    await client.start()
    
    logger.info("🔍 Testing group access...")
    
    try:
        # Test source group
        source = await client.get_entity(source_group)
        logger.info(f"✅ Source: {source.title} (ID: {source.id})")
        
        # Check if we have permission to read messages
        participant = await client.get_permissions(source, await client.get_me())
        logger.info(f"📖 Read permissions: {participant}")
        
    except Exception as e:
        logger.error(f"❌ Source group error: {e}")
    
    try:
        # Test destination group
        dest = await client.get_entity(dest_group)
        logger.info(f"✅ Destination: {dest.title} (ID: {dest.id})")
        
        # Check if we can send messages
        participant = await client.get_permissions(dest, await client.get_me())
        logger.info(f"📝 Send permissions: {participant}")
        
    except Exception as e:
        logger.error(f"❌ Destination group error: {e}")
    
    await client.disconnect()

asyncio.run(test())