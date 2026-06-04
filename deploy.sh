#!/bin/bash
# Quick deploy script for AWS EC2

set -e

echo "🚀 Deploying Pyrogram Userbot..."

cd /home/ubuntu/pyrogram-userbot

echo "📥 Pulling latest code..."
git pull origin main

echo "📦 Activating virtual environment..."
source venv/bin/activate

echo "⬆️  Installing dependencies..."
pip install -r requirements.txt --quiet

echo "♻️  Restarting service..."
sudo systemctl restart userbot

echo "✅ Deployment complete!"
echo "📊 Status:"
sudo systemctl status userbot --no-pager -l