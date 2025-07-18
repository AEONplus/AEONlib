import logging

import httpx

from aeonlib.conf import settings as default_settings
from aeonlib.ocs.lco.facility import LcoFacility

logger = logging.getLogger(__name__)


class SAAOFacility(LcoFacility):
    """
    Facility class for the SAAO 1m* AEON compatible observatories.
    Uses the OCS, so this is a simple wrapper around the LCO facility.
    """

    def __init__(self, settings=default_settings):
        if not settings.saao_token:
            logger.warn(
                "AEON_SAAO_TOKEN setting is missing, requests will be unauthenticated"
            )
        else:
            self.headers = {"Authorization": f"Token {settings.saao_token}"}

        self.client = httpx.Client(
            base_url=settings.saao_api_root, headers=self.headers
        )
