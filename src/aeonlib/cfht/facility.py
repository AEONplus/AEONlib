from typing import Literal

import httpx

from aeonlib.conf import Settings
from aeonlib.conf import settings as default_settings

from .models import Instrument, ProgramInfo, TargetData

INSTRUMENTS = Literal["SPIROU", "ESPADONS", "MEGACAM"]


class CFHTFacility:
    """CFHT Facility class"""

    def __init__(self, settings: Settings = default_settings):
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

    def targets(self, program_token: str) -> list[TargetData]:
        """Get the list of targets for a given program"""
        response = self._client.get(f"/programs/{program_token}/targets/")
        response.raise_for_status()
        payload = response.json()
        return [
            TargetData.model_validate(target) for target in payload.get("entity", [])
        ]

    def create_or_update_target(
        self, program_token: str, target: TargetData, instrument: Instrument
    ) -> TargetData:
        print(str(instrument.value))
        version = {"value": target.version} if target.version else None
        data = {
            "entity": target.model_dump(),
            "lock_version": version,
            "instrument": instrument.value,
        }
        response = self._client.put(
            f"/programs/{program_token}/targets/{target.token}/",
            json=data,
        )
        print(response.text)
        response.raise_for_status()
        payload = response.json()
        return TargetData.model_validate(payload["entity"])
