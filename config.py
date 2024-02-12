from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("26701855"))
API_HASH = getenv("cd5b268d89348d68b451310653274f4c")

BOT_TOKEN = getenv("6594837440:AAF3DcLlS_-kU2wa7tnZaqIqj4377aAlsAE")
OWNER_ID = int(getenv("5835316914"))

MONGO_DB_URI = getenv("mongodb+srv://Qrh9:bamtas-0desdy-gowniF@cluster0.mxqfawd.mongodb.net/")
MUST_JOIN = getenv("MUST_JOIN", None)
