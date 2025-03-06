from config.env import env

# Celery settings for the test environment
CELERY_ALWAYS_EAGER = True
CELERY_BROKER_URL = 'redis://localhost:6379/2'
