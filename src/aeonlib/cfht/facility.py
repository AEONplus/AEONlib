from typing import Any

import httpx

from aeonlib.conf import Settings
from aeonlib.conf import settings as default_settings

from .models import Instrument, ProgramInfo, TargetData


class VersionMismatchError(ValueError):
    """Raised when the version of the target does not match the server"""


class EntityNotFoundError(ValueError):
    """Raised when the entity is not found"""


class InvalidResponseError(ValueError):
    """Raised when the response is invalid"""


class CFHTFacility:
    """CFHT Facility class"""

    def __init__(
        self, settings: Settings = default_settings, program_token: str | None = None
    ):
        base_url = settings.cfht_api_root
        if not base_url:
            raise ValueError("AEON_CFHT_API_ROOT is not set")
        access_token = settings.cfht_access_token
        if not access_token:
            raise ValueError("AEON_CFHT_ACCESS_TOKEN token is not set")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        self._client = httpx.Client(base_url=base_url, headers=headers)
        self.program_token = program_token

    def _request(self, method: str, url: str, **kwargs: Any) -> Any:
        response = self._client.request(method, url, **kwargs)
        if response.status_code == httpx.codes.CONFLICT:
            raise VersionMismatchError(
                f"Version mismatch while requesting {response.request.url}"
            )
        if response.status_code == httpx.codes.NOT_FOUND:
            raise EntityNotFoundError(f"Entity not found: {response.request.url}")
        response.raise_for_status()
        if method == "DELETE":
            return None
        try:
            return response.json()["entity"]
        except (ValueError, TypeError, KeyError) as exc:
            raise InvalidResponseError(
                f"CFHT API response from {response.request.url} did not contain an entity"
            ) from exc

    def _program_request(self, method: str, url: str, **kwargs: Any) -> Any:
        if not self.program_token:
            raise ValueError(
                "Program must be set. Initialize the facility with a ProgramInfo or use `select_program`"
            )
        return self._request(
            method, f"programs/{self.program_token}/{url.lstrip('/')}", **kwargs
        )

    def select_program(self, program: ProgramInfo) -> None:
        if program.program_data is None:
            raise ValueError("Program data is not set")
        token = program.program_data.token
        if not token:
            raise ValueError("Program token is not set")
        self.program_token = token

    def programs(self) -> list[ProgramInfo]:
        """Get the list of observing programs"""
        entities = self._request("GET", "programs/")
        return [ProgramInfo.model_validate(entity) for entity in entities]

    def targets(self) -> list[TargetData]:
        """Get the list of targets for a given program"""
        entities = self._program_request("GET", "targets/")
        return [TargetData.model_validate(target) for target in entities]

    def get_target(self, target_token: str) -> TargetData:
        entity = self._program_request("GET", f"targets/{target_token}")
        return TargetData.model_validate(entity)

    def delete_target(self, target_token: str) -> None:
        self._program_request("DELETE", f"targets/{target_token}")

    def create_or_update_target(
        self, target: TargetData, instrument: Instrument
    ) -> TargetData:
        version = {"value": target.version} if target.version is not None else None
        data = {
            "entity": target.api_dump(),
            "lock_version": version,
            "instrument": instrument.value,
        }
        entity = self._program_request("PUT", f"targets/{target.token}/", json=data)
        return TargetData.model_validate(entity)
