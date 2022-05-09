from .base import *
from .logs.custom import *
import datetime

## SECURITY WARNING: keep the secret key used in production secret!
## Either read it from the system environment or from the .env file,
## NO fallback or default values should be used.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", env("DJANGO_SECRET_KEY"))

## SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

## Can't be empty on production setup
ALLOWED_HOSTS = []

## Expire sessions
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ROOT_URLCONF = "config.urls.production"

THIRD_PARTY_APPS = ()

LOCAL_APPS = ("home.apps.HomeConfig",)

INSTALLED_APPS += LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE += []

## Implement caching
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "unix://run/redis/redis.sock",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#         "KEY_PREFIX": "KEY HERE",
#     }
# }

## Database overrides
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": str(ROOT_DIR.path("db.sqlite3")),
#     }
# }

## MORE security on deployment ,Please check documentation for more details
SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

## Set to true to avoid transmitting these cookies to HTTP accidentally
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

SECURE_BROWSER_XSS_FILTER = True

# SESSION_COOKIE_HTTPONLY = True

## One hr testing, 31536000 secs = 1 year
SECURE_HSTS_SECONDS = 63072000

## For subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True
