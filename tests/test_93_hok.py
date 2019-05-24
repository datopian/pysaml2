#!/usr/bin/env python
# -*- coding: utf-8 -*-
from saml2.response import authn_response
from saml2.config import config_factory

from pathutils import dotname, full_path

HOLDER_OF_KEY_RESPONSE_FILE = full_path("saml_hok.xml") 


class TestHolderOfKeyResponse:
    def test_hok_response_is_parsed(self):
        """Verifies that response with 'holder-of-key' subject confirmations is parsed successfully."""
        conf = config_factory("idp", dotname("server_conf"))
        resp = authn_response(conf, "https://sp:443/.auth/saml/login", asynchop=False, allow_unsolicited=True)
        with open(HOLDER_OF_KEY_RESPONSE_FILE, 'r') as fp:
            authn_response_xml = fp.read()
        resp.loads(authn_response_xml, False)
        resp.do_not_verify = True

        resp.parse_assertion()

        assert resp.get_subject() is not None
        assert len(resp.assertion.subject.subject_confirmation) == 2
        actual_hok_certs = [sc.subject_confirmation_data.key_info[0].x509_data[0].x509_certificate.text.strip() 
                            for sc in resp.assertion.subject.subject_confirmation]
        assert actual_hok_certs == self._expected_hok_certs()

    def _expected_hok_certs(self):
        certs = ["""MIICITCCAYoCAQEwDQYJKoZIhvcNAQELBQAwWDELMAkGA1UEBhMCenoxCzAJBgNV
                    BAgMAnp6MQ0wCwYDVQQHDAR6enp6MQ4wDAYDVQQKDAVaenp6ejEOMAwGA1UECwwF
                    Wnp6enoxDTALBgNVBAMMBHRlc3QwIBcNMTkwNDEyMTk1MDM0WhgPMzAxODA4MTMx
                    OTUwMzRaMFgxCzAJBgNVBAYTAnp6MQswCQYDVQQIDAJ6ejENMAsGA1UEBwwEenp6
                    ejEOMAwGA1UECgwFWnp6enoxDjAMBgNVBAsMBVp6enp6MQ0wCwYDVQQDDAR0ZXN0
                    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDHcj80WU/XBsd9FlyQmfjPUdfm
                    edhCFDd6TEQmZNNqP/UG+VkGa+BXjRIHMfic/WxPTbGhCjv68ci0UDNomUXagFex
                    LGNpkwa7+CRVtoc/1xgq+ySE6M4nhcCutScoxNvWNn5eSQ66i3U0sTv91MgsXxqE
                    dTaiZg0BIufEc3dueQIDAQABMA0GCSqGSIb3DQEBCwUAA4GBAGUV5B+USHvaRa8k
                    gCNJSuNpo6ARlv0ekrk8bbdNRBiEUdCMyoGJFfuM9K0zybX6Vr25wai3nvaog294
                    Vx/jWjX2g5SDbjItH6VGy6C9GCGf1A07VxFRCfJn5tA9HuJjPKiE+g/BmrV5N4Ce
                    alzFxPHWYkNOzoRU8qI7OqUai1kL""",
                    """MIICITCCAYoCAQEwDQYJKoZIhvcNAQELBQAwWDELMAkGA1UEBhMCenoxCzAJBgNV
                    BAgMAnp6MQ0wCwYDVQQHDAR6enp6MQ4wDAYDVQQKDAVaenp6ejEOMAwGA1UECwwF
                    Wnp6enoxDTALBgNVBAMMBHRlc3QwIBcNMTkwNDEyMTk1MDM0WhgPMzAxODA4MTMx
                    OTUwMzRaMFgxCzAJBgNVBAYTAnp6MQswCQYDVQQIDAJ6ejENMAsGA1UEBwwEenp6
                    ejEOMAwGA1UECgwFWnp6enoxDjAMBgNVBAsMBVp6enp6MQ0wCwYDVQQDDAR0ZXN0
                    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDjW0kJM+4baWKtvO24ZsGXNvNK
                    KkwTMz7OW5Z6BRqhSOq2WA0c5NCpMk6rD8Z2OTFEolPojEjf8dVyd/Ds/hrjFKQv
                    8wQgbdXLN51YTIsgd6h+hBJO+vzhl0PT4aT7M0JKo5ALtS6qk4tsworW2BnwyvsG
                    SAinwfeWt4t/b1J3kwIDAQABMA0GCSqGSIb3DQEBCwUAA4GBAFtj7WArQQBugmh/
                    KQjjlfTQ5A052QeXfgTyO9vv1S6MRIi7qgiaEv49cGXnJv/TWbySkMKObPMUApjg
                    6z8PqcxuShew5FCTkNvwhABFPiyu0fUj3e2FEPHfsBu76jz4ugtmhUqjqhzwFY9c
                    tnWRkkl6J0AjM3LnHOSgjNIclDZG"""]
        for index, item in enumerate(certs):
            item = item.replace(' ', '').replace('\n', '')
            certs[index] = item
        return certs


if __name__ == "__main__":
    t = TestHolderOfKeyResponse()
    t.setup_class()
    t.test_hok_response_is_parsed()
