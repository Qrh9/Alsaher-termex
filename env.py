import os
from os import getenv
from dotenv import load_dotenv


load_dotenv()
OWNER_ID= 5835316914
API_ID = 29594794
API_HASH = "d4b492451c79aad8eee7592ebc2220d4"
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
DATABASE_URL ="postgres://hbbudrdw:WQ3Yef0yJF3T-jUK8uDxBRH7ls1e-yxM@jelani.db.elephantsql.com/hbbudrdw"
MUST_JOIN = "https://t.me/SXYO3"

if not API_ID:
    print("No API_ID found. Exiting...")
    raise SystemExit
if not API_HASH:
    print("No API_HASH found. Exiting...")
    raise SystemExit
if not BOT_TOKEN:
    print("No BOT_TOKEN found. Exiting...")
    raise SystemExit
if not DATABASE_URL:
    print("No DATABASE_URL found. Exiting...")
    raise SystemExit

try:
    API_ID = int(API_ID)
except ValueError:
    print("API_ID is not a valid integer. Exiting...")
    raise SystemExit

if "postgres" in DATABASE_URL and "postgresql" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgres", "postgresql")
