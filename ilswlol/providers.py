def get_steam_confidence():
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


def get_telegram_confidence():
    date = None

    last_online_datetime_telegram = cache.get('last_online_datetime_telegram')
    if last_online_datetime_telegram is None:
        logging.info("Telegram cache has expired, fetching fresh data.")
        try:
            lukas = client.get_entity('lukasovich', force_fetch=True)
        except FloodWaitError:
            abort(429)
            logging.critical("Too many Telegram API requests!")

        if isinstance(lukas.status, UserStatusOnline):
            date = datetime.utcnow()
            logging.debug("Currently online in Telegram.")
        else:
            date = lukas.status.was_online
            human_delta = humanize.naturaltime(datetime.utcnow() - date)
            logging.debug(f"Last seen in Telegram at {date} ({human_delta}).")
        cache.set('last_online_datetime_telegram', date)
    else:
        date = last_online_datetime_telegram
        logging.info(f"Fetched Telegram last online from cache: {date}")

    delta = datetime.utcnow() - date

    # Check whether Lukas has been online in Telegram recently and assign confidence.
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


def ist_lukas_schon_wach():
    # Get initial confidence from Steam
    steam_confidence = get_steam_confidence()

    # Get more confidence from Telegram
    telegram_confidence = get_telegram_confidence()

    confidence = steam_confidence + telegram_confidence
    ist_wach = confidence >= 50

    logging.info(f"Reporting ist wach '{ist_wach}' with Steam confidence {steam_confidence} "
                 f"and Telegram confidence {telegram_confidence}. Total confidence {confidence}.")

    return ist_wach
