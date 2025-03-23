from .base import *
from PAYMENT_SYSTEM.env import env

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY')  # Must be set in environment or .env
DEBUG = env.bool(DJANGO_DEBUG, default='False')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Database connection pooling (for production)
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': env('DB_NAME'),
    'USER': env('DB_USER'),
    'PASSWORD': env('DB_PASSWORD'),
    'HOST': env('DB_HOST'),
    'PORT': env('DB_PORT', default='5432'),
    'CONN_MAX_AGE': 500,  # Connection pooling for performance
}

# Static and media files
STATIC_ROOT = '/var/www/static/'
MEDIA_ROOT = '/var/www/media/'

# Redis & Celery for production
REDIS_HOST = env('REDIS_HOST', default='prod-redis-server')
BROKER_URL = env('BROKER_URL', default='amqp://prod_user:prod_password@prod-rabbitmq/')
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:6379/0'

CACHES['default'] = {
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": f"redis://{REDIS_HOST}:6379/1",
    "OPTIONS": {
        "CLIENT_CLASS": "django_redis.client.DefaultClient"
    }
}

# SSL & Security
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Logging for production (set to INFO or WARNING)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/production.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

DEBUG = False
