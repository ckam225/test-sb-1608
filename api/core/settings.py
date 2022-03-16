import os


SECRET_KEY = os.environ.get('SECRET_KEY', '')
JWT_TOKEN_ALGORITHM = os.environ.get('JWT_TOKEN_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get(
    'ACCESS_TOKEN_EXPIRE_MINUTES', 30)  # 30 minutes

AUTH_URL = os.environ.get('AUTH_URL', 'auth/login')

DATABASE_URL = 'sqlite://db.sqlite3'

TORTOISE_ORM_CONFIG = {
    "connections": {
        "default": DATABASE_URL
    },
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default",
        }
    },
}


TELEGRAM_BOT_TOKEN = '5195680484:AAGTjrsmVHzCsldaHVStedokrQMixnD6NRg'

ALLOWED_HOSTS = [
    'http://localhost:3000',
    "http://localhost:8000",
]


MEDIA_URL = 'http://localhost:8000/media/images'
