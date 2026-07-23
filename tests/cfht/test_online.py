import pytest

from aeonlib.cfht.facility import CFHTFacility

pytestmark = pytest.mark.online


def test_programs():
    facility = CFHTFacility()
    programs = facility.programs()
    print(programs)
    assert programs[0].pi_info
    assert programs[0].pi_info.first_name == "AEON"
    assert False
