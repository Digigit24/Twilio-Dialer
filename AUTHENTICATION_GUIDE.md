# Authentication System Guide

## Overview

The Twilio CRM system now uses a **multi-layered authentication system** with cookies as the primary method:

1. **Primary**: Cookie-based JWT authentication (HttpOnly, secure)
2. **Fallback 1**: Bearer token in Authorization header
3. **Fallback 2**: DRF Token authentication

## Cookie-Based Authentication

### How It Works

1. **Login**: User submits credentials to `/api/auth/login/`
2. **Response**: Server sets two HttpOnly cookies:
   - `access_token`: Valid for 8 hours
   - `refresh_token`: Valid for 7 days
3. **Subsequent Requests**: Browser automatically sends cookies
4. **No manual token management required!**

### Benefits

- ✅ **Secure**: HttpOnly cookies prevent XSS attacks
- ✅ **Automatic**: Browser handles cookie storage and sending
- ✅ **CSRF Protected**: Uses Django's CSRF token system
- ✅ **Seamless UX**: No manual token management in frontend

## API Endpoints

### Authentication Endpoints

#### Login
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "username": "agent1",
  "password": "test123"
}

Response:
{
  "access": "eyJ...",
  "refresh": "eyJ...",
  "user": {
    "id": 2,
    "username": "agent1",
    "email": "agent1@example.com",
    "role": "AGENT",
    "first_name": "John",
    "last_name": "Doe"
  }
}

+ Sets cookies: access_token, refresh_token
```

#### Logout
```bash
POST /api/auth/logout/
X-CSRFToken: <token>

Response:
{
  "message": "Logged out successfully"
}

+ Clears cookies
```

#### Refresh Token
```bash
POST /api/auth/refresh/
X-CSRFToken: <token>

Response:
{
  "access": "eyJ..."
}

+ Updates access_token cookie
```

#### Verify Token
```bash
GET /api/auth/verify/

Response:
{
  "valid": true,
  "user": {
    "id": 2,
    "username": "agent1",
    "email": "agent1@example.com",
    "role": "AGENT",
    "first_name": "John",
    "last_name": "Doe",
    "is_available": true
  }
}
```

## JavaScript Usage

### Using Cookies (Recommended)

```javascript
// Helper to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Login
const csrftoken = getCookie('csrftoken');

const response = await fetch('/api/auth/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    },
    credentials: 'include',  // Important!
    body: JSON.stringify({ username, password })
});

// All subsequent requests - cookies sent automatically
const data = await fetch('/api/calls/', {
    credentials: 'include',
    headers: { 'X-CSRFToken': csrftoken }
});
```

### Using Bearer Token (Fallback)

```javascript
// Login
const response = await fetch('/api/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
});

const { access } = await response.json();
localStorage.setItem('token', access);

// Subsequent requests
const data = await fetch('/api/calls/', {
    headers: {
        'Authorization': `Bearer ${access}`
    }
});
```

## Testing Authentication

### Test Accounts

```
Agent Account:
  Username: agent1
  Password: test123
  Role: AGENT

Manager Account:
  Username: manager1
  Password: test123
  Role: MANAGER

Admin Account:
  Username: admin
  Password: admin123
  Role: ADMIN
```

### Test with cURL

```bash
# Login and save cookies
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "agent1", "password": "test123"}' \
  -c cookies.txt

# Use cookies for authenticated request
curl http://localhost:8000/api/auth/verify/ \
  -b cookies.txt

# Logout
curl -X POST http://localhost:8000/api/auth/logout/ \
  -b cookies.txt
```

### Test with Browser

1. Open: http://localhost:8000/
2. Login with agent1/test123
3. Open DevTools → Application → Cookies
4. You should see: `access_token` and `refresh_token`

## Security Features

### Cookie Settings

- **HttpOnly**: Prevents JavaScript access (XSS protection)
- **SameSite=Lax**: CSRF protection
- **Secure**: HTTPS only in production
- **Max-Age**: Automatic expiration

### CSRF Protection

- All state-changing requests require CSRF token
- Token automatically set by Django
- JavaScript reads from `csrftoken` cookie

### Token Expiration

- Access token: 8 hours
- Refresh token: 7 days
- Automatic rotation on refresh

## Troubleshooting

### Issue: "Invalid token" or "Authentication credentials were not provided"

**Solutions:**
1. Check cookies are enabled in browser
2. Verify `credentials: 'include'` in fetch requests
3. Check CSRF token is included in POST requests
4. Try logging out and logging in again

### Issue: CORS errors

**Solutions:**
1. Verify server is running on http://localhost:8000
2. Check CORS settings allow your origin
3. Ensure `credentials: 'include'` is set

### Issue: Cookies not being set

**Solutions:**
1. Check browser console for errors
2. Verify server response includes Set-Cookie headers
3. Clear browser cookies and try again

## Migration from Old System

If you were using the old system with manual token management:

### Old Way (Manual Bearer Token)
```javascript
const { access } = await loginResponse.json();
localStorage.setItem('accessToken', access);

// Every request needs token
fetch('/api/calls/', {
    headers: { 'Authorization': `Bearer ${access}` }
});
```

### New Way (Automatic Cookies)
```javascript
await fetch('/api/auth/login/', {
    credentials: 'include',
    // ...
});

// Cookies sent automatically!
fetch('/api/calls/', {
    credentials: 'include'
});
```

## Best Practices

1. **Always use `credentials: 'include'`** in fetch requests
2. **Include CSRF token** in POST/PUT/DELETE requests
3. **Check token validity** before making critical operations
4. **Handle 401 errors** by redirecting to login
5. **Use refresh token** to get new access token when expired

## Additional Resources

- Web Client: http://localhost:8000/
- API Documentation: http://localhost:8000/api/docs/
- Admin Panel: http://localhost:8000/admin/
