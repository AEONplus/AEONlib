from typing import Any

from gpp_client import GPPClient
from gpp_client.environment import GPPEnvironment
from gpp_client.generated.create_target_by_program_id import CreateTargetByProgramId
from gpp_client.generated.create_target_by_program_reference import (
    CreateTargetByProgramReference,
)
from gpp_client.generated.create_target_by_proposal_reference import (
    CreateTargetByProposalReference,
)
from gpp_client.settings import GPPSettings

from aeonlib.conf import Settings
from aeonlib.conf import settings as default_settings
from aeonlib.models import SiderealTarget

from .conversions import target_properties_from_aeon


class _EnvironmentGPPClient(GPPClient):
    """GPP client with an environment selected at runtime.

    This is a bit of a kludge: the GPP client by default selects the environment based on the
    version of the package installed. .dev for development, or release for production. We want to
    be able to test against development, while using the production/release packages (otherwise
    we'd need to switch the installed version of the package).

    This overrides some internal settings to enabled forcing the environment.
    """

    def __init__(
        self,
        *,
        token: str,
        environment: GPPEnvironment,
        debug: bool = False,
    ) -> None:
        self._environment_override = environment
        super().__init__(token=token, debug=debug)

    def _build_settings(
        self,
        *,
        token: str | None = None,
        debug: bool | None = None,
    ) -> GPPSettings:
        token_settings: dict[str, Any]
        if self._environment_override is GPPEnvironment.DEVELOPMENT:
            token_settings = {"development_token": token}
        else:
            token_settings = {"token": token}

        return GPPSettings(
            environment_override=self._environment_override,
            debug=debug if debug is not None else False,
            **token_settings,
        )


class GeminiFacility:
    """Thin Aeonlib wrapper around the Gemini GPP client."""

    client: GPPClient

    def __init__(self, settings: Settings = default_settings) -> None:
        if not settings.gemini_token:
            raise ValueError("AEON_GEMINI_TOKEN is not set")

        environment = GPPEnvironment(settings.gemini_environment)
        self.client = _EnvironmentGPPClient(
            token=settings.gemini_token,
            environment=environment,
            debug=settings.gemini_debug,
        )

    async def create_target_by_program_id(
        self,
        program_id: str,
        target: SiderealTarget,
        *,
        include_deleted: bool = False,
    ) -> CreateTargetByProgramId:
        return await self.client.target.create_by_program_id(
            program_id,
            properties=target_properties_from_aeon(target),
            include_deleted=include_deleted,
        )

    async def create_target_by_program_reference(
        self,
        program_reference: str,
        target: SiderealTarget,
        *,
        include_deleted: bool = False,
    ) -> CreateTargetByProgramReference:
        return await self.client.target.create_by_program_reference(
            program_reference,
            properties=target_properties_from_aeon(target),
            include_deleted=include_deleted,
        )

    async def create_target_by_proposal_reference(
        self,
        proposal_reference: str,
        target: SiderealTarget,
        *,
        include_deleted: bool = False,
    ) -> CreateTargetByProposalReference:
        return await self.client.target.create_by_proposal_reference(
            proposal_reference,
            properties=target_properties_from_aeon(target),
            include_deleted=include_deleted,
        )
