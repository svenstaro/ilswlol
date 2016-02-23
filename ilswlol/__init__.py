import sys
from os import path
import subprocess
import json
import requests
import bs4
import dateparser
from datetime import datetime, timedelta

from flask import Flask

app = Flask(__name__)

def ist_lukas_schon_wach():
    confidence = 0

    # Check using steam profile
    steamprofile = requests.get("http://steamcommunity.com/id/Ahti333")
    soup = bs4.BeautifulSoup(steamprofile.text, "html.parser")

    online_offline_info = soup.find(class_='responsive_status_info')

    # Check whether user is online or offline right now
    if online_offline_info.find_all(text='Currently Online'):
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

    # Check using telegram
    tg_path = path.join(path.dirname(sys.executable), "..", "..", "externals", "tg")
    tg_cli_path = path.join(tg_path, "bin", "telegram-cli")
    tg_pubkey_path = path.join(tg_path, "tg-server.pub")
    json_contacts = subprocess.run([tg_cli_path, "-k", tg_pubkey_path,
                                    "-e", "contact_list", "--json", "-D", "-R"],
                                   stdout=subprocess.PIPE)
    split_contacts = json_contacts.stdout.splitlines()[0].decode("utf-8")
    parsed_contacts = json.loads(split_contacts)
    for contact in parsed_contacts:
        if 'username' in contact and contact['username'] == 'lukasovich':
            date = dateparser.parse(contact['when'])
            delta = datetime.utcnow() - date

            # Check whether Lukas has been online recently and assign confidence
            if delta < timedelta(minutes=5):
                confidence += 70
            elif delta < timedelta(hours=1):
                confidence += 40
            elif delta < timedelta(hours=3):
                confidence += 30
            elif delta < timedelta(hours=7):
                confidence += 20

            break

    return confidence

@app.route("/")
def index():
    if ist_lukas_schon_wach() >= 50:
        return "JA"
    else:
        return "NEIN"

if __name__ == "__main__":
    app.run()
