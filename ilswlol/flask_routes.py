import os
import re
import logging

import requests
import bs4
import dateparser
import humanize
import uwsgi
from datetime import datetime, timedelta
from flask import Flask, request, render_template, abort
from werkzeug.contrib.cache import UWSGICache

app = Flask(__name__)
cache = UWSGICache(default_timeout=10 * 60)
lukas_id = None


@app.route("/")
def index():
    schon_wach = ist_lukas_schon_wach()

    if schon_wach:
        if is_curl_like(request.user_agent.string) or request.args.get('raw'):
            return "JA"
        else:
            return render_template('index.html', schon_wach=True)
    else:
        if is_curl_like(request.user_agent.string) or request.args.get('raw'):
            return "NEIN"
        else:
            return render_template('index.html', schon_wach=False)


@app.errorhandler(429)
def too_many_requests(e):
    return "pls stop requests :("


if __name__ == "__main__":
    if not client.is_user_authorized():
        raise RuntimeError("You need to run acquire_session.py first!")
    app.run()
