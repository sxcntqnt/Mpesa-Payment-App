import environ
from pathlib import Path


env = environ.Env()

# Set BASE_DIR to the MPA directory (two levels up from env.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Tell environ where to find the .env file
environ.Env.read_env(BASE_DIR / "config" / ".env")
