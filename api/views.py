"""
API views for call management and CRM operations.
"""
import logging
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend

from calls.models import Call, CallRecording, Lead, Contact
from calls.services import twilio_service
from .serializers import (
    UserSerializer, UserCreateSerializer, LeadSerializer, ContactSerializer,
    CallSerializer, CallListSerializer, CallRecordingSerializer,
    InitiateCallSerializer, AccessTokenSerializer, AgentStatusSerializer,
    CallStatsSerializer, AgentStatsSerializer
)
from .permissions import IsManager, IsOwnerOrManager, IsManagerOrReadOnly

User = get_user_model()
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User management.
    Managers can CRUD all users, Agents can only view their own profile.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_available', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['created_at', 'username']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_manager():
            return User.objects.all()
        return User.objects.filter(id=user.id)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def set_availability(self, request, pk=None):
        """Update agent availability status."""
        user = self.get_object()

        # Only allow user to update their own status or manager to update anyone's
        if user != request.user and not request.user.is_manager():
            return Response(
                {'error': 'You can only update your own availability status'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = AgentStatusSerializer(data=request.data)
        if serializer.is_valid():
            user.is_available = serializer.validated_data['is_available']
            user.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Lead management.
    Agents see only their assigned leads, Managers see all leads.
    """
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'assigned_to']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'company']
    ordering_fields = ['created_at', 'updated_at', 'last_name']

    def get_queryset(self):
        user = self.request.user
        if user.is_manager():
            return Lead.objects.all()
        return Lead.objects.filter(assigned_to=user)

    def perform_create(self, serializer):
        # If no assigned_to is specified, assign to current user
        if not serializer.validated_data.get('assigned_to'):
            serializer.save(assigned_to=self.request.user)
        else:
            serializer.save()


class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Contact management.
    Agents see only their assigned contacts, Managers see all contacts.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['assigned_to']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'company', 'position']
    ordering_fields = ['created_at', 'updated_at', 'last_name']

    def get_queryset(self):
        user = self.request.user
        if user.is_manager():
            return Contact.objects.all()
        return Contact.objects.filter(assigned_to=user)

    def perform_create(self, serializer):
        # If no assigned_to is specified, assign to current user
        if not serializer.validated_data.get('assigned_to'):
            serializer.save(assigned_to=self.request.user)
        else:
            serializer.save()


class CallViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Call management.
    Agents see only their calls, Managers see all calls.
    """
    queryset = Call.objects.select_related('agent', 'lead', 'contact').prefetch_related('recordings')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['direction', 'status', 'agent', 'lead', 'contact']
    search_fields = ['call_sid', 'from_number', 'to_number', 'call_notes']
    ordering_fields = ['created_at', 'start_time', 'duration']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return CallListSerializer
        return CallSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Call.objects.select_related('agent', 'lead', 'contact').prefetch_related('recordings')

        if user.is_manager():
            return queryset
        return queryset.filter(agent=user)

    @action(detail=False, methods=['post'])
    def initiate(self, request):
        """Initiate an outbound call."""
        serializer = InitiateCallSerializer(data=request.data)

        if serializer.is_valid():
            to_number = serializer.validated_data['to_number']
            from_number = serializer.validated_data.get('from_number', settings.TWILIO_PHONE_NUMBER)
            record = serializer.validated_data.get('record', True)
            lead_id = serializer.validated_data.get('lead_id')
            contact_id = serializer.validated_data.get('contact_id')

            try:
                # Build callback URLs
                base_url = request.build_absolute_uri('/')[:-1]
                status_callback_url = f"{base_url}/webhooks/call-status/"
                voice_url = f"{base_url}/webhooks/voice/"

                # Make the call via Twilio
                call_data = twilio_service.make_call(
                    to_number=to_number,
                    from_number=from_number,
                    callback_url=voice_url,
                    status_callback_url=status_callback_url,
                    record=record
                )

                # Create call record
                call = Call.objects.create(
                    call_sid=call_data['call_sid'],
                    direction=Call.Direction.OUTBOUND,
                    from_number=from_number,
                    to_number=to_number,
                    agent=request.user,
                    status=Call.Status.INITIATED
                )

                # Associate with lead or contact if provided
                if lead_id:
                    try:
                        lead = Lead.objects.get(id=lead_id)
                        call.lead = lead
                        call.save()
                    except Lead.DoesNotExist:
                        pass

                if contact_id:
                    try:
                        contact = Contact.objects.get(id=contact_id)
                        call.contact = contact
                        call.save()
                    except Contact.DoesNotExist:
                        pass

                logger.info(f"Call initiated: {call.call_sid} by user {request.user.username}")

                return Response(
                    CallSerializer(call).data,
                    status=status.HTTP_201_CREATED
                )

            except Exception as e:
                logger.error(f"Error initiating call: {str(e)}")
                return Response(
                    {'error': f'Failed to initiate call: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def recordings(self, request, pk=None):
        """Get recordings for a specific call."""
        call = self.get_object()
        recordings = call.recordings.all()
        serializer = CallRecordingSerializer(recordings, many=True)
        return Response(serializer.data)


class CallRecordingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Call Recording management.
    Agents see only recordings from their calls, Managers see all recordings.
    """
    queryset = CallRecording.objects.select_related('call', 'call__agent')
    serializer_class = CallRecordingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_transcribed']
    search_fields = ['recording_sid', 'call__call_sid']
    ordering_fields = ['created_at', 'duration']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        queryset = CallRecording.objects.select_related('call', 'call__agent')

        if user.is_manager():
            return queryset
        return queryset.filter(call__agent=user)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download recording file."""
        recording = self.get_object()

        try:
            # If we have a local file, serve it
            if recording.local_file:
                from django.http import FileResponse
                return FileResponse(recording.local_file.open('rb'))

            # Otherwise, download from Twilio
            audio_data = twilio_service.download_recording(recording.recording_sid)

            from django.http import HttpResponse
            response = HttpResponse(audio_data, content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="recording_{recording.recording_sid}.mp3"'
            return response

        except Exception as e:
            logger.error(f"Error downloading recording: {str(e)}")
            return Response(
                {'error': f'Failed to download recording: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_access_token(request):
    """
    Generate Twilio access token for WebRTC client.
    """
    try:
        user = request.user
        identity = user.twilio_client_identity or f"user_{user.id}"

        # Update user's Twilio identity if not set
        if not user.twilio_client_identity:
            user.twilio_client_identity = identity
            user.save()

        # Generate token
        token = twilio_service.generate_access_token(identity)

        logger.info(f"Access token generated for user: {user.username}")

        return Response({
            'token': token,
            'identity': identity
        })

    except Exception as e:
        logger.error(f"Error generating access token: {str(e)}")
        return Response(
            {'error': f'Failed to generate access token: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def call_statistics(request):
    """
    Get call statistics.
    Agents see their own stats, Managers see all stats.
    """
    user = request.user

    # Base queryset
    if user.is_manager():
        queryset = Call.objects.all()
    else:
        queryset = Call.objects.filter(agent=user)

    # Apply date filters if provided
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if start_date:
        queryset = queryset.filter(created_at__gte=start_date)
    if end_date:
        queryset = queryset.filter(created_at__lte=end_date)

    # Calculate statistics
    total_calls = queryset.count()
    incoming_calls = queryset.filter(direction=Call.Direction.INBOUND).count()
    outgoing_calls = queryset.filter(direction=Call.Direction.OUTBOUND).count()
    completed_calls = queryset.filter(status=Call.Status.COMPLETED).count()
    missed_calls = queryset.filter(status__in=[Call.Status.NO_ANSWER, Call.Status.BUSY]).count()

    duration_stats = queryset.aggregate(
        total_duration=Sum('duration'),
        average_duration=Avg('duration')
    )

    total_recordings = CallRecording.objects.filter(
        call__in=queryset,
        status=CallRecording.Status.COMPLETED
    ).count()

    stats = {
        'total_calls': total_calls,
        'incoming_calls': incoming_calls,
        'outgoing_calls': outgoing_calls,
        'completed_calls': completed_calls,
        'missed_calls': missed_calls,
        'total_duration': duration_stats['total_duration'] or 0,
        'average_duration': duration_stats['average_duration'] or 0,
        'total_recordings': total_recordings
    }

    serializer = CallStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsManager])
def agent_statistics(request):
    """
    Get per-agent call statistics.
    Only accessible by Managers.
    """
    # Apply date filters if provided
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    queryset = Call.objects.all()

    if start_date:
        queryset = queryset.filter(created_at__gte=start_date)
    if end_date:
        queryset = queryset.filter(created_at__lte=end_date)

    # Group by agent
    agents = User.objects.filter(role=User.Role.AGENT)
    agent_stats = []

    for agent in agents:
        agent_calls = queryset.filter(agent=agent)
        total_calls = agent_calls.count()

        if total_calls > 0:
            incoming_calls = agent_calls.filter(direction=Call.Direction.INBOUND).count()
            outgoing_calls = agent_calls.filter(direction=Call.Direction.OUTBOUND).count()

            duration_stats = agent_calls.aggregate(
                total_duration=Sum('duration'),
                average_duration=Avg('duration')
            )

            agent_stats.append({
                'agent_id': agent.id,
                'agent_name': agent.get_full_name(),
                'total_calls': total_calls,
                'incoming_calls': incoming_calls,
                'outgoing_calls': outgoing_calls,
                'total_duration': duration_stats['total_duration'] or 0,
                'average_duration': duration_stats['average_duration'] or 0
            })

    serializer = AgentStatsSerializer(agent_stats, many=True)
    return Response(serializer.data)


# Template views for HTML pages
def agent_call_client(request):
    """Render the agent call client page."""
    return render(request, 'agent_call_client.html')


def test_config(request):
    """Render the configuration test page."""
    return render(request, 'test_config.html')
