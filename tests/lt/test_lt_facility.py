from datetime import datetime, timedelta

from lxml import etree

from aeonlib.lt.facility import LTFacility
from aeonlib.lt.models import Frodo, LTObservation
from aeonlib.models import SiderealTarget, Window

OBSERVATION = LTObservation(project="LCOTesting2")
TARGET = SiderealTarget(name="TestTarget", type="ICRS", ra=12.3456789, dec=-23.456789)
WINDOW = Window(start=datetime.now(), end=datetime.now() + timedelta(days=30))


def test_build_rtml():
    frodo_inst = Frodo()
    facility = LTFacility()
    result = facility.observation_payload(frodo_inst, TARGET, WINDOW, OBSERVATION)
    result_str = etree.tostring(result, encoding="unicode")
    assert result_str.startswith("<RTML")
