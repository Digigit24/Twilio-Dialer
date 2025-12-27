# Twilio VoIP & WebRTC CRM - System Architecture

## Table of Contents
1. [Overview](#overview)
2. [System Components](#system-components)
3. [Architecture Diagram](#architecture-diagram)
4. [Database Schema](#database-schema)
5. [Technology Stack](#technology-stack)
6. [Data Flow](#data-flow)
7. [Security](#security)

---

## Overview

This system integrates Twilio's Programmable Voice and WebRTC capabilities into a Django-based CRM platform, enabling browser-based and mobile calling with comprehensive call tracking and recording features.

### Key Features
- **WebRTC Calling**: Browser and mobile app calling via Twilio Voice SDK
- **Call Management**: Track all incoming and outgoing calls
- **Call Recording**: Automatic recording with secure storage and playback
- **Role-Based Access**: Agent and Manager roles with different permissions
- **Real-time Webhooks**: Twilio webhook integration for call status updates
- **REST API**: Complete API for web and mobile applications
- **Analytics**: Call statistics and agent performance metrics

---

## System Components

### 1. Frontend Applications
- **Web Application**: Browser-based calling interface using Twilio Voice SDK for JavaScript
- **Android Application**: Mobile calling app using Twilio Voice SDK for Android
- Both consume the same REST API endpoints

### 2. Django Backend

#### Apps Structure
```
twilio_crm/
├── accounts/          # User management and authentication
├── calls/             # Call management and Twilio integration
├── api/               # REST API endpoints
└── twilio_crm/        # Project settings and configuration
```

#### Key Modules

**accounts app**
- Custom User model with roles (Agent, Manager, Admin)
- Agent availability management
- Twilio client identity mapping

**calls app**
- Call logging and tracking
- Call recording management
- Lead and Contact management
- Twilio service layer
- Webhook handlers

**api app**
- RESTful API endpoints
- JWT authentication
- Custom permissions
- Serializers for all models

### 3. Twilio Integration

#### Components Used
- **Twilio Programmable Voice**: Call initiation and routing
- **Twilio Voice SDK**: WebRTC client for browser/mobile
- **TwiML**: Call flow control
- **Call Recordings**: Automatic recording storage
- **Webhooks**: Real-time call status updates

#### Twilio Flow
1. Client requests access token from backend
2. Backend generates JWT with Voice Grant
3. Client initializes Twilio Voice SDK with token
4. Client can make/receive calls through Twilio
5. Twilio sends webhooks for call events
6. Backend processes webhooks and updates database

### 4. External Services
- **Twilio API**: Voice services and recording storage
- **PostgreSQL** (optional): Production database
- **Redis**: Celery task queue (for async operations)
- **Celery**: Background task processing

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
├──────────────────────────┬──────────────────────────────────────┤
│   Web Browser (React)    │   Android App (Native/React Native)  │
│   - Twilio Voice SDK     │   - Twilio Voice SDK                 │
│   - WebRTC Audio         │   - WebRTC Audio                     │
└──────────┬───────────────┴────────────────┬─────────────────────┘
           │                                 │
           │ HTTPS / REST API (JWT Auth)     │
           │                                 │
┌──────────▼─────────────────────────────────▼─────────────────────┐
│                    Django REST Framework                          │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │    Auth     │  │     API      │  │  Webhook Handlers      │  │
│  │   (JWT)     │  │  Endpoints   │  │  - Call Status         │  │
│  └─────────────┘  └──────────────┘  │  - Recording Status    │  │
│                                      │  - Incoming Calls      │  │
│  ┌─────────────┐  ┌──────────────┐  └────────────────────────┘  │
│  │   Models    │  │   Services   │                               │
│  │ - User      │  │ - Twilio     │                               │
│  │ - Call      │  │ - Recording  │                               │
│  │ - Recording │  │              │                               │
│  │ - Lead      │  │              │                               │
│  │ - Contact   │  │              │                               │
│  └─────────────┘  └──────────────┘                               │
│                                                                   │
└──────────┬────────────────────────────────────┬──────────────────┘
           │                                     │
           │                                     │ Webhooks
           │                                     │
┌──────────▼────────────┐              ┌────────▼─────────────────┐
│   Database (SQLite/   │              │   Twilio Platform        │
│   PostgreSQL)         │              ├──────────────────────────┤
├───────────────────────┤              │ - Programmable Voice     │
│ - Users               │              │ - WebRTC Gateway         │
│ - Calls               │              │ - Call Recordings        │
│ - Recordings          │              │ - TwiML Apps             │
│ - Leads               │              │ - Phone Numbers          │
│ - Contacts            │              └──────────────────────────┘
└───────────────────────┘

┌───────────────────────────────────────────────────────────────────┐
│                     Background Services                            │
├───────────────────────────────────────────────────────────────────┤
│  Redis                    Celery Workers                           │
│  - Task Queue             - Recording Downloads                    │
│  - Cache                  - Async Processing                       │
└───────────────────────────────────────────────────────────────────┘
```

---

## Database Schema

### User Model
```python
User
├── id (PK)
├── username
├── email
├── first_name
├── last_name
├── role (ADMIN, MANAGER, AGENT)
├── phone_number
├── extension
├── is_available (boolean)
├── twilio_client_identity
├── created_at
└── updated_at
```

### Lead Model
```python
Lead
├── id (PK)
├── first_name
├── last_name
├── email
├── phone_number
├── company
├── status (NEW, CONTACTED, QUALIFIED, CONVERTED, LOST)
├── assigned_to (FK → User)
├── notes
├── created_at
└── updated_at
```

### Contact Model
```python
Contact
├── id (PK)
├── first_name
├── last_name
├── email
├── phone_number
├── company
├── position
├── assigned_to (FK → User)
├── notes
├── created_at
└── updated_at
```

### Call Model
```python
Call
├── id (PK)
├── call_sid (unique, indexed)
├── parent_call_sid
├── direction (INBOUND, OUTBOUND)
├── status (INITIATED, RINGING, IN_PROGRESS, COMPLETED, etc.)
├── from_number
├── to_number
├── agent (FK → User)
├── lead (FK → Lead, nullable)
├── contact (FK → Contact, nullable)
├── duration (seconds)
├── start_time
├── end_time
├── call_notes
├── tags
├── created_at
└── updated_at
```

### CallRecording Model
```python
CallRecording
├── id (PK)
├── call (FK → Call)
├── recording_sid (unique, indexed)
├── recording_url
├── duration (seconds)
├── file_size (bytes)
├── status (PROCESSING, COMPLETED, FAILED, DELETED)
├── local_file
├── is_transcribed
├── transcription
├── created_at
└── updated_at
```

### Entity Relationships
```
User ─┬─(1:N)─> Lead
      ├─(1:N)─> Contact
      └─(1:N)─> Call

Call ─┬─(N:1)─> User (agent)
      ├─(N:1)─> Lead (optional)
      ├─(N:1)─> Contact (optional)
      └─(1:N)─> CallRecording

CallRecording ─(N:1)─> Call
```

---

## Technology Stack

### Backend
- **Python 3.10+**
- **Django 4.2**: Web framework
- **Django REST Framework**: API development
- **djangorestframework-simplejwt**: JWT authentication
- **Twilio Python SDK**: Twilio API integration
- **Celery**: Asynchronous task processing
- **Redis**: Message broker and cache

### Frontend (Not Included)
- **Web**: React/Vue.js + Twilio Voice SDK for JavaScript
- **Android**: Kotlin/Java + Twilio Voice SDK for Android

### Database
- **Development**: SQLite
- **Production**: PostgreSQL (recommended)

### Infrastructure
- **Web Server**: Gunicorn/uWSGI
- **Reverse Proxy**: Nginx
- **SSL/TLS**: Let's Encrypt (for webhooks)

---

## Data Flow

### 1. Outbound Call Flow
```
1. Agent initiates call via web/mobile app
   ├─> POST /api/calls/initiate/
   └─> {to_number, from_number, lead_id}

2. Backend creates Call record
   └─> Status: INITIATED

3. Backend calls Twilio API
   └─> twilio_service.make_call()

4. Twilio initiates call
   └─> Requests TwiML from /webhooks/voice/

5. Backend returns TwiML
   └─> <Dial> instruction with recording

6. Call progresses through states
   ├─> RINGING
   ├─> IN_PROGRESS
   └─> COMPLETED

7. Twilio sends status webhooks
   └─> POST /webhooks/call-status/

8. Backend updates Call record
   └─> Updates status, duration, timestamps

9. If recorded, Twilio sends recording webhook
   └─> POST /webhooks/recording-status/

10. Backend creates CallRecording record
    └─> Saves recording URL and metadata
```

### 2. Inbound Call Flow
```
1. Call comes to Twilio number
   └─> Twilio requests TwiML

2. Twilio sends webhook
   └─> POST /webhooks/incoming-call/

3. Backend finds available agent
   └─> Query: User.filter(role=AGENT, is_available=True)

4. Backend creates Call record
   └─> Direction: INBOUND, Status: RINGING

5. Backend returns TwiML
   └─> <Dial><Client>agent_identity</Client></Dial>

6. Agent's client rings
   └─> Push notification or in-app alert

7. Agent answers call
   └─> WebRTC connection established

8. Call status updates via webhooks
   └─> RINGING → IN_PROGRESS → COMPLETED

9. Recording webhook received
   └─> CallRecording created
```

### 3. Access Token Generation
```
1. Client requests token
   └─> POST /api/twilio/token/

2. Backend authenticates user (JWT)
   └─> Validates Bearer token

3. Backend generates Twilio Access Token
   ├─> Identity: user_{user_id}
   ├─> Voice Grant with App SID
   └─> TTL: 1 hour

4. Returns token to client
   └─> {token, identity}

5. Client initializes Twilio Device
   └─> Twilio.Device.setup(token)

6. Client ready for calls
   └─> Can make/receive calls
```

---

## Security

### 1. Authentication
- **JWT Tokens**: Secure API access with short-lived access tokens
- **Token Refresh**: Long-lived refresh tokens for session management
- **HTTPS Only**: All API communication over TLS

### 2. Authorization
- **Role-Based Access Control (RBAC)**
  - Agents: Access only their own calls, leads, contacts
  - Managers: Full access to all resources
  - Admins: System-wide administrative access

- **Permission Classes**
  - `IsAgent`: Agent-only endpoints
  - `IsManager`: Manager/Admin only
  - `IsOwnerOrManager`: Resource owner or manager
  - `IsManagerOrReadOnly`: Read-only for non-managers

### 3. Twilio Security
- **Webhook Signature Validation**: Verify all webhooks from Twilio
- **Credential Management**: Store in environment variables, never commit
- **Access Token Scoping**: Limit grants to necessary permissions only
- **Token Expiration**: Short TTL on access tokens (1 hour)

### 4. Data Protection
- **Sensitive Data**: Call recordings stored securely
- **Access Logs**: Track who accesses recordings
- **CORS Configuration**: Whitelist allowed origins
- **CSRF Protection**: Django CSRF middleware for state-changing operations

### 5. Best Practices
- Regular security audits
- Input validation and sanitization
- SQL injection prevention (Django ORM)
- XSS protection (DRF serializers)
- Rate limiting (recommended for production)
- Regular dependency updates

---

## Scalability Considerations

### Horizontal Scaling
- **Stateless API**: Easy to load balance across multiple instances
- **Database Connection Pooling**: Use pgbouncer for PostgreSQL
- **Celery Workers**: Scale independently for background tasks

### Performance Optimization
- **Database Indexing**: On frequently queried fields (call_sid, agent, status)
- **Query Optimization**: select_related and prefetch_related for JOINs
- **Caching**: Redis for frequently accessed data
- **Pagination**: Limit API response sizes

### Monitoring
- **Logging**: Comprehensive logging at all layers
- **Error Tracking**: Sentry or similar
- **Performance Monitoring**: New Relic, DataDog
- **Twilio Monitoring**: Use Twilio Console for call quality metrics

---

## Deployment Architecture

### Production Recommendation
```
Internet
    │
    ▼
┌─────────────────┐
│  Load Balancer  │
│   (AWS ELB)     │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐  ┌───────┐
│Django │  │Django │  (Multiple instances)
│+ Gun  │  │+ Gun  │
│icorn  │  │icorn  │
└───┬───┘  └───┬───┘
    │          │
    └────┬─────┘
         ▼
   ┌──────────┐      ┌──────────┐
   │PostgreSQL│      │  Redis   │
   │ (Primary)│      │  Cluster │
   └──────────┘      └──────────┘
         │
         ▼
   ┌──────────┐      ┌──────────┐
   │PostgreSQL│      │  Celery  │
   │ (Replica)│      │ Workers  │
   └──────────┘      └──────────┘
```

---

This architecture provides a robust, scalable foundation for a production-grade Twilio VoIP CRM system.
