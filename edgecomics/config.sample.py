import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import cloudinary


SENTRY_TOKEN = ''
SENTRY = sentry_sdk.init(
    dsn='',
    integrations=[DjangoIntegration()]
)

DB = {
    'ENGINE': '',
    'NAME': '',
    'HOST': '',
    'PORT': '',
    'USER': '',
    'PASSWORD': '',
}

SECRET_KEY = ''

SITE_ADDRESS = ''

ALLOWED_HOSTS = []

DEBUG = False

SESSION_COOKIE_SECURE = True

VK_ACCESS_TOKEN = ''
VK_API_VERSION = ''

CLOUDINARY_CLOUD_NAME = ''
CLOUDINARY_API_KEY = ''
CLOUDINARY_API_SECRET = ''

CLOUDINARY_CONFIG = cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)

SIZES = {
    'xxs': 'thumb-xxs',
    'xs': 'thumb-xs',
    'sm': 'thumb-sm',
    'md': 'thumb-md',
    'lg': 'thumb-lg',
}

DUMMY = {
    'edge': {
        'id': 'dummy/dummy',
        'phash': 'cb879fb45c91f00c',
    },
    'prwld': {
        'id': 'dummy/prwld_dummy',
        'phash': 'cef1fc934c80f229',
    },
    'mdtwn': {
        'id': 'dummy/mdtwn_dummy',
        'phash': '903d0cbc3170efcb',
    },
}
