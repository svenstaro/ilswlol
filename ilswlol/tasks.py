import os

from uwsgidecorators import spool
from werkzeug.contrib.cache import UWSGICache
from telethon import TelegramClient, events
from telethon.errors.rpc_error_list import FloodWaitError

cache = UWSGICache(default_timeout=10 * 60)

client = TelegramClient('telegram_client', os.environ['TG_API_ID'], os.environ['TG_API_HASH'],
                        update_workers=1)
if not client.connect():
    raise RuntimeError("Couldn't connect to Telegram. Check network and credentials.")
lukas_id = client.get_entity('lukasovich').id

@client.on(events.UserUpdate)
def update_callback(event):
    if not lukas_id:
        raise RuntimeError("lukas_id is not set properly!")

    if event.user_id == lukas_id:
        if event.online:
            date = datetime.utcnow()
            logging.info("Received push update: Currently online in Telegram.")
        if event.last_seen:
            date = event.status.was_online
            human_delta = humanize.naturaltime(datetime.utcnow() - date)
            logging.info(f"Received push update: Last seen in Telegram at {date}"
                         f"({human_delta}).")
        cache.set('last_online_datetime_telegram', date)


