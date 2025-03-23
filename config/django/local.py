from .base import *
from PAYMENT_SYSTEM.env import env

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY', default='your-local-secret-key')  # Change to a secure value
DEBUG = True
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# settings.py
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in env.list("ALLOWED_HOSTS", default=[])]

# Database
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'dev_db.sqlite3'),
}

# Celery settings for local
CELERY_ALWAYS_EAGER = True
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

