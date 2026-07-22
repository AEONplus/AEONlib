import pytest

from aeonlib.cfht.facility import CFHTFacility

pytestmark = pytest.mark.online


def test_target_api():
    facility = CFHTFacility()
    programs = facility.programs()
    print(programs)
    for program in programs:
        print(program.program_data)
        # assert program.program_data
        # assert program.program_data.token
    assert False
