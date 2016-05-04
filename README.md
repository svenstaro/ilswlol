# ilswlol
Wer weiss?

# How do
    git submodule update --init --recursive
    make
    venv/bin/python ilswlol/__init__.py
    curl 0.0.0.0:5000

# Deployment
You can use the ansible scripts in ansible/ to deploy the site.
When deploying, you have to do this on first run to authenticate with Telegram.
This should put the auth data in a safe directory.

    TELEGRAM_HOME=/var/lib/ilswlol externals/tg/bin/telegram-cli -k externals/tg/tg-server.pub
