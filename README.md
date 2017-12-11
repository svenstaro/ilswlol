# ilswlol
Wer weiss?

# How do
You need to create a `secrets` file on the deploying machine (not the machine you're deploying to!)
containing these variables:

    TG_API_ID=1337
    TG_API_HASH=longhexhash
    TG_PHONE='+1141141414'

You can get `TG_API_ID` and `TG_API_HASH` from the Telegram API settings for
your application. The `TG_PHONE` is your phone number associated with this app.
Then run this:

    make venv
    source local_env.sh
    python acquire_session.py
    make run
    curl 0.0.0.0:5000

# Deployment
You can use the ansible scripts in ansible/ to deploy the site. Remember to run
the `acquire_session.py` script on the server.
