import base
import exceptions
import xml_render

class processor(base.processor):
    """
    SalesForce.com-specific SAML 2.0 AuthnRequest to Response Handler Processor.
    """
    def _validate_request(self):
        """
        Validates the _saml_request. Sub-classes should override this and
        throw an Exception if the validation does not succeed.
        """
        if not '.salesforce.com' in self._request_params['ACS_URL']:
            raise exceptions.CannotHandleAssertion('AssertionConsumerService is not a SalesForce URL.')

    def _determine_audience(self):
        self._audience = 'https://saml.salesforce.com'

    def _format_assertion(self):
        self._assertion_xml = xml_render.get_assertion_salesforce_xml(self._assertion_params, signed=True)