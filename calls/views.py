"""
Webhook handlers for Twilio callbacks.
"""
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Call, CallRecording
from .services import twilio_service

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def call_status_webhook(request):
    """
    Handle Twilio call status callbacks.
    Updates call status in database.
    """
    try:
        # Extract call details from webhook
        call_sid = request.POST.get('CallSid')
        call_status = request.POST.get('CallStatus')
        duration = request.POST.get('CallDuration', 0)

        logger.info(f"Call status webhook: {call_sid} - {call_status}")

        # Update or create call record
        call, created = Call.objects.get_or_create(
            call_sid=call_sid,
            defaults={
                'direction': Call.Direction.OUTBOUND,
                'from_number': request.POST.get('From', ''),
                'to_number': request.POST.get('To', ''),
                'status': Call.Status.INITIATED,
            }
        )

        # Map Twilio status to our status
        status_mapping = {
            'queued': Call.Status.INITIATED,
            'initiated': Call.Status.INITIATED,
            'ringing': Call.Status.RINGING,
            'in-progress': Call.Status.IN_PROGRESS,
            'completed': Call.Status.COMPLETED,
            'busy': Call.Status.BUSY,
            'failed': Call.Status.FAILED,
            'no-answer': Call.Status.NO_ANSWER,
            'canceled': Call.Status.CANCELED,
        }

        call.status = status_mapping.get(call_status.lower(), Call.Status.INITIATED)

        # Update timestamps
        if call_status.lower() == 'in-progress' and not call.start_time:
            call.start_time = timezone.now()

        if call_status.lower() in ['completed', 'failed', 'busy', 'no-answer', 'canceled']:
            if not call.end_time:
                call.end_time = timezone.now()
            if duration:
                call.duration = int(duration)

        call.save()

        logger.info(f"Call {call_sid} updated to status: {call.status}")

        return HttpResponse(status=200)

    except Exception as e:
        logger.error(f"Error in call status webhook: {str(e)}")
        return HttpResponse(status=500)


@csrf_exempt
@require_POST
def recording_status_webhook(request):
    """
    Handle Twilio recording status callbacks.
    Creates or updates call recording record.
    """
    try:
        # Extract recording details from webhook
        recording_sid = request.POST.get('RecordingSid')
        call_sid = request.POST.get('CallSid')
        recording_url = request.POST.get('RecordingUrl')
        duration = request.POST.get('RecordingDuration', 0)
        recording_status = request.POST.get('RecordingStatus')

        logger.info(f"Recording webhook: {recording_sid} for call {call_sid}")

        # Get the associated call
        try:
            call = Call.objects.get(call_sid=call_sid)
        except Call.DoesNotExist:
            logger.warning(f"Call not found for recording: {call_sid}")
            # Create call record if it doesn't exist
            call = Call.objects.create(
                call_sid=call_sid,
                direction=Call.Direction.OUTBOUND,
                from_number=request.POST.get('From', ''),
                to_number=request.POST.get('To', ''),
                status=Call.Status.COMPLETED,
            )

        # Map Twilio recording status to our status
        status_mapping = {
            'processing': CallRecording.Status.PROCESSING,
            'completed': CallRecording.Status.COMPLETED,
            'absent': CallRecording.Status.FAILED,
        }

        # Create or update recording
        recording, created = CallRecording.objects.update_or_create(
            recording_sid=recording_sid,
            defaults={
                'call': call,
                'recording_url': recording_url,
                'duration': int(duration) if duration else 0,
                'status': status_mapping.get(recording_status.lower(), CallRecording.Status.PROCESSING),
            }
        )

        logger.info(f"Recording {recording_sid} {'created' if created else 'updated'}")

        return HttpResponse(status=200)

    except Exception as e:
        logger.error(f"Error in recording webhook: {str(e)}")
        return HttpResponse(status=500)


@csrf_exempt
@require_POST
def incoming_call_webhook(request):
    """
    Handle incoming call webhook.
    Route call to available agent.
    """
    try:
        from_number = request.POST.get('From')
        to_number = request.POST.get('To')
        call_sid = request.POST.get('CallSid')

        logger.info(f"Incoming call: {call_sid} from {from_number}")

        # Create call record
        call = Call.objects.create(
            call_sid=call_sid,
            direction=Call.Direction.INBOUND,
            from_number=from_number,
            to_number=to_number,
            status=Call.Status.RINGING,
        )

        # Find available agent (you can implement your own logic here)
        from accounts.models import User
        available_agent = User.objects.filter(
            role=User.Role.AGENT,
            is_available=True,
            is_active=True
        ).first()

        if available_agent and available_agent.twilio_client_identity:
            # Route to agent's Twilio Client
            twiml = twilio_service.generate_twiml_client(available_agent.twilio_client_identity)
            call.agent = available_agent
            call.save()
        else:
            # No available agent, play message
            from twilio.twiml.voice_response import VoiceResponse
            response = VoiceResponse()
            response.say("Sorry, all agents are currently busy. Please try again later.")
            response.hangup()
            twiml = str(response)

        return HttpResponse(twiml, content_type='text/xml')

    except Exception as e:
        logger.error(f"Error in incoming call webhook: {str(e)}")
        from twilio.twiml.voice_response import VoiceResponse
        response = VoiceResponse()
        response.say("An error occurred. Please try again later.")
        response.hangup()
        return HttpResponse(str(response), content_type='text/xml')


@csrf_exempt
@require_POST
def voice_webhook(request):
    """
    Handle TwiML App voice webhook for outbound calls.
    """
    try:
        to_number = request.POST.get('To', '')
        from_number = request.POST.get('From', '')

        logger.info(f"Voice webhook: Dialing {to_number}")

        # Generate TwiML to dial the number
        twiml = twilio_service.generate_twiml_dial(to_number, caller_id=from_number)

        return HttpResponse(twiml, content_type='text/xml')

    except Exception as e:
        logger.error(f"Error in voice webhook: {str(e)}")
        from twilio.twiml.voice_response import VoiceResponse
        response = VoiceResponse()
        response.say("Unable to connect your call. Please try again.")
        response.hangup()
        return HttpResponse(str(response), content_type='text/xml')
