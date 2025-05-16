from logging import getLogger

import httpx

from aeonlib.conf import settings as default_settings
from aeonlib.ocs.lco.facility import LcoFacility

logger = getLogger(__name__)


class SoarFacility(LcoFacility):
    """
    SOAR Facility
    The SOAR API interface goes through the LCO OCS API, so this
    class is essentially a wrapper around the LCO Facility.
    Configuration:
        - AEON_SOAR_TOKEN: API token for authentication
        - AEON_SOAR_API_ROOT: Root URL of the API
    """

    def __init__(self, settings=default_settings):
        """
        Attempt to authenticate with the SOAR specific credentials, or fall back
        to LCO credentials if they don't exist.
        """
        if not settings.soar_token:
            logger.warn("AEON_SOAR_TOKEN setting is missing, trying LCO credentials")
            if not settings.lco_token:
                logger.warn(
                    "AEON_LCO_TOKEN setting is missing, requests will be unauthenticated"
                )
            else:
                self.headers = {"Authorization": f"Token {settings.lco_token}"}
        else:
            self.headers = {"Authorization": f"Token {settings.soar_token}"}
        self.client = httpx.Client(
            base_url=settings.soar_api_root, headers=self.headers
        )
