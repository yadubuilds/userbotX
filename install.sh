#!/bin/bash
# Quick setup script for Ubuntu/Debian EC2

echo "🚀 Setting up Pyrogram Userbot..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11 and git
sudo apt install -y python3 python3-pip python3-venv git screen

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete!"
echo "Next steps:"
echo "1. cp .env.example .env"
echo "2. nano .env (fill API_ID, API_HASH, OWNER_ID)"
echo "3. python main.py (first run to login)"
echo "4. For production: sudo cp userbot.service /etc/systemd/system/ && sudo systemctl enable --now userbot"