from datetime import datetime

import pytest
from astropy.coordinates import Angle

from aeonlib.lt.facility import LTFacility
from aeonlib.lt.models import Frodo, LTObservation
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


def test_validate_observation():
    facility = LTFacility()
    frodo = Frodo()
    payload = facility.observation_payload(frodo, TARGET, WINDOW, OBSERVATION)
    result = facility.validate_observation(payload)
    assert result


@pytest.mark.side_effect
def test_submit_observation():
    facility = LTFacility()
    frodo = Frodo()
    payload = facility.observation_payload(frodo, TARGET, WINDOW, OBSERVATION)
    result = facility.submit_observation(payload)
    assert result
    print("uid", result)

    # Clean Up
    cancel_result = facility.cancel_observation(result, OBSERVATION.project)
    assert cancel_result
