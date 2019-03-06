"""Entry point for ILSW lol app."""
import logging

# Dirty, but we need the asyncio loop before we initialize telegram and sanic
import asyncio
loop = asyncio.get_event_loop()

from ilswlol.app import app

logging.basicConfig(level='DEBUG', format='%(asctime)s %(levelname)s:%(name)s - %(message)s')

if __name__ == "__main__":
    task = asyncio.ensure_future(app)
    loop.run_forever()
