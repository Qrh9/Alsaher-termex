from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

BOT_TOKEN = getenv("BOT_TOKEN")
OWNER_ID = 5835316914

DATABASE_URL = os.getenv("DATABASE_URL","").strip()
MUST_JOIN = getenv("MUST_JOIN", None)
