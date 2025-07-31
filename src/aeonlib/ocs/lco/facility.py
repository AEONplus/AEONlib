import logging

from aeonlib.conf import Settings
from aeonlib.ocs.facility import OCSFacility

logger = logging.getLogger(__name__)


class LcoFacility(OCSFacility):
    """
    Las Cumbres Observatory Facility
    Configuration:
        - AEON_LCO_TOKEN: API token for authentication
        - AEON_LCO_API_ROOT: Root URL of the API
    """

    def api_root(self, settings: Settings) -> str:
        return settings.lco_api_root

    def api_key(self, settings: Settings) -> str:
        return settings.lco_token
