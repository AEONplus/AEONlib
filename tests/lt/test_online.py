from datetime import datetime

import pytest
from astropy.coordinates import Angle
from lxml import etree

from aeonlib.lt.facility import LTFacility
from aeonlib.lt.models import LT_INSTRUMENTS, Frodo, Ioo, LTConfig, Sprat
from aeonlib.models import SiderealTarget, Window

pytestmark = pytest.mark.online

CFG = LTConfig(project="LCOTesting2")
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


@pytest.mark.skip(reason="LT endpoint appears to be offline.'")
@pytest.mark.parametrize("ins", INSTRUMENT_TESTS.values(), ids=INSTRUMENT_TESTS.keys())
def test_validate_observation(ins: LT_INSTRUMENTS):
    """Validate all the default instruments"""
    facility = LTFacility()
    result = facility.validate_observation(CFG, ins, TARGET, WINDOW)
    assert result


@pytest.mark.skip(reason="LT endpoint appears to be offline.'")
@pytest.mark.side_effect
def test_submit_observation():
    """This test creates stuff remotely so just do one test with Frodo"""
    facility = LTFacility()
    frodo = Frodo()
    result = facility.submit_observation(CFG, frodo, TARGET, WINDOW)
    assert result

    # Clean Up
    cancel_result = facility.cancel_observation(result, CFG.project)
    assert cancel_result


@pytest.mark.skip(reason="LT endpoint appears to be offline.'")
def test_build_rtml():
    frodo = Frodo()
    facility = LTFacility()
    result = facility._observation_payload(CFG, frodo, TARGET, WINDOW)  # pyright: ignore[reportPrivateUsage]
    result_str = etree.tostring(result, encoding="unicode")
    assert result_str.startswith("<RTML")
