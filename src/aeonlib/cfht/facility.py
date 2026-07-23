from typing import Literal

import httpx

from aeonlib.conf import settings

from .models import ProgramInfo

INSTRUMENTS = Literal["SPIROU", "ESPADONS", "MEGACAM"]


class CFHTFacility:
    """CFHT Facility class"""

    def __init__(self):
        base_url = settings.cfht_api_root
        if not base_url:
            raise ValueError("AEON_CFHT_API_ROOT is not set")
        access_token = settings.cfht_access_token
        if not access_token:
            raise ValueError("AEON_CFHT_ACCESS_TOKEN token is not set")
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        self._client = httpx.Client(base_url=base_url, headers=headers)

    def programs(self) -> list[ProgramInfo]:
        """Get the list of observing programs"""
        response = self._client.get("/programs/")
        response.raise_for_status()

        payload = response.json()
        return [
            ProgramInfo.model_validate(program) for program in payload.get("entity", [])
        ]
