#!/usr/bin/env python

from signal import signal, SIGINT
import asyncio
import uvloop

from ilswlol import loop
from ilswlol.app import app

if loop is None:
    loop = asyncio.get_event_loop()

server = app.create_server(host="0.0.0.0", port=8080)
task = asyncio.ensure_future(server)
loop.run_forever()
signal(SIGINT, lambda s, f: loop.stop())
try:
    loop.run_forever()
except:
    loop.stop()
