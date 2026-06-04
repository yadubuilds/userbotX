# Pyrogram Userbot with Plugins

Full-featured Telegram userbot built with Pyrogram v2.

[![Deploy to AWS](https://img.shields.io/badge/Deploy-AWS_EC2-orange)](DEPLOY_AWS.md)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)

## Features

✅ **Update & Restart**
- `.update` - git pull and auto-restart
- `.restart` - restart userbot

✅ **Broadcast to all DM chats**
- `.bcdm [--interval 2] [--schedule '2025-12-31 23:59'] <text>` or reply
- Sends to all private chats with delay to avoid FloodWait

✅ **Broadcast to all contacts**
- `.bccontacts <text>` or reply

✅ **Post Story**
- `.story <caption>` (reply to photo/video)
- Uses `client.send_story` - requires Telegram Premium for longer periods

✅ **Save Contact**
- `.savecontact +919876543210 FirstName LastName`

✅ **Message Join Requests**
- `.reqdm @groupusername <message>`
- Sends DM with group link to all pending join requests

✅ **Broadcast to Group Members**
- `.bcgroup @group [--interval 3] [--schedule '2025-06-10 10:00'] <text>` or reply
- DMs all non-bot members

## Setup

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Get API credentials from https://my.telegram.org
3. Copy `.env.example` to `.env` and fill:
```
API_ID=...
API_HASH=...
OWNER_ID=...  # your telegram user id
```

4. Run:
```bash
python main.py
```
First run will ask for phone number and code.

## 🚀 Deploy to AWS EC2

See **[DEPLOY_AWS.md](DEPLOY_AWS.md)** for complete step-by-step guide.

Quick start:
```bash
# On EC2
git clone https://github.com/YOUR_USERNAME/pyrogram-userbot.git
cd pyrogram-userbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Create .env, then:
sudo cp userbot.service /etc/systemd/system/
sudo systemctl enable --now userbot
```

## Project Structure
```
pyrogram-userbot/
├── main.py
├── config.py
├── plugins/
│   ├── update.py
│   ├── broadcast.py
│   ├── story.py
│   ├── contacts.py
│   ├── joinreq.py
│   └── group_broadcast.py
```

## Notes

- All commands work only for you (filters.me)
- Default interval is 2 seconds to prevent bans. Increase for large broadcasts.
- Scheduled broadcasts use APScheduler (timezone Asia/Kolkata - change in main.py)
- Story posting requires Pyrogram fork with stories support (Kurigram/PyroTGFork). Standard Pyrogram 2.0.106 supports it.
- Be careful with mass DMs - Telegram may limit your account. Use responsibly.

## Commands Summary

| Command | Description |
|---------|-------------|
| `.update` | Pull from git and restart |
| `.restart` | Restart bot |
| `.bcdm Hello` | Broadcast to all DMs |
| `.bcdm --interval 5 --schedule '2025-12-25 09:00' Merry Christmas` | Scheduled |
| `.bccontacts Sale today!` | Broadcast to contacts |
| `.story Nice day` (reply to media) | Post story |
| `.savecontact +91... John` | Save contact |
| `.reqdm @mychannel Please join` | DM pending joiners |
| `.bcgroup @mygroup Hello members` | DM all group members |