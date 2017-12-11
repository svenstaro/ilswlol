import sys
import logging
import os
from os import path
import re
import getpass
import json
import requests
import bs4
import dateparser
import tempfile
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from datetime import datetime, timedelta
from werkzeug.contrib.cache import FileSystemCache
from flask import Flask, request, render_template

app = Flask(__name__)
cache_dir = tempfile.TemporaryDirectory(prefix="ilswlol-")
cache = FileSystemCache(cache_dir.name)
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


def get_steam_confidence():
    confidence = 0

    # Check using steam profile
    steamprofile = requests.get("http://steamcommunity.com/id/Ahti333")
    soup = bs4.BeautifulSoup(steamprofile.text, "html.parser")

    online_offline_info = soup.find(class_='responsive_status_info')

    # Check whether user is online or offline right now
    if online_offline_info.find_all(text='Currently Online') or \
       online_offline_info.find_all(text=re.compile('Online using')) or \
       online_offline_info.find_all(text=re.compile('Currently In-Game')):
        # If he's online in steam now, we're pretty confident
        confidence += 70
    else:
        last_online = online_offline_info.find(class_='profile_in_game_name').string
        last_online_date = last_online.replace('Last Online ', '')
        date = dateparser.parse(last_online_date)
        delta = datetime.utcnow() - date

        # Check whether Lukas has been online recently and assign confidence
        if delta < timedelta(hours=1):
            confidence += 40
        elif delta < timedelta(hours=3):
            confidence += 30
        elif delta < timedelta(hours=7):
            confidence += 20

    return confidence


def get_telegram_confidence():
    confidence = 0

    lukas = client.get_entity('lukasovich')
    date = lukas.status.was_online
    delta = datetime.utcnow() - date

    # Check whether Lukas has been online recently and assign confidence
    if delta < timedelta(minutes=5):
        confidence += 70
    if delta < timedelta(minutes=45):
        confidence += 50
    elif delta < timedelta(hours=1):
        confidence += 40
    elif delta < timedelta(hours=3):
        confidence += 30
    elif delta < timedelta(hours=7):
        confidence += 20

    return confidence


def ist_lukas_schon_wach():
    # Get initial confidence from Steam
    confidence = get_steam_confidence()

    # Get more confidence from Telegram
    confidence += get_telegram_confidence()

    return confidence >= 50


@app.route("/")
def index():
    schon_wach = cache.get('ist_lukas_schon_wach')
    if schon_wach is None:
        schon_wach = ist_lukas_schon_wach()
        cache.set('ist_lukas_schon_wach', schon_wach, timeout=5 * 60)

    if schon_wach:
        if request.args.get('raw'):
            return "JA"
        else:
            return render_template('index.html', schon_wach=True)
    else:
        if request.args.get('raw'):
            return "NEIN"
        else:
            return render_template('index.html', schon_wach=False)


if __name__ == "__main__":
    app.run()
