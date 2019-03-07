"""Module for updating and querying the last_seen status of Lukas from telegram."""
import os
import logging
import humanize
import asyncio
from datetime import datetime, timedelta
from aiocache import SimpleMemoryCache, cached
from telethon import TelegramClient
from telethon.errors.rpcbaseerrors import FloodError
from telethon.events import UserUpdate
from telethon.tl.types import (
    UserStatusOnline,
    UserStatusOffline,
)
from dotenv import load_dotenv

loop = asyncio.get_event_loop()

load_dotenv(verbose=True)

client = TelegramClient(
    'telegram_client',
    os.environ['TG_API_ID'],
    os.environ['TG_API_HASH'],
    loop=loop,
)

cache = SimpleMemoryCache()


async def get_telegram_confidence():
    """Get last seen status from telethon and calculate the confidence of him being awake."""
    date = None

    date = await get_last_seen()
    logging.info(f"Fetched Telegram last online from cache: {date}")

    delta = datetime.now(date.tzinfo) - date

    # Check whether Lukas has been online in Telegram recently and assign confidence.
    if delta < timedelta(minutes=5):
        confidence = 70
    elif delta < timedelta(minutes=45):
        confidence = 50
    elif delta < timedelta(hours=1):
        confidence = 40
    elif delta < timedelta(hours=3):
        confidence = 30
    elif delta < timedelta(hours=7):
        confidence = 20
    else:
        confidence = 0

    return confidence


@cached(key="telegram", ttl=600)
async def get_last_seen():
    """Get the last_seen status from cache or query it manually."""
    # The cache expired and we are forced to query manually
    cooldown_is_active = await cache.get("telegram_cooldown", default=False)
    if cooldown_is_active:
        logging.info("Telegram cache has expired but Telegram API request cooldown is active. Assuming lukas was never online")
        return datetime.min

    logging.info("Telegram cache has expired, fetching fresh data.")
    try:
        lukas = await client.get_entity('lukasovich')
    except FloodError:
        logging.critical("Too many Telegram API requests, engaging cooldown")
        await cache.set("telegram_cooldown", True, ttl=3600)
        raise RuntimeError("Too many Telegram API requests")

    # Check whether he is online right now or get the last_seen status.
    if isinstance(lukas.status, UserStatusOnline):
        date = datetime.utcnow()
        logging.info("Currently online in Telegram.")
    elif isinstance(lukas.status, UserStatusOffline):
        date = lukas.status.was_online
        human_delta = humanize.naturaltime(datetime.now(date.tzinfo) - date)
        logging.info(f"Last seen in Telegram at {date} ({human_delta}).")
    else:
        raise RuntimeError("Lukas changed his privacy settings. We are fucked.")

    return date


async def update_callback(update):
    """Subscribe on UserUpdate event.

    We filter for Lukas's id and save the last_seen time in the cache.
    """
    lukas_id = await cache.get("lukas_id")
    logging.info(f"Retrieved lukas_id: {lukas_id}")
    if not lukas_id:
        raise RuntimeError("lukas_id is not set properly!")

    if update.user_id == lukas_id:
        if update.online:
            date = datetime.utcnow()
            logging.info("Received push update: Currently online in Telegram.")
        else:
            date = update.last_seen
            human_delta = humanize.naturaltime(datetime.now(date.tzinfo) - update.last_seen)
            logging.info(f"Received push update: Last seen in Telegram at {date}"
                          f"({human_delta}).")
        await cache.set("telegram", date, ttl=600)


async def init_telegram():
    """Initialize some Telegram stuff."""
    # Check whether we are able to connect to telegram
    await client.connect()
    if not await client.is_user_authorized():
        raise RuntimeError("User is not authorized. Check network and credentials.")

    # We need to query lukas's ID once so we are able to filter UserUpdates later on.
    lukas = await client.get_entity('lukasovich')
    await cache.set("lukas_id", lukas.id)
    logging.info(f"Setting lukas_id to {lukas.id}")

loop.run_until_complete(init_telegram())
client.add_event_handler(update_callback, UserUpdate)
