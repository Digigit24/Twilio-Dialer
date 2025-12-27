"""
Custom authentication views with cookie support.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Custom login view that sets JWT tokens in httpOnly cookies
    and also returns them in response body for flexibility.
    """
    def post(self, request, *args, **kwargs):
        # Call parent to get tokens
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            # Set cookies
            # Access token cookie (httpOnly for security)
            response.set_cookie(
                key='access_token',
                value=access_token,
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                httponly=True,
                secure=not settings.DEBUG,  # HTTPS only in production
                samesite='Lax'
            )

            # Refresh token cookie
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax'
            )

            # Log successful login
            username = request.data.get('username')
            logger.info(f"User {username} logged in successfully with cookies set")

        return response


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Custom login endpoint with detailed error messages.
    Sets cookies and returns tokens in response.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Authenticate user
    user = authenticate(username=username, password=password)

    if user is None:
        logger.warning(f"Failed login attempt for username: {username}")
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_active:
        return Response(
            {'error': 'User account is disabled'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Generate tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # Create response
    response = Response({
        'access': access_token,
        'refresh': refresh_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    }, status=status.HTTP_200_OK)

    # Set cookies
    response.set_cookie(
        key='access_token',
        value=access_token,
        max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax'
    )

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax'
    )

    logger.info(f"User {username} logged in successfully")
    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint that clears cookies.
    """
    response = Response({'message': 'Logged out successfully'})

    # Clear cookies
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    logger.info(f"User {request.user.username} logged out")
    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    """
    Refresh access token using refresh token from cookie or body.
    """
    # Try to get refresh token from cookie first, then from body
    refresh_token = request.COOKIES.get('refresh_token') or request.data.get('refresh')

    if not refresh_token:
        return Response(
            {'error': 'Refresh token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)

        response = Response({
            'access': access_token
        })

        # Update access token cookie
        response.set_cookie(
            key='access_token',
            value=access_token,
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax'
        )

        return response

    except Exception as e:
        logger.error(f"Token refresh failed: {str(e)}")
        return Response(
            {'error': 'Invalid refresh token'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token_view(request):
    """
    Verify that the current token is valid and return user info.
    """
    user = request.user
    return Response({
        'valid': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_available': user.is_available,
        }
    })
