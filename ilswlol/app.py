"""The Sanic module for answering requests."""
from sanic import Sanic
from aiocache import SimpleMemoryCache
from jinja2 import Environment, PackageLoader, select_autoescape

app = Sanic()
env = Environment(
    loader=PackageLoader('ilswlol', 'templates'),
    autoescape=select_autoescape(['html'])
)


@app.route('/')
async def index(request):
    """Well, lets check whether he is awake or net."""
    schon_wach = True
#     schon_wach = ist_lukas_schon_wach()

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


def is_curl_like(user_agent_string):
    """Check whether the agent is curl like."""
    curl_likes = ["HTTPie", "curl"]
    return any([tool in user_agent_string for tool in curl_likes])


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
