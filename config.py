import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_NAME = os.getenv("SESSION_NAME", "userbot")

# Command prefixes
PREFIXES = [".", "!"]

# Owner ID (optional - for security)
OWNER_ID = int(os.getenv("OWNER_ID", "0"))  # set to your user id

# Default broadcast interval in seconds (to avoid FloodWait)
DEFAULT_INTERVAL = float(os.getenv("DEFAULT_INTERVAL", "2.0"))

# Git repo path for update (usually current directory)
REPO_PATH = os.getenv("REPO_PATH", ".")