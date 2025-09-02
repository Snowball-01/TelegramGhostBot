import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Vars(object):
    # bot configuration
    API_ID = os.getenv("API_ID", "")
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")

    # database configuration
    MONGODB_URL = os.getenv("MONGODB_URL", "")

    # other config variables
    ADMINS = [int(admin) for admin in os.getenv("ADMINS", "").split()]
