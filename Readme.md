# Diskwala Downloader Bot

A Telegram bot that resolves Diskwala share links, downloads the file via `aria2c`,
and delivers it back to the user — with multi-link support, concurrent-download
handling, MongoDB caching, dump-channel backups, force-subscribe gating, and an
optional UPI-based premium subscription system.

> **This is a fixed version of a repo that was found to contain a malicious
> `bot.py` (silently banned a hardcoded user and revoked their messages instead
> of running the bot), hardcoded live credentials (bot token, Telethon session,
> MongoDB password, UPI IDs), and a Docker Compose file that mounted the host's
> SSH keys and Docker socket into the container. All of that has been removed.
> The actual bot logic (`plugins/diskwala.py`) was legitimate and is unchanged.**

---

## ✨ Features

- **Multi-link messages** — send one or many Diskwala links in a single message
- **Fast parallel downloads** via `aria2c`
- **Concurrency control** — global semaphore caps simultaneous downloads
- **MongoDB-backed cache** — duplicate requests are served via instant
  server-side Telegram copy instead of re-downloading
- **Dump channel backups** — configurable channels get a copy of every delivery
- **Live progress** — inline button shows % + speed
- **Force-subscribe gate**
- **Premium/UPI subscription system** — QR-code payment, auto-verification,
  free-tier download limit before switching to stream-only mode
- `/stats`, `/adddump`, `/deldump`, `/dumps`, `/addpaid`, `/delpremium`,
  `/broadcast` (all owner-only except `/premium`, `/start`)

---

## 🧰 Tech Stack

| Component | Purpose |
|---|---|
| Pyrogram | Telegram Bot API client |
| Telethon | User-session client, used to obtain Diskwala's Mini App auth token |
| Motor | Async MongoDB driver |
| aria2c | Multi-connection accelerated downloader |

---

## 📋 Requirements

- Python 3.10+
- MongoDB instance (e.g. MongoDB Atlas free tier)
- `aria2` on the host (`apt install aria2`)
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- A Telegram **user session string** (see below) — used only to call
  Diskwala's Mini App endpoint via Telethon

---

## ⚙️ Configuration

All secrets now live in environment variables — nothing is hardcoded in
source, so this repo is safe to keep in git.

1. Copy `.env.example` to `.env`
2. Fill in your own values (bot token, API ID/hash, Mongo URI, etc.)
3. **Never commit `.env`** — it's already in `.gitignore`

### Getting `SESSION` (Telethon StringSession)

Run this once, locally, with your **own** Telegram account (not shared, not
copy-pasted from anywhere else — a session string is equivalent to a login,
so treat it like a password):

```python
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 12345          # your api_id from my.telegram.org
api_hash = "your_hash"

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
```

Paste the printed string into `SESSION` in your `.env`. The account must have
opened `@sky577bot`'s Mini App at least once (`get_init()` depends on that).

---

## 🚀 Installation

### Local
```bash
git clone <your-fork-url>
cd diskwala-bot
pip install -r requirements.txt
sudo apt install aria2   # if not already installed
cp .env.example .env     # then edit .env
python3 bot.py
```

### Docker
```bash
cp .env.example .env     # then edit .env
docker compose up -d --build
```

### Render
- Deploy as a **Background Worker** (not Web Service) — this is a bot, it
  doesn't need to receive HTTP traffic. This also avoids the free-tier
  "spins down when idle" behavior that a Web Service has.
- Set every variable from `.env.example` in Render's Environment tab.
- If you must use a Web Service (e.g. plan constraints), `bot.py` already
  binds `$PORT` with a tiny health-check server when Render sets that
  variable — no extra code needed.

---

## 🔧 Tuning

- **`MAX_CONCURRENT_DOWNLOADS`** (in `plugins/diskwala.py`) — how many files
  download simultaneously across all users.
- **`aria2c` flags** (`-x`, `-s`, `-k`) inside the same file control
  connections/splits per file.

---

## ⚠️ Security notes

- `config.py` reads everything from environment variables — verify your
  hosting provider's env vars are set before deploying, or the bot will
  fail fast with a clear `KeyError` instead of running with blank secrets.
- `PAYMENT_VERIFY_API` must point to **your own** payment-verification
  endpoint — the original repo pointed to someone else's private server,
  which obviously won't work for your payments.
- Rotate/replace any credential that was ever hardcoded in the original
  repo (bot token, session string, Mongo password) — treat all of them as
  permanently compromised, don't just reuse them here.
