import asyncio

import pytest

from aeonlib.gemini import GeminiFacility

pytestmark = pytest.mark.online


def test_ping():
    async def ping():
        facility = GeminiFacility()
        ok, error = await facility.client.ping()
        assert ok, error

    asyncio.run(ping())
