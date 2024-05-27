from .base import *
from dotenv import load_dotenv

DEBUG = True

# Read from .env file

load_dotenv(os.path.join(BASE_DIR, '.env'))