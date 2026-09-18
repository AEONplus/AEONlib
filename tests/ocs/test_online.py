"""
These tests do real validation against an LCO OCS API. To run them, you
must run the "online" mark explicitly: pytest -m online.

By default test will run against an OCS running at http://localhost:8000
set the AEONLIB_TEST_OCS environmental variable to test against a different
address.

The LCO requests assume you are a member of a proposal named TEST_PROPOSAL that has time
on all instruments.
"""

import logging

import pytest

from aeonlib.ocs.blanco.facility import BlancoFacility
from aeonlib.ocs.lco.facility import LcoFacility
from aeonlib.ocs.request_models import RequestGroup
from aeonlib.ocs.saao.facility import SAAOFacility
from aeonlib.ocs.soar.facility import SoarFacility

from .blanco_requests import BLANCO_REQUESTS
from .lco_requests import LCO_REQUESTS
from .saao_requests import SAAO_REQUESTS
from .soar_requests import SOAR_REQUESTS

logger = logging.getLogger(__name__)
pytestmark = pytest.mark.online


@pytest.fixture
def lco_facility() -> LcoFacility:
    return LcoFacility()


@pytest.mark.parametrize(
    "request_group", LCO_REQUESTS.values(), ids=LCO_REQUESTS.keys()
)
def test_valid_lco_requests(lco_facility: LcoFacility, request_group: RequestGroup):
    result = lco_facility.validate_request_group(request_group)
    if not result.valid:
        logger.error("Online validation failed. Server response: %s", result.errors)
    assert result.valid
    assert result.duration and result.duration > 0.0


def test_invalid_lco_request(lco_facility: LcoFacility):
    request_group = LCO_REQUESTS["lco_1m0_scicam_sinistro"].model_copy(deep=True)
    # Set an unreasonably low airmass to trigger server side validation failure
    request_group.requests[0].configurations[0].constraints.max_airmass = 1.0
    result = lco_facility.validate_request_group(request_group)
    assert not result.valid
    assert result.errors
    assert (
        "loosening the airmass" in result.errors["requests"][0]["non_field_errors"][0]
    )


@pytest.mark.side_effect
def test_submit_lco_request(lco_facility: LcoFacility):
    request_group_in = LCO_REQUESTS["lco_1m0_scicam_sinistro"]
    request_group_out = lco_facility.submit_request_group(request_group_in)
    assert request_group_out.id
    assert request_group_out.state == "PENDING"
    assert request_group_out.created


# Soar requests work exactly like LCO requests
@pytest.fixture
def soar_facility() -> SoarFacility:
    return SoarFacility()


@pytest.mark.parametrize(
    "request_group", SOAR_REQUESTS.values(), ids=SOAR_REQUESTS.keys()
)
def test_valid_soar_requests(soar_facility: SoarFacility, request_group: RequestGroup):
    result = soar_facility.validate_request_group(request_group)
    if not result.valid:
        logger.error("Online validation failed. Server response: %s", result.errors)
    assert result.valid
    assert result.duration and result.duration > 0.0


@pytest.mark.side_effect
def test_submit_soar_request(soar_facility: SoarFacility):
    request_group_in = SOAR_REQUESTS["soar_triplespec"]
    request_group_out = soar_facility.submit_request_group(request_group_in)
    assert request_group_out.id
    assert request_group_out.state == "PENDING"
    assert request_group_out.created


# SAAO works the same as LCO and SOAR
@pytest.fixture
def saao_facility() -> SAAOFacility:
    return SAAOFacility()


@pytest.mark.parametrize(
    "request_group", SAAO_REQUESTS.values(), ids=SAAO_REQUESTS.keys()
)
def test_valid_saao_requests(saao_facility: SAAOFacility, request_group: RequestGroup):
    result = saao_facility.validate_request_group(request_group)
    if not result.valid:
        logger.error("Online validation failed. Server response: %s", result.errors)
    assert result.valid
    assert result.duration and result.duration > 0.0


# BLANCO tests
@pytest.fixture
def blanco_facility() -> BlancoFacility:
    return BlancoFacility()


@pytest.mark.parametrize(
    "request_group", BLANCO_REQUESTS.values(), ids=BLANCO_REQUESTS.keys()
)
def test_valid_blanco_requests(
    blanco_facility: BlancoFacility, request_group: RequestGroup
):
    result = blanco_facility.validate_request_group(request_group)
    if not result.valid:
        logger.error("Online validation failed. Server response: %s", result.errors)
    assert result.valid
    assert result.duration and result.duration > 0.0


@pytest.mark.side_effect
def test_submit_blanco_request(blanco_facility: BlancoFacility):
    request_group_in = BLANCO_REQUESTS["blanco_newfirm"]
    request_group_out = blanco_facility.submit_request_group(request_group_in)
    assert request_group_out.id
    assert request_group_out.state == "PENDING"
    assert request_group_out.created
