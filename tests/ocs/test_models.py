from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from aeonlib.conf import Settings
from aeonlib.models import NonSiderealTarget, SiderealTarget, Window
from aeonlib.ocs import (
    Constraints,
    Location,
    Request,
    RequestGroup,
)
from aeonlib.ocs.lco.facility import LcoFacility
from aeonlib.ocs.lco.instruments import Lco1M0ScicamSinistro


@pytest.fixture
def request_group() -> RequestGroup:
    """The simplest possible request group to edit or build from."""
    instrument = Lco1M0ScicamSinistro

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
                    instrument(
                        type="EXPOSE",
                        target=SiderealTarget(
                            name="M51", type="ICRS", ra=202.469, dec=47.195
                        ),
                        constraints=Constraints(),
                        instrument_configs=[
                            instrument.config_class(
                                exposure_count=1,
                                exposure_time=10,
                                mode="central_2k_2x2",
                                optical_elements=instrument.optical_elements_class(
                                    filter="R"
                                ),
                            )
                        ],
                        acquisition_config=instrument.acquisition_config_class(
                            mode="OFF"
                        ),
                        guiding_config=instrument.guiding_config_class(
                            mode="ON", optional=True
                        ),
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


class TestSerialization:
    def test_time_fields_serialized_as_mjd(self, request_group: RequestGroup):
        """
        Test that certain time fields on a RequestGroup are serialized as MJD.
        This is likely specific to LCO/OCS so only the LCO Facility has this behavior.
        """
        facility = LcoFacility(settings=Settings(lco_token="", lco_api_root=""))
        target = NonSiderealTarget(
            name="mover",
            type="ORBITAL_ELEMENTS",
            scheme="JPL_MINOR_PLANET",
            epochofel=datetime(2025, 1, 1),  # Time as datetime
            orbinc=0.0,
            longascnode=0.0,
            argofperih=0.0,
            eccentricity=1.0,
            meandist=1.0,
            meananom=0.0,
            epochofperih=2460676.5,  # Time as JD
        )
        request_group.requests[0].configurations[0].target = target
        result = facility.serialize_request_group(request_group)
        result_target = result["requests"][0]["configurations"][0]["target"]
        # Assert that the resulting serialized values are in MJD
        assert result_target["epochofel"] == 60676.0
        assert result_target["epochofperih"] == 60676.0
