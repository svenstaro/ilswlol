import os
import logging

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
    """Well, lets check whether he is awake or net."""
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
