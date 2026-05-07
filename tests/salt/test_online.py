from datetime import datetime, timedelta

import pytest
from aeonlib.models import Window
from aeonlib.salt.facility import SALTFacility

window = Window(
    start=datetime.now(),
    end=datetime.now() + timedelta(days=365),
)

# Replace with an appropriate proposal code.
proposal_code = "2026-1-DDT-002"


@pytest.mark.online
def test_validate(base_request):
    # Test online proposal validation."""
    base_request.proposal_code = proposal_code
    base_request.blocks[0].windows = [window]
    facility = SALTFacility(use_playground=True)
    valid, errors = facility.validate(base_request)
    assert valid or errors


@pytest.mark.online
def test_submit(base_request):
    # Test online proposal validation."""
    base_request.proposal_code = proposal_code
    base_request.blocks[0].windows = [window]
    facility = SALTFacility(use_playground=True)
    submission = facility.submit(base_request)
    assert submission
