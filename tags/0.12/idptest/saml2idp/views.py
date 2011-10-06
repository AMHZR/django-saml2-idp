# Python imports:
import base64
import logging
import time
import uuid
# Django/other library imports:
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_view_exempt, csrf_response_exempt
# saml2idp app imports:
import saml2idp_settings
import exceptions
import registry

@csrf_view_exempt
def login_begin(request, *args, **kwargs):
    """
    Receives a SAML 2.0 AuthnRequest from a Service Point and
    stores it in the session prior to enforcing login.
    """
    if request.method == 'POST':
        source = request.POST
    else:
        source = request.GET
    # Store these values now, because Django's login cycle won't preserve them.
    request.session['SAMLRequest'] = source['SAMLRequest']
    request.session['RelayState'] = source['RelayState']
    return redirect('login_process')

@login_required
@csrf_response_exempt
def login_process(request):
    """
    Processor-based login continuation.
    Presents a SAML 2.0 Assertion for POSTing back to the Service Point.
    """
    reg = registry.ProcessorRegistry()
    logging.debug("Request: %s" % request)
    proc = reg.find_processor(request)

    # Just in case downstream code wants to filter by some user criteria:
    try:
        tv = proc.generate_response()
    except exceptions.UserNotAuthorized:
        return render_to_response('saml2idp/invalid_user.html')

    return render_to_response('saml2idp/login.html', tv)

@csrf_view_exempt
def logout(request):
    """
    Receives a SAML 2.0 LogoutRequest from a Service Point,
    logs out the user and returns a standard logged-out page.
    """
    auth.logout(request)
    tv = {}
    return render_to_response('saml2idp/logged_out.html', tv)