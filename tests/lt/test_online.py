from datetime import datetime

import pytest
from astropy.coordinates import Angle

from aeonlib.lt.facility import LTFacility
from aeonlib.lt.models import LT_INSTRUMENTS, Frodo, Ioo, LTObservation, Sprat
from aeonlib.models import SiderealTarget, Window

pytestmark = pytest.mark.online

OBSERVATION = LTObservation(project="LCOTesting2")
TARGET = SiderealTarget(
    name="Vega",
    type="ICRS",
    ra=Angle("18:36:56.336", unit="hourangle"),
    dec=Angle("+38:47:01.280", unit="deg"),
)
WINDOW = Window(start=datetime(2020, 2, 18, 18), end=datetime(2020, 2, 28))

INSTRUMENT_TESTS = {
    "IOO": Ioo(),
    "FRODO": Frodo(),
    "SPRAT": Sprat(),
}


@pytest.mark.parametrize("ins", INSTRUMENT_TESTS.values(), ids=INSTRUMENT_TESTS.keys())
def test_validate_observation(ins: LT_INSTRUMENTS):
    """Validate all the default instruments"""
    facility = LTFacility()
    payload = facility.observation_payload(ins, TARGET, WINDOW, OBSERVATION)
    result = facility.validate_observation(payload)
    assert result


@pytest.mark.side_effect
def test_submit_observation():
    """This test creates stuff remotely so just do one test with Frodo"""
    facility = LTFacility()
    frodo = Frodo()
    payload = facility.observation_payload(frodo, TARGET, WINDOW, OBSERVATION)
    result = facility.submit_observation(payload)
    assert result

    # Clean Up
    cancel_result = facility.cancel_observation(result, OBSERVATION.project)
    assert cancel_result
