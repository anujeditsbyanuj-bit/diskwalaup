import os
import logging
import sys

# ── Telegram credentials ─────────────────────────────────────────
# All secrets now come from environment variables — nothing is
# hardcoded in source, so this file is safe to commit to git.
API_ID = int(os.environ["API_ID"])              # from my.telegram.org
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]              # from @BotFather
SESSION = os.environ["SESSION"]                  # Telethon StringSession (see README)

OWNER_ID = int(os.environ["OWNER_ID"])           # your Telegram user ID
TG_BOT_WORKERS = int(os.getenv("TG_BOT_WORKERS", "4"))
FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL", "")  # channel username, without @

# ── Database ──────────────────────────────────────────────────────
DB_URI = os.environ["DATABASE_URL"]              # MongoDB connection string
DB_NAME = os.getenv("DATABASE_NAME", "diskwala_bot")

commands = ["start", "stats", "premium"]

# ── Premium plans ─────────────────────────────────────────────────
# Prices/labels are just config — edit freely, nothing secret here.
PLANS = [
    {"label": "1 Day", "days": 1, "price": os.getenv("PLAN_1D_PRICE", "")},
    {"label": "7 Days", "days": 7, "price": os.getenv("PLAN_7D_PRICE", "")},
    {"label": "30 Days", "days": 30, "price": os.getenv("PLAN_30D_PRICE", "")},
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
    "default": int(os.environ["LOG_CHANNEL_ID"]) if os.getenv("LOG_CHANNEL_ID") else None,
}

PAYMENT_VERIFY_API = os.getenv("PAYMENT_VERIFY_API", "")

# ── Logging ───────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = lambda name: logging.getLogger(name)
