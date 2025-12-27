"""
Twilio service layer for call management.
"""
import logging
from typing import Optional, Dict, Any
from django.conf import settings
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial
from .models import Call, CallRecording

logger = logging.getLogger(__name__)


class TwilioService:
    """
    Service class for Twilio operations.
    """

    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.phone_number = settings.TWILIO_PHONE_NUMBER
        self.app_sid = settings.TWILIO_APP_SID
        # API Keys for JWT token generation (optional, falls back to Account SID/Token)
        self.api_key_sid = getattr(settings, 'TWILIO_API_KEY_SID', None)
        self.api_key_secret = getattr(settings, 'TWILIO_API_KEY_SECRET', None)
        self._client = None

    @property
    def client(self):
        """Lazy initialization of Twilio client."""
        if self._client is None:
            if not self.account_sid or not self.auth_token:
                raise ValueError(
                    "Twilio credentials not configured. "
                    "Please set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in .env file"
                )
            self._client = Client(self.account_sid, self.auth_token)
        return self._client

    def generate_access_token(self, identity: str, ttl: int = 3600) -> str:
        """
        Generate Twilio access token for WebRTC client.

        Args:
            identity: Unique identifier for the client (usually user ID or username)
            ttl: Token time-to-live in seconds (default: 1 hour)

        Returns:
            JWT access token string
        """
        try:
            # Check if we have API Keys configured (RECOMMENDED)
            api_key_sid = getattr(settings, 'TWILIO_API_KEY_SID', None)
            api_key_secret = getattr(settings, 'TWILIO_API_KEY_SECRET', None)

            # Use API Keys if available and not empty, otherwise fall back to Account SID/Token
            if api_key_sid and api_key_secret and api_key_sid.strip() and api_key_secret.strip():
                # Production: Use API Keys (RECOMMENDED)
                signing_key_sid = api_key_sid
                signing_key_secret = api_key_secret
                logger.info(f"✓ Using API Key for token generation: {signing_key_sid[:8]}...")
            else:
                # Development: Use Account SID and Auth Token
                signing_key_sid = self.account_sid
                signing_key_secret = self.auth_token
                logger.warning("⚠ Using Account SID/Token for token generation (not recommended for production)")

            # Validate required settings
            if not self.account_sid or not signing_key_sid or not signing_key_secret:
                raise ValueError("Missing required Twilio credentials")

            if not self.app_sid:
                raise ValueError("TWILIO_APP_SID is required for WebRTC calling")

            # Create access token
            token = AccessToken(
                self.account_sid,      # Twilio Account SID
                signing_key_sid,       # API Key SID (or Account SID for dev)
                signing_key_secret,    # API Key Secret (or Auth Token for dev)
                identity=identity,
                ttl=ttl
            )

            # Create Voice grant
            voice_grant = VoiceGrant(
                outgoing_application_sid=self.app_sid,
                incoming_allow=True
            )

            # Add grant to token
            token.add_grant(voice_grant)

            # Generate and return JWT
            jwt_token = token.to_jwt()

            logger.info(f"✓ Generated access token for identity: {identity} (TTL: {ttl}s)")

            # Decode if bytes
            if isinstance(jwt_token, bytes):
                return jwt_token.decode('utf-8')
            return str(jwt_token)

        except Exception as e:
            logger.error(f"✗ Error generating access token: {str(e)}", exc_info=True)
            raise

    def make_call(
        self,
        to_number: str,
        from_number: Optional[str] = None,
        callback_url: Optional[str] = None,
        status_callback_url: Optional[str] = None,
        record: bool = True
    ) -> Dict[str, Any]:
        """
        Initiate an outbound call.

        Args:
            to_number: Destination phone number
            from_number: Caller ID (defaults to configured Twilio number)
            callback_url: TwiML URL for call instructions
            status_callback_url: Webhook URL for call status updates
            record: Whether to record the call

        Returns:
            Dictionary with call details
        """
        try:
            from_number = from_number or self.phone_number

            call = self.client.calls.create(
                to=to_number,
                from_=from_number,
                url=callback_url,
                status_callback=status_callback_url,
                status_callback_event=['initiated', 'ringing', 'answered', 'completed'],
                status_callback_method='POST',
                record=record
            )

            logger.info(f"Call initiated: {call.sid} from {from_number} to {to_number}")

            return {
                'call_sid': call.sid,
                'status': call.status,
                'from': from_number,
                'to': to_number,
                'direction': 'outbound-api'
            }

        except Exception as e:
            logger.error(f"Error making call: {str(e)}")
            raise

    def get_call_details(self, call_sid: str) -> Dict[str, Any]:
        """
        Fetch call details from Twilio.

        Args:
            call_sid: Twilio Call SID

        Returns:
            Dictionary with call details
        """
        try:
            call = self.client.calls(call_sid).fetch()

            return {
                'call_sid': call.sid,
                'status': call.status,
                'direction': call.direction,
                'from': call.from_,
                'to': call.to,
                'duration': call.duration,
                'start_time': call.start_time,
                'end_time': call.end_time,
                'price': call.price,
                'price_unit': call.price_unit
            }

        except Exception as e:
            logger.error(f"Error fetching call details: {str(e)}")
            raise

    def get_call_recordings(self, call_sid: str) -> list:
        """
        Fetch recordings for a specific call.

        Args:
            call_sid: Twilio Call SID

        Returns:
            List of recording dictionaries
        """
        try:
            recordings = self.client.recordings.list(call_sid=call_sid)

            return [{
                'recording_sid': rec.sid,
                'duration': rec.duration,
                'status': rec.status,
                'date_created': rec.date_created,
                'uri': rec.uri,
                'media_url': f"https://api.twilio.com{rec.uri.replace('.json', '.mp3')}"
            } for rec in recordings]

        except Exception as e:
            logger.error(f"Error fetching recordings: {str(e)}")
            raise

    def download_recording(self, recording_sid: str) -> bytes:
        """
        Download recording audio file.

        Args:
            recording_sid: Twilio Recording SID

        Returns:
            Recording audio bytes
        """
        try:
            recording = self.client.recordings(recording_sid).fetch()
            media_url = f"https://api.twilio.com{recording.uri.replace('.json', '.mp3')}"

            # Download the recording
            import requests
            response = requests.get(
                media_url,
                auth=(self.account_sid, self.auth_token),
                stream=True
            )
            response.raise_for_status()

            logger.info(f"Downloaded recording: {recording_sid}")
            return response.content

        except Exception as e:
            logger.error(f"Error downloading recording: {str(e)}")
            raise

    def generate_twiml_dial(self, to_number: str, caller_id: Optional[str] = None) -> str:
        """
        Generate TwiML for dialing a number.

        Args:
            to_number: Number to dial
            caller_id: Caller ID to use

        Returns:
            TwiML XML string
        """
        response = VoiceResponse()
        dial = Dial(caller_id=caller_id or self.phone_number, record='record-from-answer')
        dial.number(to_number)
        response.append(dial)

        return str(response)

    def generate_twiml_client(self, client_identity: str) -> str:
        """
        Generate TwiML for connecting to a Twilio Client.

        Args:
            client_identity: Twilio Client identity to connect to

        Returns:
            TwiML XML string
        """
        response = VoiceResponse()
        dial = Dial(record='record-from-answer')
        dial.client(client_identity)
        response.append(dial)

        return str(response)

    def validate_webhook_signature(self, url: str, params: dict, signature: str) -> bool:
        """
        Validate Twilio webhook signature.

        Args:
            url: Full URL of the webhook
            params: POST parameters
            signature: X-Twilio-Signature header value

        Returns:
            True if signature is valid, False otherwise
        """
        from twilio.request_validator import RequestValidator

        validator = RequestValidator(self.auth_token)
        return validator.validate(url, params, signature)


# Singleton instance
twilio_service = TwilioService()
