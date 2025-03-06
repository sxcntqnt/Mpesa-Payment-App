from .base import *

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY', default='your-test-secret-key')  # Change to a secure value
DEBUG = True
ALLOWED_HOSTS = ['test-server.com']

# Database
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'test_db',
    'USER': 'test_user',
    'PASSWORD': 'test_password',
    'HOST': 'localhost',
    'PORT': '5432',
}

# Caching
CACHES['default'] = {
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": "redis://localhost:6379/2",
    "OPTIONS": {
        "CLIENT_CLASS": "django_redis.client.DefaultClient"
    }
}

# Celery settings for the test environment
CELERY_ALWAYS_EAGER = True
CELERY_BROKER_URL = 'redis://localhost:6379/2'

