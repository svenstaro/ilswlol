"""Module for updating and querying the last_seen status of Lukas from steam."""
import bs4
import re
import logging
import aiohttp
import dateparser
from datetime import datetime, timedelta
from aiocache import cached


async def get_steam_confidence():
    """Get last seen status from steam and calculate the confidence of him being awake."""
    date = None

    date = await get_last_seen()
    logging.info(f"Fetched Steam last online from cache: {date}")

    delta = datetime.utcnow() - date

    # Check whether Lukas has been online in Steam recently and assign confidence.
    if delta < timedelta(minutes=5):
        confidence = 70
    elif delta < timedelta(minutes=45):
        confidence = 50
    elif delta < timedelta(hours=1):
        confidence = 40
    elif delta < timedelta(hours=3):
        confidence = 30
    elif delta < timedelta(hours=7):
        confidence = 20
    else:
        confidence = 0

    return confidence


@cached(key="steam", ttl=600)
async def get_last_seen():
    """Get the last_seen status from cache or query it manually."""
    logging.info("Steam cache has expired, fetching fresh data.")

    # Check using steam profile.
    soup = None
    async with aiohttp.ClientSession() as session:
        async with session.get("http://steamcommunity.com/id/Ahti333") as resp:
            soup = bs4.BeautifulSoup(await resp.text(), "html.parser")

    online_offline_info = soup.find(class_='responsive_status_info')

    # Check whether Lukas is online or offline right now.
    if online_offline_info.find_all(text='Currently Online') or \
       online_offline_info.find_all(text=re.compile('Online using')) or \
       online_offline_info.find_all(text=re.compile('Currently In-Game')):
        # If he's online in steam now, we're pretty confident.
        date = datetime.utcnow()
        logging.debug("Currently online in Steam.")
    else:
        last_online = online_offline_info.find(class_='profile_in_game_name').string
        last_online_date = last_online.replace('Last Online ', '')
        date = dateparser.parse(last_online_date)
        logging.debug(f"Last seen in Steam at {date}.")

    return date
