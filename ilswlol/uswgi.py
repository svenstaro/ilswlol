from werkzeug.contrib.cache import UWSGICache

cache = UWSGICache(default_timeout=10 * 60)
