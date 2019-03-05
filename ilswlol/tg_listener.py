from telethon import TelegramClient
from telethon.tl.types import UserStatusOnline, UpdateUserStatus
from telethon.errors.rpc_error_list import FloodWaitError

def update_callback(update):
    if not lukas_id:
        raise RuntimeError("lukas_id is not set properly!")

    if isinstance(update, UpdateUserStatus) and update.user_id == lukas_id:
        if isinstance(update.status, UserStatusOnline):
            date = datetime.utcnow()
            logging.debug("Received push update: Currently online in Telegram.")
        else:
            date = update.status.was_online
            human_delta = humanize.naturaltime(datetime.utcnow() - date)
            logging.debug(f"Received push update: Last seen in Telegram at {date}"
                          f"({human_delta}).")
        cache.set('last_online_datetime_telegram', date)


client = TelegramClient('telegram_client', os.environ['TG_API_ID'], os.environ['TG_API_HASH'],
                        update_workers=4)
lukas_id = client.get_entity('lukasovich', force_fetch=True).id
client.add_update_handler(update_callback)
if not client.connect():
    raise RuntimeError("Couldn't connect to Telegram. Check network and credentials.")


logging.basicConfig(level='DEBUG', format='%(asctime)s %(levelname)s:%(name)s - %(message)s')


