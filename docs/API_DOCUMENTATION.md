# API Documentation

## Table of Contents
1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Lead Management](#lead-management)
4. [Contact Management](#contact-management)
5. [Call Management](#call-management)
6. [Recording Management](#recording-management)
7. [Statistics & Reporting](#statistics--reporting)
8. [Twilio Integration](#twilio-integration)
9. [Error Handling](#error-handling)

---

## Base URL
```
Development: http://localhost:8000/api
Production: https://your-domain.com/api
```

## Authentication

All API endpoints (except login) require JWT authentication.

### Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Login

**POST** `/auth/login/`

Get access and refresh tokens.

**Request:**
```json
{
  "username": "agent1",
  "password": "password123"
}
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token

**POST** `/auth/refresh/`

Get a new access token using refresh token.

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## User Management

### List Users

**GET** `/users/`

Get list of users.

**Permissions:** Managers see all, Agents see only themselves

**Query Parameters:**
- `role` - Filter by role (ADMIN, MANAGER, AGENT)
- `is_available` - Filter by availability (true/false)
- `search` - Search by username, name, email
- `ordering` - Sort by field (created_at, username)

**Response:**
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "agent1",
      "email": "agent1@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "AGENT",
      "phone_number": "+1234567890",
      "extension": "101",
      "is_available": true,
      "twilio_client_identity": "user_1",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Get Current User

**GET** `/users/me/`

Get current authenticated user's profile.

**Response:**
```json
{
  "id": 1,
  "username": "agent1",
  "email": "agent1@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "AGENT",
  "phone_number": "+1234567890",
  "extension": "101",
  "is_available": true,
  "twilio_client_identity": "user_1",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Create User

**POST** `/users/`

Create a new user.

**Permissions:** Manager/Admin only

**Request:**
```json
{
  "username": "newagent",
  "email": "newagent@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "password": "securepassword",
  "password_confirm": "securepassword",
  "role": "AGENT",
  "phone_number": "+1234567891",
  "extension": "102"
}
```

**Response:** 201 Created
```json
{
  "id": 2,
  "username": "newagent",
  "email": "newagent@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "role": "AGENT",
  "phone_number": "+1234567891",
  "extension": "102",
  "is_available": true,
  "twilio_client_identity": null,
  "created_at": "2024-01-15T11:00:00Z"
}
```

### Update User Availability

**POST** `/users/{id}/set_availability/`

Update agent availability status.

**Permissions:** Self or Manager

**Request:**
```json
{
  "is_available": false
}
```

**Response:**
```json
{
  "id": 1,
  "username": "agent1",
  "is_available": false,
  ...
}
```

---

## Lead Management

### List Leads

**GET** `/leads/`

Get list of leads.

**Permissions:** Agents see assigned leads, Managers see all

**Query Parameters:**
- `status` - Filter by status (NEW, CONTACTED, QUALIFIED, CONVERTED, LOST)
- `assigned_to` - Filter by assigned agent ID
- `search` - Search by name, email, phone, company
- `ordering` - Sort by field

**Response:**
```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "first_name": "Alice",
      "last_name": "Johnson",
      "full_name": "Alice Johnson",
      "email": "alice@company.com",
      "phone_number": "+1555123456",
      "company": "Tech Corp",
      "status": "NEW",
      "assigned_to": 1,
      "assigned_to_name": "John Doe",
      "notes": "Interested in product demo",
      "created_at": "2024-01-10T09:00:00Z",
      "updated_at": "2024-01-10T09:00:00Z"
    }
  ]
}
```

### Create Lead

**POST** `/leads/`

Create a new lead.

**Request:**
```json
{
  "first_name": "Bob",
  "last_name": "Williams",
  "email": "bob@startup.com",
  "phone_number": "+1555987654",
  "company": "Startup Inc",
  "status": "NEW",
  "assigned_to": 1,
  "notes": "Referral from existing client"
}
```

**Response:** 201 Created

### Update Lead

**PUT/PATCH** `/leads/{id}/`

Update lead information.

**Request:**
```json
{
  "status": "CONTACTED",
  "notes": "Called and left voicemail"
}
```

### Get Lead

**GET** `/leads/{id}/`

Get lead details.

### Delete Lead

**DELETE** `/leads/{id}/`

Delete a lead.

**Permissions:** Manager/Admin only

---

## Contact Management

### List Contacts

**GET** `/contacts/`

Get list of contacts.

**Permissions:** Agents see assigned contacts, Managers see all

**Query Parameters:**
- `assigned_to` - Filter by assigned agent ID
- `search` - Search by name, email, phone, company, position
- `ordering` - Sort by field

**Response:**
```json
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "first_name": "Charlie",
      "last_name": "Brown",
      "full_name": "Charlie Brown",
      "email": "charlie@enterprise.com",
      "phone_number": "+1555456789",
      "company": "Enterprise LLC",
      "position": "CTO",
      "assigned_to": 1,
      "assigned_to_name": "John Doe",
      "notes": "Key decision maker",
      "created_at": "2024-01-05T14:30:00Z",
      "updated_at": "2024-01-05T14:30:00Z"
    }
  ]
}
```

### Create Contact

**POST** `/contacts/`

Create a new contact.

**Request:**
```json
{
  "first_name": "Diana",
  "last_name": "Martinez",
  "email": "diana@company.com",
  "phone_number": "+1555111222",
  "company": "Big Corp",
  "position": "VP Sales",
  "assigned_to": 1,
  "notes": "Converted from lead"
}
```

### Update Contact

**PUT/PATCH** `/contacts/{id}/`

### Get Contact

**GET** `/contacts/{id}/`

### Delete Contact

**DELETE** `/contacts/{id}/`

**Permissions:** Manager/Admin only

---

## Call Management

### List Calls

**GET** `/calls/`

Get list of calls.

**Permissions:** Agents see their calls, Managers see all

**Query Parameters:**
- `direction` - Filter by direction (INBOUND, OUTBOUND)
- `status` - Filter by status (INITIATED, RINGING, IN_PROGRESS, COMPLETED, etc.)
- `agent` - Filter by agent ID
- `lead` - Filter by lead ID
- `contact` - Filter by contact ID
- `search` - Search by call_sid, phone numbers, notes
- `ordering` - Sort by field (default: -created_at)

**Response:**
```json
{
  "count": 100,
  "results": [
    {
      "id": 1,
      "call_sid": "CA1234567890abcdef",
      "direction": "OUTBOUND",
      "status": "COMPLETED",
      "from_number": "+17656456867",
      "to_number": "+1555123456",
      "agent_name": "John Doe",
      "duration": 180,
      "duration_formatted": "03:00",
      "start_time": "2024-01-15T10:00:00Z",
      "has_recording": true,
      "created_at": "2024-01-15T09:59:55Z"
    }
  ]
}
```

### Get Call Details

**GET** `/calls/{id}/`

Get detailed call information including recordings.

**Response:**
```json
{
  "id": 1,
  "call_sid": "CA1234567890abcdef",
  "parent_call_sid": null,
  "direction": "OUTBOUND",
  "status": "COMPLETED",
  "from_number": "+17656456867",
  "to_number": "+1555123456",
  "agent": 1,
  "agent_name": "John Doe",
  "lead": 5,
  "lead_name": "Alice Johnson",
  "contact": null,
  "contact_name": null,
  "duration": 180,
  "duration_formatted": "03:00",
  "start_time": "2024-01-15T10:00:00Z",
  "end_time": "2024-01-15T10:03:00Z",
  "call_notes": "Discussed product features",
  "tags": "demo,interested",
  "recordings": [
    {
      "id": 1,
      "recording_sid": "RE1234567890abcdef",
      "recording_url": "https://api.twilio.com/...",
      "duration": 180,
      "duration_formatted": "03:00",
      "file_size": 1048576,
      "file_size_formatted": "1.00 MB",
      "status": "COMPLETED",
      "is_transcribed": false,
      "created_at": "2024-01-15T10:03:05Z"
    }
  ],
  "created_at": "2024-01-15T09:59:55Z",
  "updated_at": "2024-01-15T10:03:05Z"
}
```

### Initiate Call

**POST** `/calls/initiate/`

Initiate an outbound call.

**Request:**
```json
{
  "to_number": "+1555123456",
  "from_number": "+17656456867",
  "lead_id": 5,
  "record": true
}
```

**Response:** 201 Created
```json
{
  "id": 1,
  "call_sid": "CA1234567890abcdef",
  "direction": "OUTBOUND",
  "status": "INITIATED",
  "from_number": "+17656456867",
  "to_number": "+1555123456",
  "agent": 1,
  "agent_name": "John Doe",
  "lead": 5,
  "lead_name": "Alice Johnson",
  "duration": 0,
  "created_at": "2024-01-15T09:59:55Z"
}
```

### Update Call

**PATCH** `/calls/{id}/`

Update call information (notes, tags, associations).

**Request:**
```json
{
  "call_notes": "Customer interested in enterprise plan",
  "tags": "enterprise,follow-up",
  "contact": 3
}
```

### Get Call Recordings

**GET** `/calls/{id}/recordings/`

Get all recordings for a specific call.

**Response:**
```json
[
  {
    "id": 1,
    "recording_sid": "RE1234567890abcdef",
    "recording_url": "https://api.twilio.com/...",
    "duration": 180,
    "duration_formatted": "03:00",
    "status": "COMPLETED",
    "created_at": "2024-01-15T10:03:05Z"
  }
]
```

---

## Recording Management

### List Recordings

**GET** `/recordings/`

Get list of call recordings.

**Permissions:** Agents see recordings from their calls, Managers see all

**Query Parameters:**
- `status` - Filter by status (PROCESSING, COMPLETED, FAILED)
- `is_transcribed` - Filter by transcription status (true/false)
- `search` - Search by recording_sid, call_sid
- `ordering` - Sort by field

**Response:**
```json
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "recording_sid": "RE1234567890abcdef",
      "recording_url": "https://api.twilio.com/...",
      "duration": 180,
      "duration_formatted": "03:00",
      "file_size": 1048576,
      "file_size_formatted": "1.00 MB",
      "status": "COMPLETED",
      "local_file": null,
      "is_transcribed": false,
      "transcription": null,
      "created_at": "2024-01-15T10:03:05Z"
    }
  ]
}
```

### Get Recording

**GET** `/recordings/{id}/`

Get recording details.

### Download Recording

**GET** `/recordings/{id}/download/`

Download recording audio file.

**Response:** Audio file (audio/mpeg)
- Content-Disposition: attachment; filename="recording_RE....mp3"

---

## Statistics & Reporting

### Call Statistics

**GET** `/statistics/calls/`

Get call statistics for current user (or all if manager).

**Query Parameters:**
- `start_date` - Start date filter (YYYY-MM-DD)
- `end_date` - End date filter (YYYY-MM-DD)

**Response:**
```json
{
  "total_calls": 150,
  "incoming_calls": 60,
  "outgoing_calls": 90,
  "completed_calls": 120,
  "missed_calls": 15,
  "total_duration": 18000,
  "average_duration": 120.0,
  "total_recordings": 100
}
```

### Agent Statistics

**GET** `/statistics/agents/`

Get per-agent call statistics.

**Permissions:** Manager/Admin only

**Query Parameters:**
- `start_date` - Start date filter (YYYY-MM-DD)
- `end_date` - End date filter (YYYY-MM-DD)

**Response:**
```json
[
  {
    "agent_id": 1,
    "agent_name": "John Doe",
    "total_calls": 75,
    "incoming_calls": 30,
    "outgoing_calls": 45,
    "total_duration": 9000,
    "average_duration": 120.0
  },
  {
    "agent_id": 2,
    "agent_name": "Jane Smith",
    "total_calls": 75,
    "incoming_calls": 30,
    "outgoing_calls": 45,
    "total_duration": 9000,
    "average_duration": 120.0
  }
]
```

---

## Twilio Integration

### Generate Access Token

**POST** `/twilio/token/`

Generate Twilio access token for WebRTC client.

**Request:** Empty body

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "identity": "user_1"
}
```

**Usage:**
```javascript
// Web (JavaScript)
const device = new Twilio.Device(token);

// Android (Java)
Device device = new Device(token, listener);
```

---

## Error Handling

### Error Response Format

All errors follow this format:

```json
{
  "error": "Error message describing what went wrong"
}
```

Or for validation errors:

```json
{
  "field_name": ["Error message for this field"],
  "another_field": ["Error message"]
}
```

### HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Successful deletion
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Common Errors

**401 Unauthorized**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden**
```json
{
  "error": "You do not have permission to perform this action."
}
```

**404 Not Found**
```json
{
  "detail": "Not found."
}
```

**400 Validation Error**
```json
{
  "to_number": ["This field is required."],
  "password": ["Passwords do not match"]
}
```

---

## Rate Limiting (Recommended for Production)

Consider implementing rate limiting:
- Authentication endpoints: 5 requests per minute
- API endpoints: 100 requests per minute per user
- Webhook endpoints: 1000 requests per minute

---

## Pagination

All list endpoints support pagination with the following parameters:

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20, max: 100)

**Response:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/calls/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## Filtering & Search

Most list endpoints support:
- **Filtering**: `?field=value` (e.g., `?status=COMPLETED`)
- **Search**: `?search=keyword` (searches across multiple fields)
- **Ordering**: `?ordering=field` or `?ordering=-field` (descending)

**Examples:**
```
GET /api/calls/?status=COMPLETED&ordering=-created_at
GET /api/leads/?search=Tech&status=NEW
GET /api/users/?role=AGENT&is_available=true
```

---

## Webhooks

Twilio sends webhooks to your server. Configure these URLs in Twilio Console:

### Webhook URLs

- **Voice URL**: `https://your-domain.com/webhooks/voice/`
- **Status Callback**: `https://your-domain.com/webhooks/call-status/`
- **Recording Callback**: `https://your-domain.com/webhooks/recording-status/`
- **Incoming Call**: `https://your-domain.com/webhooks/incoming-call/`

### Webhook Security

All webhooks validate Twilio signatures for security. Ensure your server:
1. Uses HTTPS
2. Has the correct `TWILIO_AUTH_TOKEN` configured
3. Provides the full public URL for webhook validation

---

## API Documentation (Interactive)

Access interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`

---

## Sample API Workflow

### 1. Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "agent1", "password": "password123"}'
```

### 2. Get Twilio Token
```bash
curl -X POST http://localhost:8000/api/twilio/token/ \
  -H "Authorization: Bearer <access_token>"
```

### 3. Initiate Call
```bash
curl -X POST http://localhost:8000/api/calls/initiate/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "to_number": "+1555123456",
    "lead_id": 5,
    "record": true
  }'
```

### 4. Get Call History
```bash
curl -X GET "http://localhost:8000/api/calls/?ordering=-created_at" \
  -H "Authorization: Bearer <access_token>"
```

### 5. Get Statistics
```bash
curl -X GET "http://localhost:8000/api/statistics/calls/?start_date=2024-01-01" \
  -H "Authorization: Bearer <access_token>"
```

---

For more details and updates, visit the interactive API documentation.
