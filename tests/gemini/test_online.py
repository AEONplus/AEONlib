import asyncio

import pytest
from gpp_client.generated.enums import Existence
from gpp_client.generated.exceptions import GraphQLClientHttpError

from aeonlib.gemini import GeminiFacility
from aeonlib.models import SiderealTarget

pytestmark = pytest.mark.online


def test_ping():
    async def ping():
        facility = GeminiFacility()
        ok, error = await facility.client.ping()
        assert ok, error

    asyncio.run(ping())


@pytest.mark.side_effect
def test_create_target_by_program_id():
    async def test_create():
        facility = GeminiFacility()
        target = SiderealTarget(
            name="aeontest-target",
            type="ICRS",
            ra=0,
            dec=0,
        )
        try:
            result = await facility.create_target_by_program_id("p-1531", target)
        except GraphQLClientHttpError as exc:
            pytest.fail(f"GPP HTTP {exc.status_code}: {exc.response.text}")

        created = result.create_target.target
        try:
            assert created.program.id == "p-1531"
            assert created.name == target.name
            assert created.sidereal is not None
        finally:
            deleted = await facility.client.target.delete_by_id(created.id)
            assert len(deleted.update_targets.targets) == 1
            assert deleted.update_targets.targets[0].id == created.id
            assert deleted.update_targets.targets[0].existence is Existence.DELETED

    asyncio.run(test_create())
