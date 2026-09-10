from typing import Any

import httpx

from aeonlib.conf import Settings
from aeonlib.conf import settings as default_settings

from .models import (
    ExposureData,
    Instrument,
    ObservingGroupData,
    ObservingTemplateData,
    ProgramInfo,
    TargetData,
)


class VersionMismatchError(ValueError):
    """Raised when the version of the target does not match the server"""


class EntityNotFoundError(ValueError):
    """Raised when the entity is not found"""


class InvalidResponseError(ValueError):
    """Raised when the response is invalid"""


class ServerError(RuntimeError):
    """Raised when the server returns an error"""


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

    def __del__(self):
        self._client.close()

    def _request(
        self,
        method: str,
        url: str,
        *,
        response_key: str = "entity",
        **kwargs: Any,
    ) -> Any:
        response = self._client.request(method, url, **kwargs)
        if response.status_code == httpx.codes.CONFLICT:
            raise VersionMismatchError(
                f"Version mismatch while requesting {response.request.url}"
            )
        if response.status_code == httpx.codes.NOT_FOUND:
            raise EntityNotFoundError(f"Entity not found: {response.request.url}")
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise ServerError(f"CFHT API error: {exc}") from exc
        if method == "DELETE":
            return None

        try:
            return response.json()[response_key]
        except (ValueError, TypeError, KeyError) as exc:
            raise InvalidResponseError(
                f"CFHT API response from {response.request.url} did not contain "
                f"the expected {response_key!r} key"
            ) from exc

    def _program_request(
        self,
        method: str,
        url: str,
        *,
        response_key: str = "entity",
        **kwargs: Any,
    ) -> Any:
        if not self.program_token:
            raise ValueError(
                "Program must be set. Initialize the facility with program_token or use `select_program`"
            )
        return self._request(
            method,
            f"programs/{self.program_token}/{url.lstrip('/')}",
            response_key=response_key,
            **kwargs,
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

    def instruments(self) -> set[Instrument]:
        """Return the instruments allocated to the selected program"""
        if not self.program_token:
            raise ValueError(
                "Program must be set. Initialize the facility with program_token or use `select_program`"
            )
        for program in self.programs():
            program_data = program.program_data
            if program_data is None or program_data.token != self.program_token:
                continue

            return {
                allocation.instrument
                for allocation in program_data.time_allocation or []
                if allocation.instrument is not None
            }

        raise EntityNotFoundError(f"Program not found: {self.program_token}")

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

    def observing_templates(self) -> list[ObservingTemplateData]:
        entities = self._program_request("GET", "observing-templates/")
        return [ObservingTemplateData.model_validate(entity) for entity in entities]

    def create_observing_group(
        self, observing_group: ObservingGroupData
    ) -> ObservingGroupData:
        data = {"entity": observing_group.api_dump()}
        entity = self._program_request(
            "PUT", f"observing-groups/{observing_group.token}/", json=data
        )
        return ObservingGroupData.model_validate(entity)

    def delete_observing_group(self, observing_group_token: str) -> None:
        self._program_request("DELETE", f"observing-groups/{observing_group_token}")

    def exposures(self) -> list[ExposureData]:
        exposures = self._program_request("GET", "exposures/", response_key="exposure")
        return [ExposureData.model_validate(exposure) for exposure in exposures]
