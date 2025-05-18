import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # safely no-ops if no .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
POSTGRES_URL = os.getenv("POSTGRES_URL", "")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing — create a .env file")
