"""Entry point for ILSW lol app."""
import os
import asyncio
import logging
from aiocache import cached, SimpleMemoryCache

import asyncio
loop = asyncio.get_event_loop()

from ilswlol.telegram import get_telegram_confidence
from ilswlol.app import app

logging.basicConfig(level='DEBUG', format='%(asctime)s %(levelname)s:%(name)s - %(message)s')

if __name__ == "__main__":
    task = asyncio.ensure_future(app)
    loop.run_forever()
