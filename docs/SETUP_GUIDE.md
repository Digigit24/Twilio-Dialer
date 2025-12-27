# Twilio VoIP CRM - Setup & Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Twilio Setup](#twilio-setup)
3. [Local Development Setup](#local-development-setup)
4. [Database Setup](#database-setup)
5. [Running the Application](#running-the-application)
6. [Creating Test Users](#creating-test-users)
7. [Testing the API](#testing-the-api)
8. [Production Deployment](#production-deployment)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- Python 3.10 or higher
- pip (Python package manager)
- Git
- PostgreSQL 13+ (for production) or SQLite (for development)
- Redis 6+ (for Celery)

### Optional
- Docker & Docker Compose (for containerized deployment)
- ngrok (for local webhook testing)

---

## Twilio Setup

### 1. Create Twilio Account
1. Go to [twilio.com](https://www.twilio.com)
2. Sign up for a free account
3. Verify your email and phone number

### 2. Get Twilio Credentials
1. Navigate to the [Twilio Console](https://console.twilio.com)
2. Copy your **Account SID** and **Auth Token** from the dashboard

### 3. Get a Twilio Phone Number
1. Go to **Phone Numbers** → **Manage** → **Buy a number**
2. Choose a number with **Voice** capabilities
3. Purchase the number (free with trial account)
4. Note the phone number (format: +1XXXXXXXXXX)

### 4. Create TwiML App
1. Go to **Voice** → **Manage** → **TwiML Apps**
2. Click **Create new TwiML App**
3. Set **Friendly Name**: "CRM Voice App"
4. Set **Voice Request URL**: `https://your-domain.com/webhooks/voice/` (update later)
5. Set **Voice Status Callback URL**: `https://your-domain.com/webhooks/call-status/`
6. Click **Save**
7. Copy the **TwiML App SID** (starts with AP...)

### 5. Configure Phone Number
1. Go to **Phone Numbers** → **Manage** → **Active numbers**
2. Click on your purchased number
3. Under **Voice Configuration**:
   - **Configure with**: Webhooks, TwiML Apps, Functions, Studio, or Proxy
   - **A call comes in**: TwiML App → Select "CRM Voice App"
   - **Status Callback URL**: `https://your-domain.com/webhooks/call-status/`
   - **Record Calls**: Do not record
4. Click **Save**

---

## Local Development Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd Twilio-Dialer
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Update the following in `.env`:
```env
# Django Settings
SECRET_KEY=your-random-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Twilio Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX
TWILIO_APP_SID=APxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Generate SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Database Setup

### Option 1: SQLite (Development)
SQLite is used by default and requires no additional setup.

### Option 2: PostgreSQL (Recommended for Production)

#### Install PostgreSQL
```bash
# macOS
brew install postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Windows
# Download from https://www.postgresql.org/download/windows/
```

#### Create Database
```bash
# Start PostgreSQL
sudo service postgresql start  # Linux
brew services start postgresql  # macOS

# Create database and user
sudo -u postgres psql

postgres=# CREATE DATABASE twilio_crm;
postgres=# CREATE USER twilio_user WITH PASSWORD 'secure_password';
postgres=# ALTER ROLE twilio_user SET client_encoding TO 'utf8';
postgres=# ALTER ROLE twilio_user SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE twilio_user SET timezone TO 'UTC';
postgres=# GRANT ALL PRIVILEGES ON DATABASE twilio_crm TO twilio_user;
postgres=# \q
```

#### Update Django Settings
Edit `twilio_crm/settings.py` and uncomment the PostgreSQL configuration:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'twilio_crm'),
        'USER': os.getenv('DB_USER', 'twilio_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'secure_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

Update `.env`:
```env
DB_NAME=twilio_crm
DB_USER=twilio_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432
```

### Run Migrations
```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

---

## Running the Application

### 1. Create Superuser
```bash
python manage.py createsuperuser

# Follow prompts:
# Username: admin
# Email: admin@example.com
# Password: ********
```

### 2. Start Development Server
```bash
python manage.py runserver
```

The server will start at: `http://localhost:8000`

### 3. Access Admin Panel
Navigate to: `http://localhost:8000/admin`
Login with superuser credentials

### 4. Access API Documentation
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

---

## Creating Test Users

### Via Admin Panel
1. Go to `http://localhost:8000/admin`
2. Click **Users** → **Add User**
3. Fill in details:
   - Username: `agent1`
   - Password: `testpass123`
4. Click **Save and continue editing**
5. Set additional fields:
   - First name: John
   - Last name: Doe
   - Role: AGENT
   - Is available: ✓
6. Click **Save**

### Via Django Shell
```bash
python manage.py shell
```

```python
from accounts.models import User

# Create Agent
agent = User.objects.create_user(
    username='agent1',
    email='agent1@example.com',
    password='testpass123',
    first_name='John',
    last_name='Doe',
    role=User.Role.AGENT,
    phone_number='+1234567890',
    extension='101',
    is_available=True
)

# Create Manager
manager = User.objects.create_user(
    username='manager1',
    email='manager1@example.com',
    password='testpass123',
    first_name='Jane',
    last_name='Smith',
    role=User.Role.MANAGER,
    phone_number='+1234567891',
    extension='200',
    is_available=True
)

print("Users created successfully!")
```

---

## Testing the API

### 1. Get Access Token
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "agent1",
    "password": "testpass123"
  }'
```

**Response:**
```json
{
  "refresh": "eyJ0eXAi...",
  "access": "eyJ0eXAi..."
}
```

### 2. Get User Profile
```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer <access_token>"
```

### 3. Generate Twilio Token
```bash
curl -X POST http://localhost:8000/api/twilio/token/ \
  -H "Authorization: Bearer <access_token>"
```

### 4. Create Lead
```bash
curl -X POST http://localhost:8000/api/leads/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "Lead",
    "phone_number": "+1555123456",
    "company": "Test Corp",
    "status": "NEW"
  }'
```

### 5. Initiate Test Call (Optional)
```bash
curl -X POST http://localhost:8000/api/calls/initiate/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "to_number": "+1555123456",
    "record": true
  }'
```

---

## Setting Up Webhooks for Local Development

### Using ngrok

#### 1. Install ngrok
```bash
# macOS
brew install ngrok

# Or download from https://ngrok.com/download
```

#### 2. Start ngrok
```bash
ngrok http 8000
```

**Output:**
```
Forwarding https://abc123.ngrok.io -> http://localhost:8000
```

#### 3. Update Twilio Configuration
1. Go to Twilio Console
2. Update your TwiML App URLs:
   - Voice URL: `https://abc123.ngrok.io/webhooks/voice/`
   - Status Callback: `https://abc123.ngrok.io/webhooks/call-status/`
3. Update Phone Number:
   - Voice URL: Use the TwiML App
   - Or set directly: `https://abc123.ngrok.io/webhooks/incoming-call/`

#### 4. Update Django Settings
Add ngrok URL to `ALLOWED_HOSTS` in `.env`:
```env
ALLOWED_HOSTS=localhost,127.0.0.1,abc123.ngrok.io
```

Restart Django server for changes to take effect.

---

## Running with Celery (Optional)

### 1. Install Redis
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo service redis-server start
```

### 2. Start Celery Worker
```bash
# In a new terminal window
celery -A twilio_crm worker -l info
```

### 3. Start Celery Beat (for scheduled tasks)
```bash
# In another terminal window
celery -A twilio_crm beat -l info
```

---

## Production Deployment

### 1. Server Setup

#### Update Settings
Edit `twilio_crm/settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
```

Update `.env`:
```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
SECRET_KEY=use-a-very-strong-secret-key-here
```

### 2. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 3. Install Production Server

#### Install Gunicorn
```bash
pip install gunicorn
```

#### Create Gunicorn Configuration
`gunicorn.conf.py`:
```python
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "-"
accesslog = "-"
```

#### Run Gunicorn
```bash
gunicorn twilio_crm.wsgi:application -c gunicorn.conf.py
```

### 4. Nginx Configuration

Install Nginx:
```bash
sudo apt-get install nginx
```

Create configuration: `/etc/nginx/sites-available/twilio_crm`
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/Twilio-Dialer/staticfiles/;
    }

    location /media/ {
        alias /path/to/Twilio-Dialer/media/;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/twilio_crm /etc/nginx/sites-enabled/
sudo nginx -t
sudo service nginx restart
```

### 5. SSL/TLS with Let's Encrypt

Install Certbot:
```bash
sudo apt-get install certbot python3-certbot-nginx
```

Get certificate:
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 6. Systemd Service

Create service file: `/etc/systemd/system/twilio_crm.service`
```ini
[Unit]
Description=Twilio CRM Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/Twilio-Dialer
Environment="PATH=/path/to/Twilio-Dialer/venv/bin"
ExecStart=/path/to/Twilio-Dialer/venv/bin/gunicorn \
          --workers 4 \
          --bind 0.0.0.0:8000 \
          twilio_crm.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable twilio_crm
sudo systemctl start twilio_crm
sudo systemctl status twilio_crm
```

### 7. Celery Service

Create service file: `/etc/systemd/system/celery.service`
```ini
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/path/to/Twilio-Dialer
Environment="PATH=/path/to/Twilio-Dialer/venv/bin"
ExecStart=/path/to/Twilio-Dialer/venv/bin/celery -A twilio_crm worker -l info

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable celery
sudo systemctl start celery
```

### 8. Update Twilio Webhooks
Update all webhook URLs in Twilio Console to use your production domain:
- `https://your-domain.com/webhooks/voice/`
- `https://your-domain.com/webhooks/call-status/`
- `https://your-domain.com/webhooks/recording-status/`
- `https://your-domain.com/webhooks/incoming-call/`

---

## Docker Deployment (Alternative)

### Dockerfile
```dockerfile
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "twilio_crm.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=twilio_crm
      - POSTGRES_USER=twilio_user
      - POSTGRES_PASSWORD=secure_password

  redis:
    image: redis:6-alpine

  web:
    build: .
    command: gunicorn twilio_crm.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

  celery:
    build: .
    command: celery -A twilio_crm worker -l info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Deploy with Docker
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## Troubleshooting

### Issue: Migrations Error
```bash
# Reset migrations (development only!)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
python manage.py makemigrations
python manage.py migrate
```

### Issue: Twilio Webhook Signature Validation Failed
- Ensure webhook URLs are publicly accessible
- Verify `TWILIO_AUTH_TOKEN` is correct
- Check that URLs use HTTPS in production

### Issue: No Audio in WebRTC Calls
- Check browser permissions for microphone
- Verify Twilio token is valid
- Ensure TwiML App is properly configured

### Issue: Calls Not Recording
- Verify `record=True` in call initiation
- Check TwiML includes `record="record-from-answer"`
- Ensure recording webhook URL is configured

### Issue: Database Connection Error
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database user has proper permissions

### Check Logs
```bash
# Django logs
tail -f logs/twilio_crm.log

# Nginx logs
tail -f /var/log/nginx/error.log

# System service logs
sudo journalctl -u twilio_crm -f
sudo journalctl -u celery -f
```

---

## Next Steps

1. **Implement Frontend**: Build web UI with React/Vue.js using the API
2. **Android App**: Develop mobile app using Twilio Voice SDK for Android
3. **Add Features**:
   - Call transfer between agents
   - Call queuing
   - Real-time notifications
   - Call transcription
4. **Monitoring**: Set up logging, error tracking (Sentry), performance monitoring
5. **Backups**: Implement automated database backups
6. **Testing**: Add unit tests and integration tests

---

For additional help, refer to:
- [Django Documentation](https://docs.djangoproject.com/)
- [Twilio Voice Documentation](https://www.twilio.com/docs/voice)
- [Django REST Framework](https://www.django-rest-framework.org/)
