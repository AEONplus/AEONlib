from datetime import datetime, timedelta

from aeonlib.models import SiderealTarget, Window
from aeonlib.ocs import (
    Constraints,
    Location,
    Request,
    RequestGroup,
)
from aeonlib.ocs.blanco.instruments import BlancoNewfirm

target = SiderealTarget(
    name="M10",
    type="ICRS",
    ra=254.287,
    dec=-4.72,
)

window = Window(
    start=datetime.now(),
    end=datetime.now() + timedelta(days=60),
)

blanco_newfirm = RequestGroup(
    name="blanco_test",
    observation_type="NORMAL",
    operator="SINGLE",
    proposal="TEST_PROPOSAL",
    ipp_value=1.0,
    requests=[
        Request(
            location=Location(telescope_class="4m0"),
            configurations=[
                BlancoNewfirm(
                    type="EXPOSE",
                    target=target,
                    constraints=Constraints(max_airmass=3.0),
                    instrument_configs=[
                        BlancoNewfirm.config_class(
                            exposure_count=1,
                            exposure_time=2,
                            mode="fowler1",
                            optical_elements=BlancoNewfirm.optical_elements_class(
                                filter="HX"
                            ),
                        )
                    ],
                    acquisition_config=BlancoNewfirm.acquisition_config_class(
                        mode="MANUAL"
                    ),
                    guiding_config=BlancoNewfirm.guiding_config_class(
                        mode="ON", optional=True
                    ),
                )
            ],
            windows=[window],
        )
    ],
)

BLANCO_REQUESTS = {"blanco_newfirm": blanco_newfirm}
