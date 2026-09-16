from unittest.mock import patch

import pytest
from gpp_client.environment import GPPEnvironment

from aeonlib.conf import Settings
from aeonlib.gemini.facility import GeminiFacility


def test_missing_token():
    with pytest.raises(ValueError, match="AEON_GEMINI_TOKEN"):
        GeminiFacility(Settings(gemini_token=""))


def test_facility_passes_settings_to_client():
    settings = Settings(
        gemini_token="token",
        gemini_environment="development",
        gemini_debug=True,
    )

    with patch("aeonlib.gemini.facility._EnvironmentGPPClient") as client_class:
        facility = GeminiFacility(settings)

    client_class.assert_called_once_with(
        token="token",
        environment=GPPEnvironment.DEVELOPMENT,
        debug=True,
    )
    assert facility.client is client_class.return_value
