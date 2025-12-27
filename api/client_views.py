"""
Views for serving client applications.
"""
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def agent_call_client(request):
    """
    Serve the agent call client HTML page.
    Ensures CSRF cookie is set for API requests.
    """
    return render(request, 'agent_call_client.html')
