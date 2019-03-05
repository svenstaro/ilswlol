import bs4
import re
import logging
import requests
import dateparser
from datetime import datetime, timedelta


def get_steam_confidence():
    """Get last seen status from steam and calculate the confidence of him being awake."""
    date = None

    last_online_datetime_steam = cache.get('last_online_datetime_steam')
    if last_online_datetime_steam is None:
        logging.info("Steam cache has expired, fetching fresh data.")

        # Check using steam profile.
        steamprofile = requests.get("http://steamcommunity.com/id/Ahti333")
        soup = bs4.BeautifulSoup(steamprofile.text, "html.parser")

        online_offline_info = soup.find(class_='responsive_status_info')

        # Check whether Lukas is online or offline right now.
        if online_offline_info.find_all(text='Currently Online') or \
           online_offline_info.find_all(text=re.compile('Online using')) or \
           online_offline_info.find_all(text=re.compile('Currently In-Game')):
            # If he's online in steam now, we're pretty confident.
            confidence = 70
            date = datetime.utcnow()
            logging.debug("Currently online in Steam.")
        else:
            last_online = online_offline_info.find(class_='profile_in_game_name').string
            last_online_date = last_online.replace('Last Online ', '')
            date = dateparser.parse(last_online_date)
            logging.debug(f"Last seen in Steam at {date}.")
        cache.set('last_online_datetime_steam', date)
    else:
        date = last_online_datetime_steam
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
