#!/bin/bash
# LIFEASY V30 PRO - Production Server Setup Script
# For Ubuntu/Debian VPS (DigitalOcean, Hetzner, etc.)

echo "🚀 LIFEASY V30 PRO - Production Server Setup"
echo "============================================="
echo ""

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
echo "🐍 Installing Python..."
sudo apt install -y python3 python3-pip python3-venv

# Install PostgreSQL
echo "🐘 Installing PostgreSQL..."
sudo apt install -y postgresql postgresql-contrib

# Install Nginx
echo "🌐 Installing Nginx..."
sudo apt install -y nginx

# Install system dependencies
echo "📚 Installing system libraries..."
sudo apt install -y libpq-dev gcc

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /var/www/lifeasy
cd /var/www/lifeasy

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "📦 Installing Python packages..."
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary python-jose passlib[bcrypt] pydantic

# Setup PostgreSQL database
echo "🗄️ Setting up PostgreSQL database..."
sudo -u postgres psql << EOF
CREATE DATABASE lifeasy;
CREATE USER lifeasy_user WITH PASSWORD 'CHANGE_THIS_PASSWORD_IN_PRODUCTION';
GRANT ALL PRIVILEGES ON DATABASE lifeasy TO lifeasy_user;
ALTER DATABASE lifeasy OWNER TO lifeasy_user;
EOF

# Configure environment variables
echo "⚙️ Creating environment configuration..."
cat > .env << EOL
LIFEASY_ENV=production
DATABASE_URL=postgresql://lifeasy_user:CHANGE_THIS_PASSWORD_IN_PRODUCTION@localhost/lifeasy
JWT_SECRET=CHANGE_THIS_TO_SECURE_RANDOM_STRING_IN_PRODUCTION
TOKEN_EXPIRY=30
HOST=0.0.0.0
PORT=8000
EOL

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 NEXT STEPS:"
echo "   1. Copy your backend files to /var/www/lifeasy/"
echo "   2. Update .env file with secure passwords"
echo "   3. Run: python3 seed_prod.py"
echo "   4. Configure Nginx (see nginx_config.txt)"
echo "   5. Setup SSL with Certbot"
echo "   6. Start with: uvicorn main_prod:app --host 0.0.0.0 --port 8000"
echo ""
echo "🔒 SECURITY REMINDER:"
echo "   - Change all default passwords"
echo "   - Use strong JWT secret"
echo "   - Enable firewall (ufw)"
echo "   - Setup automatic security updates"
