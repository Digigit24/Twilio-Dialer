# Twilio VoIP & WebRTC CRM System

A comprehensive Django-based CRM system integrated with Twilio Programmable Voice and WebRTC for browser-based and mobile calling, featuring call tracking, recording, and analytics.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/django-4.2-green.svg)
![Twilio](https://img.shields.io/badge/twilio-voice-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## Features

### Core Functionality
- **WebRTC Calling**: Browser and mobile app calling via Twilio Voice SDK
- **Click-to-Call**: Initiate calls directly from CRM interface
- **Call Management**: Track all incoming and outgoing calls with detailed logs
- **Automatic Recording**: Record calls with secure storage and playback
- **Lead & Contact Management**: Associate calls with leads and contacts
- **Real-time Status**: Live call status updates via Twilio webhooks

### User Roles & Permissions
- **Sales Agents**: Make/receive calls, view own call history and recordings
- **Managers**: View all team calls, access all recordings, manage agents
- **Admins**: Full system access and configuration

### Analytics & Reporting
- Call statistics (total, incoming, outgoing, duration, etc.)
- Per-agent performance metrics
- Call history filtering and search
- Recording management and playback

### API Features
- RESTful API for web and mobile applications
- JWT authentication with token refresh
- Comprehensive filtering, search, and pagination
- Interactive API documentation (Swagger/ReDoc)

---

## Technology Stack

**Backend:**
- Django 4.2
- Django REST Framework
- Twilio Python SDK
- JWT Authentication
- PostgreSQL / SQLite
- Celery + Redis (async tasks)

**Frontend (Not Included):**
- Web: React/Vue.js + Twilio Voice SDK for JavaScript
- Android: Kotlin/Java + Twilio Voice SDK for Android

---

## Quick Start

### Prerequisites
- Python 3.10+
- Twilio Account with:
  - Account SID
  - Auth Token
  - Phone Number (with Voice capability)
  - TwiML App SID

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Twilio-Dialer
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Twilio credentials
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Admin Panel: http://localhost:8000/admin
   - API Docs: http://localhost:8000/api/docs/
   - API: http://localhost:8000/api/

---

## Configuration

### Twilio Setup

Configure your Twilio credentials in `.env`:
```env
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number
TWILIO_APP_SID=your-twiml-app-sid
```

**Next Steps:**
1. Get your Twilio credentials from [Twilio Console](https://console.twilio.com)
2. Purchase a Twilio phone number with Voice capability
3. Create a TwiML App in Twilio Console
4. Configure webhook URLs (see [Setup Guide](docs/SETUP_GUIDE.md))
5. Update all credentials in `.env`

### Environment Variables

See `.env.example` for all available configuration options.

Key settings:
- `SECRET_KEY`: Django secret key (generate a new one for production)
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Your domain names
- `TWILIO_*`: Twilio credentials
- `DB_*`: Database configuration (optional, defaults to SQLite)

---

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Architecture Documentation](docs/ARCHITECTURE.md)**: System design, components, and data flow
- **[API Documentation](docs/API_DOCUMENTATION.md)**: Complete API reference with examples
- **[Setup Guide](docs/SETUP_GUIDE.md)**: Detailed installation and deployment instructions

---

## API Overview

### Authentication
```bash
# Login
POST /api/auth/login/
{
  "username": "agent1",
  "password": "password123"
}

# Response
{
  "access": "eyJ0eXAiOiJKV1Q...",
  "refresh": "eyJ0eXAiOiJKV1Q..."
}
```

### Generate Twilio Token
```bash
POST /api/twilio/token/
Authorization: Bearer <access_token>

# Response
{
  "token": "eyJ0eXAiOiJKV1Q...",
  "identity": "user_1"
}
```

### Initiate Call
```bash
POST /api/calls/initiate/
Authorization: Bearer <access_token>
{
  "to_number": "+1555123456",
  "lead_id": 5,
  "record": true
}
```

### Get Call History
```bash
GET /api/calls/?ordering=-created_at
Authorization: Bearer <access_token>
```

### Get Statistics
```bash
GET /api/statistics/calls/?start_date=2024-01-01
Authorization: Bearer <access_token>
```

For complete API documentation, visit `/api/docs/` when the server is running.

---

## Database Schema

### Core Models

**User**
- Custom user model with roles (Agent, Manager, Admin)
- Availability status for call routing
- Twilio client identity mapping

**Call**
- Call SID, direction, status
- Caller and receiver numbers
- Agent assignment
- Lead/Contact association
- Duration and timestamps
- Call notes and tags

**CallRecording**
- Recording SID and URL
- Duration and file size
- Transcription support
- Local file storage

**Lead & Contact**
- Contact information
- Agent assignment
- Status tracking
- Associated call history

See [Architecture Documentation](docs/ARCHITECTURE.md) for detailed schema diagrams.

---

## Project Structure

```
Twilio-Dialer/
├── accounts/               # User management
│   ├── models.py          # Custom User model
│   └── admin.py           # User admin
├── calls/                 # Call management
│   ├── models.py          # Call, Recording, Lead, Contact models
│   ├── services.py        # Twilio service layer
│   ├── views.py           # Webhook handlers
│   └── admin.py           # Call admin
├── api/                   # REST API
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API viewsets
│   ├── permissions.py     # Custom permissions
│   └── urls.py            # API routing
├── twilio_crm/            # Project settings
│   ├── settings.py        # Django configuration
│   ├── urls.py            # URL routing
│   └── celery.py          # Celery configuration
├── docs/                  # Documentation
│   ├── ARCHITECTURE.md
│   ├── API_DOCUMENTATION.md
│   └── SETUP_GUIDE.md
├── media/                 # Media files
│   └── recordings/        # Call recordings
├── logs/                  # Application logs
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── .env                   # Your configuration
└── manage.py              # Django management
```

---

## Webhooks

Twilio sends webhooks to your backend for real-time updates. Configure these URLs in the Twilio Console:

| Webhook | URL | Purpose |
|---------|-----|---------|
| Voice URL | `/webhooks/voice/` | TwiML for outbound calls |
| Call Status | `/webhooks/call-status/` | Call status updates |
| Recording Status | `/webhooks/recording-status/` | Recording completion |
| Incoming Call | `/webhooks/incoming-call/` | Route incoming calls |

**Development:** Use [ngrok](https://ngrok.com/) to expose local server for webhook testing.

**Production:** Ensure all webhook URLs use HTTPS with valid SSL certificates.

---

## Deployment

### Development
```bash
python manage.py runserver
```

### Production

**With Gunicorn:**
```bash
gunicorn twilio_crm.wsgi:application --bind 0.0.0.0:8000
```

**With Docker:**
```bash
docker-compose up -d
```

**With Systemd:**
See [Setup Guide](docs/SETUP_GUIDE.md) for complete production deployment instructions.

---

## Testing

### Create Test Users

Via Django shell:
```bash
python manage.py shell
```

```python
from accounts.models import User

# Create Agent
User.objects.create_user(
    username='agent1',
    password='testpass123',
    first_name='John',
    last_name='Doe',
    role=User.Role.AGENT,
    phone_number='+1234567890',
    extension='101'
)

# Create Manager
User.objects.create_user(
    username='manager1',
    password='testpass123',
    first_name='Jane',
    last_name='Smith',
    role=User.Role.MANAGER
)
```

### Test API

See [API Documentation](docs/API_DOCUMENTATION.md) for complete examples.

---

## Security

- **JWT Authentication**: Secure API access with token-based auth
- **Role-Based Access Control**: Agents see only their data, managers see all
- **Webhook Validation**: All Twilio webhooks are signature-validated
- **Environment Variables**: Credentials stored securely, never committed
- **HTTPS Required**: Production webhooks require SSL/TLS
- **CORS Configuration**: Whitelist allowed origins

---

## Roadmap

### Current Features
- ✅ WebRTC calling (browser/mobile)
- ✅ Call tracking and logging
- ✅ Automatic call recording
- ✅ Lead and contact management
- ✅ Role-based permissions
- ✅ REST API with JWT auth
- ✅ Call statistics and reporting
- ✅ Interactive API documentation

### Planned Features
- 🔄 Call transfer between agents
- 🔄 Call queuing system
- 🔄 Real-time notifications (WebSockets)
- 🔄 Call transcription (Twilio Speech Recognition)
- 🔄 IVR (Interactive Voice Response)
- 🔄 Call notes during calls
- 🔄 SMS integration
- 🔄 Email notifications
- 🔄 Advanced analytics dashboard

---

## Troubleshooting

### Common Issues

**Migrations Error:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Twilio Webhooks Not Working:**
- Verify webhook URLs are publicly accessible
- Use ngrok for local development
- Check webhook signature validation

**No Audio in Calls:**
- Verify browser microphone permissions
- Check Twilio token validity
- Ensure TwiML App configuration is correct

See [Setup Guide](docs/SETUP_GUIDE.md) for more troubleshooting tips.

---

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review Twilio Console for service status

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Acknowledgments

- [Django](https://www.djangoproject.com/)
- [Twilio](https://www.twilio.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Twilio Voice SDK](https://www.twilio.com/docs/voice/sdks)

---

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Built with ❤️ using Django and Twilio**
