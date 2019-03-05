import os
import re
import bs4
import logging

import requests
import dateparser
from datetime import datetime, timedelta
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Sanic
from sanic.response import json
from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer

from ilswlol.telethon import get_telegram_confidence

logging.basicConfig(level='DEBUG', format='%(asctime)s %(levelname)s:%(name)s - %(message)s')

app = Sanic()
env = Environment(
    loader=PackageLoader('ilswlol', 'templates'),
    autoescape=select_autoescape(['html'])
)
lukas_id = None

@app.route('/')
async def index(request):
    schon_wach = True

    template = env.get_template('index.html')

    if schon_wach:
        if is_curl_like(request.user_agent.string) or request.args.get('raw'):
            return "JA"
        else:
            return template.render('index.html', schon_wach=True)
    else:
        if is_curl_like(request.user_agent.string) or request.args.get('raw'):
            return "NEIN"
        else:
            return template.render('index.html', schon_wach=False)


# def is_curl_like(user_agent_string):
#     curl_likes = ["HTTPie", "curl"]
#     return any([tool in user_agent_string for tool in curl_likes])
#
#
# def get_steam_confidence():
#     date = None
#
#     last_online_datetime_steam = cache.get('last_online_datetime_steam')
#     if last_online_datetime_steam is None:
#         logging.info("Steam cache has expired, fetching fresh data.")
#
#         # Check using steam profile.
#         steamprofile = requests.get("http://steamcommunity.com/id/Ahti333")
#         soup = bs4.BeautifulSoup(steamprofile.text, "html.parser")
#
#         online_offline_info = soup.find(class_='responsive_status_info')
#
#         # Check whether Lukas is online or offline right now.
#         if online_offline_info.find_all(text='Currently Online') or \
#            online_offline_info.find_all(text=re.compile('Online using')) or \
#            online_offline_info.find_all(text=re.compile('Currently In-Game')):
#             # If he's online in steam now, we're pretty confident.
#             confidence = 70
#             date = datetime.utcnow()
#             logging.debug("Currently online in Steam.")
#         else:
#             last_online = online_offline_info.find(class_='profile_in_game_name').string
#             last_online_date = last_online.replace('Last Online ', '')
#             date = dateparser.parse(last_online_date)
#             logging.debug(f"Last seen in Steam at {date}.")
#         cache.set('last_online_datetime_steam', date)
#     else:
#         date = last_online_datetime_steam
#         logging.info(f"Fetched Steam last online from cache: {date}")
#
#     delta = datetime.utcnow() - date
#
#     # Check whether Lukas has been online in Steam recently and assign confidence.
#     if delta < timedelta(minutes=5):
#         confidence = 70
#     elif delta < timedelta(minutes=45):
#         confidence = 50
#     elif delta < timedelta(hours=1):
#         confidence = 40
#     elif delta < timedelta(hours=3):
#         confidence = 30
#     elif delta < timedelta(hours=7):
#         confidence = 20
#     else:
#         confidence = 0
#
#     return confidence
#
#
# def ist_lukas_schon_wach():
#     # Get initial confidence from Steam
#     steam_confidence = get_steam_confidence()
#
#     # Get more confidence from Telegram
#     telegram_confidence = get_telegram_confidence()
#
#     confidence = steam_confidence + telegram_confidence
#     ist_wach = confidence >= 50
#
#     logging.info(f"Reporting ist wach '{ist_wach}' with Steam confidence {steam_confidence} "
#                  f"and Telegram confidence {telegram_confidence}. Total confidence {confidence}.")
#
#     return ist_wach
#
#
# @app.route("/")
# def index():
#     schon_wach = ist_lukas_schon_wach()
#
#     if schon_wach:
#         if is_curl_like(request.user_agent.string) or request.args.get('raw'):
#             return "JA"
#         else:
#             return render_template('index.html', schon_wach=True)
#     else:
#         if is_curl_like(request.user_agent.string) or request.args.get('raw'):
#             return "NEIN"
#         else:
#             return render_template('index.html', schon_wach=False)
#
#
# @app.errorhandler(429)
# def too_many_requests(e):
#     return "pls stop requests :("
#
#
# if __name__ == "__main__":
#     if not client.is_user_authorized():
#         raise RuntimeError("You need to run acquire_session.py first!")
#     app.run()
