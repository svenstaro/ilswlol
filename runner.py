#!/usr/bin/env python
"""Entry point for ilswlol."""
from signal import signal, SIGINT
import asyncio

from ilswlol.app import app

loop = asyncio.get_event_loop()

server = app.create_server(host="localhost", port=8080)
task = asyncio.ensure_future(server)
loop.run_forever()
signal(SIGINT, lambda s, f: loop.stop())

try:
    loop.run_forever()
except BaseException:
    loop.stop()
