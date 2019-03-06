import logging

# Dirty, but we need the asyncio loop before we initialize telegram and sanic
logging.basicConfig(level='DEBUG', format='%(asctime)s %(levelname)s:%(name)s - %(message)s')
