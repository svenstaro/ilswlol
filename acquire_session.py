#!/usr/bin/env python

import asyncio
import logging
import os
import getpass
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

logging.basicConfig(level=logging.INFO)
load_dotenv(verbose=True)

loop = asyncio.get_event_loop()


async def acquire_session():
    # Initialize Telegram
    logging.info("Connecting to Telegram...")
    client = TelegramClient('telegram_client', os.environ['TG_API_ID'], os.environ['TG_API_HASH'], loop=loop)
    await client.connect()
    logging.info("Logging in to Telegram...")
    if not await client.is_user_authorized():
        logging.info("User unauthorized")
        await client.send_code_request(os.environ['TG_PHONE'])
        code_ok = False
        while not code_ok:
            code = input('Enter the auth code: ')
            try:
                code_ok = await client.sign_in(os.environ['TG_PHONE'], code)
            except SessionPasswordNeededError:
                password = getpass('Two step verification enabled. '
                                   'Please enter your password: ')
                code_ok = await client.sign_in(password=password)
    logging.info("Client initialized succesfully")

loop.run_until_complete(acquire_session())
