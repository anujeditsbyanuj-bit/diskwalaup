import os
import logging
import sys

# ── Telegram credentials ─────────────────────────────────────────
# All secrets now come from environment variables — nothing is
# hardcoded in source, so this file is safe to commit to git.
API_ID = int(os.environ.get("API_ID", "37476811"))              # from my.telegram.org
API_HASH = os.environ.get("API_HASH", "7aa60670b871050820086c6267371ee6")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7512964694:AAF-0WDknvSpjnFGMcGNXKuiRpJEbNRSj3Q")              # from @BotFather
SESSION = os.environ.get["SESSION", "1BVtsOJ0Bu7iFhYaPaDWTPDdVAtu310L3iOh4PlTSxrTSyGaJPYQzf6rDgAMM9xGktQy9DodpC5TCCDTBMV3AiS4f5SNUbDR6kiPQ0PHUfj--XOQv82ZW2w2e7SM6GXvGdVTDXczbTBypUSYN0pSu-IMCd5atImWZBG6DvOg8o95pKmC9nc0H5jRMCfTBrtFbB0ba6iysaBd515MDP8fEWefKnRB8k8az61yt3hYhNhG-LQ2xgb1bz845tfZUK2KuKzXnmRZiMUmB_0agXDwQSEnTlJa5NlJxken911hhODilu2VCTKwbnweqj9QFHPDGoJcRZ-1GaVeGI-o1K70J3GZqLdcA_Ls="]                  # Telethon StringSession (see README)

OWNER_ID = int(os.environ.get["OWNER_ID", "8730393744"])           # your Telegram user ID
TG_BOT_WORKERS = int(os.getenv("TG_BOT_WORKERS", "4"))
FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL", "")  # channel username, without @

# ── Database ──────────────────────────────────────────────────────
DB_URI = os.environ.get["DATABASE_URL", "mongodb+srv://Anujedit:Anujedit@cluster0.7cs2nhd.mongodb.net/?appName=Cluster0"]              # MongoDB connection string
DB_NAME = os.getenv("DATABASE_NAME", "diskwala_bot")

commands = ["start", "stats", "premium"]

# ── Premium plans ─────────────────────────────────────────────────
# Prices/labels are just config — edit freely, nothing secret here.
PLANS = [
    {"label": "1 Day", "days": 1, "price": os.getenv("PLAN_1D_PRICE", "10")},
    {"label": "7 Days", "days": 7, "price": os.getenv("PLAN_7D_PRICE", "59")},
    {"label": "30 Days", "days": 30, "price": os.getenv("PLAN_30D_PRICE", "200")},
]

# ── Payment accounts ──────────────────────────────────────────────
# Put your own UPI / merchant details in environment variables —
# do NOT hardcode real payment identifiers in source control.
PAYMENT_ACCOUNTS = {
    "default": {
        "upi": os.getenv("PAYMENT_UPI", ""),
        "merchant": os.getenv("PAYMENT_MERCHANT_ID", ""),
    },
}
ACTIVE_PAYMENT = os.getenv("ACTIVE_PAYMENT_ACCOUNT", "default")

# Log / dump channel(s) that receive copies + payment notifications.
# Comma-separated list of chat IDs in env, e.g. "-100111,-100222"
LOG_CHANNELS = {
    "default": int(os.environ.get["LOG_CHANNEL_ID"]) if os.getenv("LOG_CHANNEL_ID", "-1003824246703") else None,
}

# ── Admin repost feature ───────────────────────────────────────────
# VIDEO_STORAGE_CHANNEL: where downloaded videos get uploaded/backed up
# REPOST_CHANNEL: where the edited post (with the combined deep-link) goes
# Accepts either a numeric chat ID or a channel username (with or without @).
# Prefer a username if you hit "Peer id invalid" errors — Render's container
# filesystem is wiped on every deploy, so the bot's cached numeric-ID peer
# list resets each time; a username always resolves regardless of session
# state, since Telegram looks it up directly instead of using a cache.
def _parse_chat_ref(value):
    if not value:
        return None
    v = value.strip()
    try:
        return int(v)
    except ValueError:
        return v if v.startswith("@") else f"@{v}"


VIDEO_STORAGE_CHANNEL = _parse_chat_ref(os.getenv("VIDEO_STORAGE_CHANNEL", ""))
REPOST_CHANNEL = _parse_chat_ref(os.getenv("REPOST_CHANNEL"))

PAYMENT_VERIFY_API = os.getenv("PAYMENT_VERIFY_API", "")

# ── Logging ───────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = lambda name: logging.getLogger(name)
