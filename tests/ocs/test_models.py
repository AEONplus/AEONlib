from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from aeonlib.ocs.lco.instruments import Lco1M0ScicamSinistro, Lco1M0ScicamSinistroConfig
from aeonlib.ocs.request_models import (
    Location,
    Request,
    RequestGroup,
    Window,
)
from aeonlib.ocs.target_models import Constraints, Target


@pytest.fixture
def request_group() -> RequestGroup:
    """The simplest possible request group to edit or build from."""
    return RequestGroup(
        name="test",
        observation_type="NORMAL",
        operator="SINGLE",
        proposal="test",
        ipp_value=1.0,
        requests=[
            Request(
                location=Location(telescope_class="1m0"),
                configurations=[
                    Lco1M0ScicamSinistro(
                        type="EXPOSE",
                        target=Target(name="M51", type="ICRS"),
                        constraints=Constraints(),
                        instrument_configs=[
                            Lco1M0ScicamSinistroConfig(
                                exposure_count=1,
                                exposure_time=10,
                                mode="central_2k_2x2",
                                filters="R",
                            )
                        ],
                    )
                ],
                windows=[
                    Window(
                        start=datetime.now(),
                        end=datetime.now() + timedelta(days=30),
                    )
                ],
            )
        ],
    )


class TestCommonValidationErrors:
    def test_value_missing(self):
        """
        Test that a ValidationError is raised when a required field (proposal) is missing.
        """
        with pytest.raises(ValidationError) as exc_info:
            RequestGroup(  # type: ignore
                name="test",
                observation_type="NORMAL",
                operator="SINGLE",
                ipp_value=1.0,
            )
        assert exc_info.value.errors()[0]["loc"] == ("proposal",)
        assert exc_info.value.errors()[0]["type"] == "missing"

    def test_max_length_string(self, request_group: RequestGroup):
        """
        Test that a ValidationError is raised when the name field on a
        RequestGroup exceeds the maximum length of 50 characters.
        """
        with pytest.raises(ValidationError) as exc_info:
            request_group.name = "A" * 100
        assert exc_info.value.errors()[0]["loc"] == ("name",)
        assert exc_info.value.errors()[0]["type"] == "string_too_long"

    def test_invalid_choice(self, request_group: RequestGroup):
        """
        Test that a ValidationError is raised when the observation_type field on a
        RequestGroup is not one of the allowed values.
        """
        with pytest.raises(ValidationError) as exc_info:
            request_group.observation_type = "INVALID"  # type: ignore
        assert exc_info.value.errors()[0]["loc"] == ("observation_type",)
        assert exc_info.value.errors()[0]["type"] == "literal_error"

    def test_positive_float(self, request_group: RequestGroup):
        """
        Test that a ValidationError is raised when the ipp_value field on a
        RequestGroup is not a positive float.
        """
        with pytest.raises(ValidationError) as exc_info:
            request_group.ipp_value = -1.0
        assert exc_info.value.errors()[0]["loc"] == ("ipp_value",)
        assert exc_info.value.errors()[0]["type"] == "greater_than_equal"

    def test_value_out_of_range(self, request_group: RequestGroup):
        """
        Test that a ValidationError is raised when the acceptability_threshold field on a
        Request is greater than 100.
        """
        request = request_group.requests[0]
        with pytest.raises(ValidationError) as exc_info:
            request.acceptability_threshold = 200
        assert exc_info.value.errors()[0]["loc"] == ("acceptability_threshold",)
        assert exc_info.value.errors()[0]["type"] == "less_than_equal"
