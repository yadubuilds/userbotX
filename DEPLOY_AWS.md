# 🚀 Deploy Pyrogram Userbot to AWS EC2

Complete guide to deploy your userbot on AWS EC2 with auto-restart, logging, and GitHub integration.

---

## 📋 Prerequisites

1. AWS Account
2. GitHub Account
3. Telegram API credentials from https://my.telegram.org
4. SSH key pair for EC2

---

## PART 1: Prepare GitHub Repository

### Step 1: Create GitHub Repo
```bash
# On your local machine
cd pyrogram-userbot
git init
git add .
git commit -m "Initial commit: Pyrogram userbot with plugins"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/pyrogram-userbot.git
git push -u origin main
```

### Step 2: Add Secrets (for .update command)
Your bot will pull from this repo when you run `.update`

---

## PART 2: Launch AWS EC2 Instance

### Step 1: Create EC2
1. Go to AWS Console → EC2 → Launch Instance
2. Choose:
   - **Name**: pyrogram-userbot
   - **AMI**: Ubuntu Server 22.04 LTS (free tier)
   - **Instance type**: t2.micro (free tier) or t3.small for better performance
   - **Key pair**: Create new or use existing
   - **Security Group**: Allow SSH (port 22) from your IP
   - **Storage**: 8GB (default)

3. Launch instance

### Step 2: Connect via SSH
```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

---

## PART 3: Server Setup

Run these commands on your EC2:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python, Git, pip
sudo apt install -y python3 python3-pip python3-venv git

# Clone your repository
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/pyrogram-userbot.git
cd pyrogram-userbot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
```
Paste:
```
API_ID=1234567
API_HASH=your_api_hash
SESSION_NAME=userbot
OWNER_ID=your_telegram_user_id
DEFAULT_INTERVAL=2.5
```
Save: `Ctrl+O`, Enter, `Ctrl+X`

```bash
# First run (to login to Telegram)
python main.py
```
Enter phone number, code, and 2FA password. Once you see "Logged in as...", press `Ctrl+C`.

```bash
deactivate
```

---

## PART 4: Setup Auto-Start with Systemd

```bash
# Copy service file
sudo cp userbot.service /etc/systemd/system/

# Edit if needed (check paths)
sudo nano /etc/systemd/system/userbot.service

# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable userbot

# Start service
sudo systemctl start userbot

# Check status
sudo systemctl status userbot
```

**Useful commands:**
```bash
sudo systemctl stop userbot      # Stop
sudo systemctl restart userbot   # Restart
sudo systemctl status userbot    # Check status
journalctl -u userbot -f         # Live logs
journalctl -u userbot -n 100     # Last 100 lines
```

---

## PART 5: Deploy Updates

### Method 1: Using .update command (from Telegram)
Simply send in Telegram:
```
.update
```
Bot will git pull and restart automatically!

### Method 2: Manual
```bash
ssh -i your-key.pem ubuntu@YOUR_IP
cd /home/ubuntu/pyrogram-userbot
git pull
sudo systemctl restart userbot
```

---

## PART 6: Docker Deployment (Alternative)

If you prefer Docker:

```bash
# Install Docker
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
# Re-login SSH

cd /home/ubuntu/pyrogram-userbot

# Create .env file (same as above)
nano .env

# First run to create session
docker-compose run --rm userbot python main.py
# Login, then Ctrl+C

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Update
git pull
docker-compose up -d --build
```

---

## PART 7: Security Best Practices

1. **Never commit .env or .session files**
   - Already in .gitignore

2. **Restrict SSH access**
   - AWS Security Group: Only your IP on port 22

3. **Setup firewall**
```bash
sudo ufw allow ssh
sudo ufw enable
```

4. **Auto security updates**
```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure unattended-upgrades
```

5. **Backup session file**
```bash
# Download session for local backup
scp -i your-key.pem ubuntu@YOUR_IP:/home/ubuntu/pyrogram-userbot/userbot.session ./
```

---

## PART 8: Monitoring

### Check if bot is running
```bash
sudo systemctl is-active userbot
```

### Setup CloudWatch alerts (optional)
1. Install CloudWatch agent
2. Monitor memory/CPU
3. Get alerts if bot stops

### Telegram notifications on crash
Add to `main.py` (already handled by systemd restart)

---

## 🎯 Quick Deploy Script

Save as `deploy.sh` on EC2:
```bash
#!/bin/bash
cd /home/ubuntu/pyrogram-userbot
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart userbot
echo "Deployed successfully!"
```

Make executable:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## ✅ Verification Checklist

- [ ] EC2 instance running Ubuntu 22.04
- [ ] Repository cloned
- [ ] .env configured with correct API_ID/API_HASH
- [ ] First login completed (session file created)
- [ ] Systemd service enabled and running
- [ ] `.update` command works from Telegram
- [ ] Bot restarts automatically after reboot (`sudo reboot` to test)

---

## 🆘 Troubleshooting

**Bot not starting:**
```bash
journalctl -u userbot -n 50
# Check for missing .env or wrong API credentials
```

**FloodWait errors:**
- Increase `DEFAULT_INTERVAL` in .env to 3-5 seconds

**Git pull fails:**
```bash
cd /home/ubuntu/pyrogram-userbot
git config --global credential.helper store
git pull
# Enter GitHub username and PAT
```

**Session expired:**
- Delete `userbot.session` and run `python main.py` again

---

## 💰 Cost Estimate

- **t2.micro**: FREE for 12 months (AWS Free Tier)
- **After free tier**: ~$8-10/month
- **t3.small**: ~$15/month (better for heavy broadcasting)

---

Need help? Check logs: `journalctl -u userbot -f`