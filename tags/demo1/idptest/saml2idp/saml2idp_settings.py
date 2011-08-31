from django.conf import settings

#TODO: Add settings so that signed stuff works in views.py
try:
    SAML2IDP_SIGNING = settings.SAML2IDP_SIGNING
except:
    SAML2IDP_SIGNING = False # by default

# If using relative paths, be careful!
try:
    SAML2IDP_PRIVATE_KEY_FILE = settings.SAML2IDP_PRIVATE_KEY_FILE
except:
    SAML2IDP_PRIVATE_KEY_FILE = 'keys/private-key.pem'

# If using relative paths, be careful!
try:
    SAML2IDP_CERTIFICATE_FILE = settings.SAML2IDP_CERTIFICATE_FILE
except:
    SAML2IDP_CERTIFICATE_FILE = 'keys/certificate.pem'