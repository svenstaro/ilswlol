import os
import logging
import humanize
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.tl.types import UserStatusOnline, UpdateUserStatus, PeerUser
from telethon.errors.rpcbaseerrors import FloodError
from telethon.events import UserUpdate

from ilswlol.uswgi import cache

client = TelegramClient(
    'telegram_client',
    os.environ['TG_API_ID'],
    os.environ['TG_API_HASH'],
    update_workers=4
)
# Check whether we are able to connect to telegram
if not client.connect():
    raise RuntimeError("Couldn't connect to Telegram. Check network and credentials.")

# We need to query lukas's ID once so we are able to filter UserUpdates later on.
lukas_id = client.get_entity('lukasovich', force_fetch=True).id
if not lukas_id:
    raise RuntimeError("lukas_id is not set properly!")


async def get_telegram_confidence():
    """Get last seen status from telethon and calculate the confidence of him being awake."""
    date = None

    last_online_datetime_telegram = cache.get('last_online_datetime_telegram')
    if last_online_datetime_telegram is None:
        logging.info("Telegram cache has expired, fetching fresh data.")
        try:
            lukas = await client.get_entity('lukasovich', force_fetch=True)
        except FloodError:
            logging.critical("Too many Telegram API requests!")

        if isinstance(lukas.status, UserStatusOnline):
            date = datetime.utcnow()
            logging.debug("Currently online in Telegram.")
        else:
            date = lukas.status.was_online
            human_delta = humanize.naturaltime(datetime.utcnow() - date)
            logging.debug(f"Last seen in Telegram at {date} ({human_delta}).")
        cache.set('last_online_datetime_telegram', date)
    else:
        date = last_online_datetime_telegram
        logging.info(f"Fetched Telegram last online from cache: {date}")

    delta = datetime.utcnow() - date

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


def update_callback(update):
    """Subscribe on UserUpdate event.

    We filter for Lukas's id and save the last_seen time in the cache.
    """
    if update.user_id == lukas_id:
        if update.online:
            date = datetime.utcnow()
            logging.debug("Received push update: Currently online in Telegram.")
        else:
            date = update.last_seen
            human_delta = humanize.naturaltime(datetime.utcnow() - update.last_seen)
            logging.debug(f"Received push update: Last seen in Telegram at {date}"
                          f"({human_delta}).")
        cache.set('last_online_datetime_telegram', date)


client.add_event_handler(update_callback, UserUpdate)
