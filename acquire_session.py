import logging
import os
import getpass
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

logging.basicConfig(level=logging.INFO)


# Initialize Telegram
logging.info("Connecting to Telegram...")
client = TelegramClient('telegram_client', os.environ['TG_API_ID'], os.environ['TG_API_HASH'])
client.connect()
logging.info("Logging in to Telegram...")
if not client.is_user_authorized():
    logging.info("User unauthorized")
    client.send_code_request(os.environ['TG_PHONE'])
    code_ok = False
    while not code_ok:
        code = input('Enter the auth code: ')
        try:
            code_ok = client.sign_in(os.environ['TG_PHONE'], code)
        except SessionPasswordNeededError:
            password = getpass('Two step verification enabled. '
                               'Please enter your password: ')
            code_ok = client.sign_in(password=password)
logging.info("Client initialized succesfully")
