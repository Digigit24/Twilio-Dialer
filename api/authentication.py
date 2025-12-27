"""
Custom authentication classes supporting multiple auth methods.
Priority: 1. Cookies, 2. Bearer Token, 3. Authentication Token
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    """
    JWT authentication using cookies.
    Looks for JWT token in 'access_token' cookie first.
    """
    def authenticate(self, request):
        # Try to get token from cookie
        cookie_token = request.COOKIES.get('access_token')

        if cookie_token:
            # Validate the token from cookie
            validated_token = self.get_validated_token(cookie_token)
            return self.get_user(validated_token), validated_token

        # If no cookie, return None to let next auth class try
        return None


class BearerJWTAuthentication(JWTAuthentication):
    """
    Standard JWT authentication using Authorization header with Bearer token.
    """
    def authenticate(self, request):
        # Get token from Authorization header
        header = self.get_header(request)

        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token


class FallbackTokenAuthentication(TokenAuthentication):
    """
    Fallback to Django REST Framework's Token Authentication.
    """
    def authenticate(self, request):
        # Only try if there's an Authorization header with "Token"
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()

        if not auth or auth[0].lower() != 'token':
            return None

        return super().authenticate(request)
