from datetime import datetime, timedelta

from aeonlib.models import SiderealTarget, Window
from aeonlib.ocs import (
    Constraints,
    Location,
    Request,
    RequestGroup,
)
from aeonlib.ocs.saao.instruments import SAAO1M0AMookodiImg

target = SiderealTarget(
    name="M10",
    type="ICRS",
    ra=254.287,
    dec=-4.72,
)

window = Window(
    start=datetime.now(),
    end=datetime.now() + timedelta(days=7),
)

saao_sibonise_imager = RequestGroup(
    name="test",
    observation_type="NORMAL",
    operator="SINGLE",
    proposal="IO_support_2024-1",
    ipp_value=1.0,
    requests=[
        Request(
            location=Location(telescope_class="1m0"),
            configurations=[
                SAAO1M0AMookodiImg(
                    type="EXPOSE",
                    target=target,
                    constraints=Constraints(max_airmass=3.0),
                    instrument_configs=[
                        SAAO1M0AMookodiImg.config_class(
                            exposure_count=1,
                            exposure_time=10,
                            mode="1x1HighFastOpen",
                            optical_elements=SAAO1M0AMookodiImg.optical_elements_class(
                                obfilter="Clear", filter="r'", slit="out", grism="in"
                            ),
                        )
                    ],
                    acquisition_config=SAAO1M0AMookodiImg.acquisition_config_class(
                        mode="AcN:OFF&Acq:OFF"
                    ),
                    guiding_config=SAAO1M0AMookodiImg.guiding_config_class(
                        mode="GUIDE OFF", optional=True
                    ),
                )
            ],
            windows=[window],
        )
    ],
)

SAAO_REQUESTS = {
    "saao_sibonise_imager": saao_sibonise_imager,
}
