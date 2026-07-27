from typing import Literal

import httpx

from aeonlib.conf import settings

from .models import Instrument, ProgramInfo, TargetData

INSTRUMENTS = Literal["SPIROU", "ESPADONS", "MEGACAM"]


class CFHTFacility:
    """CFHT Facility class"""

    def __init__(self, api_root: str | None = None, access_token: str | None = None):
        """Initialize the CFHT Facility client. Sets `_client` property.

        Args:
            api_root: The API root URL. Defaults to None.
            access_token: The access token for authentication. Defaults to None.

        Note:
            Arguments take precedence over the aeonlib.conf.settings.

        Raises:
            ValueError: If AEON_CFHT_API_ROOT is not set.
            ValueError: If AEON_CFHT_ACCESS_TOKEN is not set.
        """
        base_url = api_root or settings.cfht_api_root
        if not base_url:
            raise ValueError("AEON_CFHT_API_ROOT is not set")

        access_token = access_token or settings.cfht_access_token
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
        """Get the list of Kealahou targets for a given program.

        Args:
            program_token: CFHT API's unique string identifier ("token") for
                the observing program whose targets should be retrieved.
                From :meth:`programs` (see ``ProgramInfo.token``); used to
                build the request URL.

        Returns:
            list[TargetData]: The targets currently registered for the
            program, as returned by the CFHT API. Each element is a
            validated ``TargetData`` instance including server-assigned
            fields such as ``token`` and ``version``. Returns an empty list
            if the program has no targets.
        """
        response = self._client.get(f"/programs/{program_token}/targets/")
        response.raise_for_status()
        payload = response.json()
        kealahou_targets = [
            TargetData.model_validate(target) for target in payload.get("entity", [])
        ]
        return kealahou_targets

    def create_or_update_target(
        self, program_token: str, target: TargetData, instrument: Instrument
    ) -> TargetData:
        """Create or update a Kealahou target within a CFHT observing program.

        If ``target.token`` corresponds to an existing target within the
        program, that target is updated in place. Otherwise, a new target is
        created. Callers that already have a ``TargetData`` instance (e.g.
        from a prior call to :meth:`targets`) can pass it directly here to
        push local edits back to the CFHT API.

        Args:
            program_token: CFHT API's unique string identifier ("token") for the
                observing program that owns this target (not a
                security/auth token). From
                :meth:`programs` (see ``ProgramInfo.token``); used to
                build the request URL.
            target: The target data to create or update. This is a Pydantic
                ``BaseModel`` subclass (see ``aeonlib.cfht.models.TargetData``),
                so its fields are validated; can be serialized via
                ``model_dump``.
            instrument: The instrument this target is intended for.

        Returns:
            TargetData: The target as returned by the CFHT API after the
            create/update operation, including any server-assigned fields
            such as ``token`` and ``version``.
        """
        version = {"value": target.version} if target.version else None
        # construct PUT request payload
        data = {
            "entity": target.model_dump(
                by_alias=True,  # use BaseModel Field(alias=... names, not attribute names
                exclude_none=True,  # don't send None-valued fields
            ),
            "lock_version": version,
            "instrument": instrument.value,
        }
        response = self._client.put(
            f"/programs/{program_token}/targets/{target.token}/",
            json=data,
        )
        response.raise_for_status()
        payload = response.json()
        return TargetData.model_validate(payload["entity"])
