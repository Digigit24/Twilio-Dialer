"""
Serializers for API endpoints.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from calls.models import Call, CallRecording, Lead, Contact

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone_number', 'extension', 'is_available',
            'twilio_client_identity', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users."""

    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password', 'password_confirm',
            'role', 'phone_number', 'extension', 'is_available'
        ]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LeadSerializer(serializers.ModelSerializer):
    """Serializer for Lead model."""

    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = Lead
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number',
            'company', 'status', 'assigned_to', 'assigned_to_name', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model."""

    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = Contact
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number',
            'company', 'position', 'assigned_to', 'assigned_to_name', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CallRecordingSerializer(serializers.ModelSerializer):
    """Serializer for CallRecording model."""

    duration_formatted = serializers.CharField(source='get_duration_formatted', read_only=True)
    file_size_formatted = serializers.CharField(source='get_file_size_formatted', read_only=True)

    class Meta:
        model = CallRecording
        fields = [
            'id', 'recording_sid', 'recording_url', 'duration', 'duration_formatted',
            'file_size', 'file_size_formatted', 'status', 'local_file',
            'is_transcribed', 'transcription', 'created_at'
        ]
        read_only_fields = ['id', 'recording_sid', 'created_at']


class CallSerializer(serializers.ModelSerializer):
    """Serializer for Call model."""

    agent_name = serializers.CharField(source='agent.get_full_name', read_only=True)
    lead_name = serializers.CharField(source='lead.get_full_name', read_only=True)
    contact_name = serializers.CharField(source='contact.get_full_name', read_only=True)
    duration_formatted = serializers.CharField(source='get_duration_formatted', read_only=True)
    recordings = CallRecordingSerializer(many=True, read_only=True)

    class Meta:
        model = Call
        fields = [
            'id', 'call_sid', 'parent_call_sid', 'direction', 'status',
            'from_number', 'to_number', 'agent', 'agent_name',
            'lead', 'lead_name', 'contact', 'contact_name',
            'duration', 'duration_formatted', 'start_time', 'end_time',
            'call_notes', 'tags', 'recordings', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'call_sid', 'created_at', 'updated_at']


class CallListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for call list view."""

    agent_name = serializers.CharField(source='agent.get_full_name', read_only=True)
    duration_formatted = serializers.CharField(source='get_duration_formatted', read_only=True)
    has_recording = serializers.SerializerMethodField()

    class Meta:
        model = Call
        fields = [
            'id', 'call_sid', 'direction', 'status', 'from_number', 'to_number',
            'agent_name', 'duration', 'duration_formatted', 'start_time',
            'has_recording', 'created_at'
        ]

    def get_has_recording(self, obj):
        return obj.recordings.exists()


class InitiateCallSerializer(serializers.Serializer):
    """Serializer for initiating a call."""

    to_number = serializers.CharField(max_length=20, required=True)
    from_number = serializers.CharField(max_length=20, required=False)
    lead_id = serializers.IntegerField(required=False, allow_null=True)
    contact_id = serializers.IntegerField(required=False, allow_null=True)
    record = serializers.BooleanField(default=True)


class AccessTokenSerializer(serializers.Serializer):
    """Serializer for access token response."""

    token = serializers.CharField()
    identity = serializers.CharField()


class AgentStatusSerializer(serializers.Serializer):
    """Serializer for updating agent availability status."""

    is_available = serializers.BooleanField(required=True)


class CallStatsSerializer(serializers.Serializer):
    """Serializer for call statistics."""

    total_calls = serializers.IntegerField()
    incoming_calls = serializers.IntegerField()
    outgoing_calls = serializers.IntegerField()
    completed_calls = serializers.IntegerField()
    missed_calls = serializers.IntegerField()
    total_duration = serializers.IntegerField()
    average_duration = serializers.FloatField()
    total_recordings = serializers.IntegerField()


class AgentStatsSerializer(serializers.Serializer):
    """Serializer for agent-specific statistics."""

    agent_id = serializers.IntegerField()
    agent_name = serializers.CharField()
    total_calls = serializers.IntegerField()
    incoming_calls = serializers.IntegerField()
    outgoing_calls = serializers.IntegerField()
    total_duration = serializers.IntegerField()
    average_duration = serializers.FloatField()
