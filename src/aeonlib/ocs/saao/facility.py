import logging

from aeonlib.conf import Settings
from aeonlib.ocs.facility import OCSFacility

logger = logging.getLogger(__name__)


class SAAOFacility(OCSFacility):
    """
    Facility class for the SAAO 1m* AEON compatible observatories.
    Uses the OCS, so this is a simple wrapper around the LCO facility.
    """

    def api_key(self, settings: Settings) -> str:
        return settings.saao_token

    def api_root(self, settings: Settings) -> str:
        return settings.saao_api_root
