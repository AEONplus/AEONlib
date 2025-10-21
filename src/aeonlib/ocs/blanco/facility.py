from logging import getLogger
from typing import override

from aeonlib.conf import Settings
from aeonlib.ocs.facility import OCSFacility

logger = getLogger(__name__)


class BlancoFacility(OCSFacility):
    """
    BLANCO Facility
    The BLANCO API interface goes through the LCO OCS API, so this
    class is essentially a wrapper around the LCO Facility.
    Configuration:
        - AEON_BLANCO_TOKEN: API token for authentication
        - AEON_BLANCO_API_ROOT: Root URL of the API
    """

    @override
    def api_key(self, settings: Settings) -> str:
        if not settings.blanco_token:
            logger.warning(
                "AEON_BLANCO_TOKEN setting is missing, trying LCO credentials"
            )
            return settings.lco_token
        else:
            return settings.blanco_token

    @override
    def api_root(self, settings: Settings) -> str:
        return settings.blanco_api_root
