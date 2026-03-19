# 🚀 LIFEASY V30 PRO - COMPLETE PRODUCTION DEPLOYMENT GUIDE

## 📋 **TABLE OF CONTENTS**

1. [Architecture Overview](#architecture-overview)
2. [VPS Provider Selection](#vps-provider-selection)
3. [Server Setup](#server-setup)
4. [PostgreSQL Configuration](#postgresql-configuration)
5. [Backend Deployment](#backend-deployment)
6. [Nginx + SSL Setup](#nginx--ssl-setup)
7. [Mobile App Configuration](#mobile-app-configuration)
8. [Monitoring & Maintenance](#monitoring--maintenance)

---

## 🏗️ **ARCHITECTURE OVERVIEW**

```
┌─────────────┐
│ Mobile App  │ (Flutter APK)
└──────┬──────┘
       │ HTTPS (Internet)
       ▼
┌─────────────┐
│   Domain    │ api.lifeasy.com
└──────┬──────┘
       │
┌──────▼──────┐
│    Nginx    │ (Reverse Proxy + SSL)
└──────┬──────┘
       │ Port 8000
┌──────▼──────┐
│  FastAPI    │ (Python Backend)
└──────┬──────┘
       │ SQLAlchemy
┌──────▼──────┐
│ PostgreSQL  │ (Production Database)
└─────────────┘
```

---

## 💻 **VPS PROVIDER SELECTION**

### **Recommended Providers:**

| Provider | Plan | Price | Specs |
|----------|------|-------|-------|
| **DigitalOcean** | Basic | $5/month | 1GB RAM, 1 CPU, 25GB SSD |
| **Hetzner** | CPX11 | €4.50/month | 2GB RAM, 1 CPU, 40GB SSD |
| **Linode** | Nanode | $5/month | 1GB RAM, 1 CPU, 25GB SSD |
| **Vultr** | Cloud | $5/month | 1GB RAM, 1 CPU, 25GB SSD |

### **Minimum Requirements:**
- ✅ 1 GB RAM
- ✅ 1 CPU Core
- ✅ 20+ GB SSD
- ✅ Ubuntu 20.04 or 22.04 LTS
- ✅ Public IP address

---

## 🖥️ **SERVER SETUP**

### **Step 1: SSH into Server**

```bash
ssh root@your_server_ip
# Password: (provided by VPS provider)
```

### **Step 2: Create Non-Root User**

```bash
# Add new user
adduser lifeasy

# Grant sudo privileges
usermod -aG sudo lifeasy

# Switch to new user
su - lifeasy
```

### **Step 3: Update System**

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 🗄️ **POSTGRESQL CONFIGURATION**

### **Step 1: Install PostgreSQL**

```bash
sudo apt install -y postgresql postgresql-contrib libpq-dev
```

### **Step 2: Create Database & User**

```bash
sudo -u postgres psql
```

```sql
-- Create database
CREATE DATABASE lifeasy;

-- Create user with password
CREATE USER lifeasy_user WITH PASSWORD 'CHANGE_THIS_SECURE_PASSWORD';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE lifeasy TO lifeasy_user;
ALTER DATABASE lifeasy OWNER TO lifeasy_user;

-- Exit
\q
```

### **Step 3: Verify Connection**

```bash
psql -U lifeasy_user -d lifeasy -h localhost
```

---

## 🔧 **BACKEND DEPLOYMENT**

### **Step 1: Install Python Dependencies**

```bash
sudo apt install -y python3 python3-pip python3-venv

# Create app directory
sudo mkdir -p /var/www/lifeasy
cd /var/www/lifeasy

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### **Step 2: Install Python Packages**

```bash
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary python-jose passlib[bcrypt] pydantic python-dotenv
```

### **Step 3: Copy Application Files**

```bash
# From your local machine, copy files via SCP
scp -r backend/* lifeasy@your_server_ip:/var/www/lifeasy/
```

Or use Git:

```bash
git clone <your-repo-url> /var/www/lifeasy
```

### **Step 4: Create Environment File**

```bash
cd /var/www/lifeasy
nano .env
```

Add:

```env
LIFEASY_ENV=production
DATABASE_URL=postgresql://lifeasy_user:YOUR_SECURE_PASSWORD@localhost/lifeasy
JWT_SECRET=GENERATE_RANDOM_STRING_HERE_MIN_32_CHARS
TOKEN_EXPIRY=30
HOST=0.0.0.0
PORT=8000
```

### **Step 5: Initialize Database**

```bash
source venv/bin/activate
python seed_prod.py
```

### **Step 6: Test Backend**

```bash
python -m uvicorn main_prod:app --host 0.0.0.0 --port 8000
```

Visit: `http://your_server_ip:8000/docs`

---

## 🌐 **NGINX + SSL SETUP**

### **Step 1: Install Nginx**

```bash
sudo apt install -y nginx
```

### **Step 2: Configure Nginx**

```bash
sudo nano /etc/nginx/sites-available/lifeasy
```

Paste content from [`nginx_config.txt`](nginx_config.txt)

### **Step 3: Enable Site**

```bash
sudo ln -s /etc/nginx/sites-available/lifeasy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### **Step 4: Install SSL Certificate (Let's Encrypt)**

```bash
sudo apt install -y certbot python3-certbot-nginx

sudo certbot --nginx -d api.lifeasy.com
```

### **Step 5: Auto-Renew SSL**

```bash
sudo crontab -e
```

Add:

```cron
0 3 * * * certbot renew --quiet
```

---

## 📱 **MOBILE APP CONFIGURATION**

### **Update API URL**

Edit file: `mobile_app/lib/services/api_service.dart`

```dart
static const String baseUrl = "https://api.lifeasy.com/api";
```

### **Rebuild APK**

```powershell
cd mobile_app

flutter clean
flutter pub get
flutter build apk --release
```

### **APK Location**

```
build/app/outputs/flutter-apk/app-release.apk
```

---

## 🔒 **SECURITY HARDENING**

### **1. Firewall Setup**

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### **2. Fail2Ban (Brute Force Protection)**

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### **3. Automatic Security Updates**

```bash
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

### **4. Secure JWT Secret**

Generate strong secret:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Update `.env` file with generated secret.

---

## 🔄 **SYSTEMD SERVICE (Auto-Start)**

### **Step 1: Create Service File**

```bash
sudo nano /etc/systemd/system/lifeasy.service
```

Paste content from [`lifeasy.service`](lifeasy.service)

### **Step 2: Enable Service**

```bash
sudo systemctl daemon-reload
sudo systemctl enable lifeasy
sudo systemctl start lifeasy
```

### **Step 3: Check Status**

```bash
sudo systemctl status lifeasy
```

### **Step 4: View Logs**

```bash
sudo journalctl -u lifeasy -f
```

---

## 📊 **MONITORING & MAINTENANCE**

### **Database Backups**

```bash
# Backup script
nano /home/lifeasy/backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y-%m-%d_%H%M%S)
pg_dump -U lifeasy_user lifeasy > /backups/lifeasy_$DATE.sql
find /backups -name "*.sql" -mtime +7 -delete
```

```bash
chmod +x backup.sh

# Add to crontab
crontab -e
0 2 * * * /home/lifeasy/backup.sh
```

### **Monitor Disk Space**

```bash
df -h
```

### **Monitor Memory**

```bash
free -h
```

### **Check Logs**

```bash
# Nginx logs
tail -f /var/log/nginx/lifeasy_access.log
tail -f /var/log/nginx/lifeasy_error.log

# Application logs
sudo journalctl -u lifeasy -f
```

---

## 🎯 **DEPLOYMENT CHECKLIST**

### **Pre-Deployment:**

- [ ] VPS provisioned
- [ ] Domain purchased (Namecheap, GoDaddy)
- [ ] DNS configured (point to server IP)
- [ ] SSH access working
- [ ] Firewall rules set

### **During Deployment:**

- [ ] PostgreSQL installed & configured
- [ ] Python packages installed
- [ ] Environment variables set
- [ ] Database seeded
- [ ] Nginx configured
- [ ] SSL certificate installed

### **Post-Deployment:**

- [ ] Backend accessible at `https://api.lifeasy.com/docs`
- [ ] Mobile app updated with new URL
- [ ] Login tested successfully
- [ ] Monitoring setup
- [ ] Backups configured
- [ ] Documentation updated

---

## 🔑 **PRODUCTION CREDENTIALS**

```
Tenant ID:  1001
Password:   123456
Auth Type:  JWT + Bcrypt
Token Expiry: 30 minutes
```

---

## 📞 **DOMAIN CONFIGURATION**

### **DNS Records (at Namecheap/GoDaddy):**

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | your_server_ip | Automatic |
| A | api | your_server_ip | Automatic |
| CNAME | www | api.lifeasy.com | Automatic |

---

## 💰 **COST BREAKDOWN**

| Item | Cost |
|------|------|
| VPS (DigitalOcean/Hetzner) | $5/month |
| Domain (Namecheap) | $10/year |
| SSL Certificate (Let's Encrypt) | FREE |
| **TOTAL** | ~$70/year |

---

## 🚨 **TROUBLESHOOTING**

### **Backend won't start:**

```bash
sudo systemctl status lifeasy
sudo journalctl -u lifeasy -f
```

### **Database connection error:**

```bash
sudo systemctl status postgresql
psql -U lifeasy_user -d lifeasy -h localhost
```

### **Nginx errors:**

```bash
sudo nginx -t
sudo systemctl status nginx
```

### **SSL issues:**

```bash
sudo certbot certificates
sudo certbot renew --dry-run
```

---

## 🎉 **SUCCESS!**

Your LIFEASY V30 PRO is now deployed with:

✅ Production-grade architecture  
✅ PostgreSQL database  
✅ JWT + Bcrypt authentication  
✅ HTTPS/SSL encryption  
✅ Nginx reverse proxy  
✅ Auto-start on boot  
✅ Automated backups  
✅ Security hardening  

**🏢 LIFEASY V30 PRO - PRODUCTION READY!**  
*Enterprise-grade apartment management system*

---

**Last Updated:** 2026-03-17  
**Version:** 30.0.0  
**Status:** Production Ready ✅
