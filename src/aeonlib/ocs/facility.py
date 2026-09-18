import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, Literal

import httpx
from astropy.table import Table

from aeonlib.conf import Settings
from aeonlib.conf import settings as default_settings
from aeonlib.exceptions import AuthenticationError
from aeonlib.ocs.request_models import (
    RequestGroup,
    SubmittedRequestGroup,
    ValidationResult,
)

logger = logging.getLogger(__name__)


def walk_pagination(
    response: dict[Any, Any], callback: Callable[[dict[Any, Any]], None]
):
    while response["next"]:
        response = httpx.get(response["next"]).json()
        callback(response)


def dict_table(proposals: list[dict[Any, Any]], fields: list[str]) -> Table:
    """Construct an Astropy Table from the given list of dictionaries, containing
    only the specified fields.
    """
    ps = [{field: p[field] for field in fields} for p in proposals]
    return Table(rows=ps)


class OCSFacility(ABC):
    """
    Generic OCS Facility that can be utilized by any facility running the OCS.
    """

    @abstractmethod
    def api_key(self, settings: Settings) -> str:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def api_root(self, settings: Settings) -> str:
        raise NotImplementedError("Subclasses must implement this method")

    def __init__(self, settings: Settings = default_settings):
        headers = {"Authorization": f"Token {self.api_key(settings)}"}
        self.client: httpx.Client = httpx.Client(
            base_url=self.api_root(settings), headers=headers
        )

    def __del__(self):
        self.client.close()

    def proposals(
        self, format: Literal["dict", "table"] = "table"
    ) -> Table | list[dict[Any, Any]]:
        response = self.client.get("/proposals/")
        _ = response.raise_for_status()
        proposals = response.json()["results"]
        walk_pagination(response.json(), lambda x: proposals.extend(x["results"]))
        if format == "dict":
            return proposals
        elif format == "table":
            fields = ["id", "active", "title", "requestgroup_count"]
            return dict_table(proposals, fields)

    def serialize_request_group(self, request_group: RequestGroup) -> dict[str, Any]:
        return request_group.model_dump(mode="json", exclude_none=True)

    def validate_request_group(self, request_group: RequestGroup) -> ValidationResult:
        payload = self.serialize_request_group(request_group)
        logger.debug("LcoFacility.validate_request_group -> %s", payload)
        response = self.client.post("/requestgroups/validate/", json=payload)
        # The logic gets tricky here because we want to intercept 400s and
        # convert them into ValidationResult instead of propagating them
        errors: dict[str, Any] = {}
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            if 401 <= response.status_code <= 403:
                raise AuthenticationError(f"OCS: {response.content}") from exc
            if response.status_code != 400:
                raise

        try:
            data: dict[str, Any] = response.json()
        except ValueError:
            if response.status_code != 400:
                raise
            data = {"errors": {"non_field_errors": [response.text]}}
        logger.debug("<- %s", data)

        details = data.get("errors", data if response.status_code == 400 else {})
        if isinstance(details, dict):
            errors.update(details)
        elif details:
            errors["non_field_errors"] = (
                details if isinstance(details, list) else [str(details)]
            )

        durations = data.get("request_durations") or {}
        valid = response.status_code != 400 and bool(durations) and not errors
        if not valid and not errors:
            errors["non_field_errors"] = [str(data)]
        return ValidationResult(
            valid=valid,
            errors=errors,
            duration=durations.get("duration") if valid else None,
        )

    def submit_request_group(
        self, request_group: RequestGroup
    ) -> SubmittedRequestGroup:
        payload = self.serialize_request_group(request_group)
        logger.debug("-> %s", payload)
        response = self.client.post("/requestgroups/", json=payload)
        _ = response.raise_for_status()
        logger.debug("<- %s", response.content)
        return SubmittedRequestGroup.model_validate_json(response.content)
