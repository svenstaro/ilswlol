"""The Sanic module for answering requests."""
import logging
from sanic import Sanic, response
from jinja2 import Environment, PackageLoader, select_autoescape

from ilswlol.steam import get_steam_confidence
from ilswlol.telegram import get_telegram_confidence

app = Sanic(__name__)
app.static('/static', './ilswlol/static')
env = Environment(
    loader=PackageLoader('ilswlol', 'templates'),
    autoescape=select_autoescape(['html'])
)


@app.route('/')
async def index(request):
    """Well, lets check whether he is awake or net."""
    schon_wach = await ist_lukas_schon_wach()

    template = env.get_template('index.html')

    if schon_wach:
        if is_curl_like(request.headers['user-agent']) or request.args.get('raw'):
            return response.text("JA")
        else:
            return response.html(template.render(schon_wach=True, url_for=app.url_for))
    else:
        if is_curl_like(request.headers['user-agent']) or request.args.get('raw'):
            return response.text("NEIN")
        else:
            return response.html(template.render(schon_wach=False, url_for=app.url_for))


def is_curl_like(user_agent_string):
    """Check whether the agent is curl like."""
    curl_likes = ["HTTPie", "curl"]
    return any([tool in user_agent_string for tool in curl_likes])


async def ist_lukas_schon_wach():
    # Get initial confidence from Steam
    steam_confidence = await get_steam_confidence()

    # Get more confidence from Telegram
    telegram_confidence = await get_telegram_confidence()

    confidence = steam_confidence + telegram_confidence
    ist_wach = confidence >= 50

    logging.info(f"Reporting ist wach '{ist_wach}' with Steam confidence {steam_confidence} "
                 f"and Telegram confidence {telegram_confidence}. Total confidence {confidence}.")

    return ist_wach
