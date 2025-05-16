from datetime import datetime, timedelta

from aeonlib.models import SiderealTarget, Window
from aeonlib.ocs import (
    Constraints,
    Location,
    Request,
    RequestGroup,
)
from aeonlib.ocs.soar.instruments import SoarGhtsBluecamImager, SoarTriplespec

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

soar_triplespec = RequestGroup(
    name="test",
    observation_type="NORMAL",
    operator="SINGLE",
    proposal="TEST_PROPOSAL",
    ipp_value=1.0,
    requests=[
        Request(
            location=Location(telescope_class="4m0"),
            configurations=[
                SoarTriplespec(
                    type="SPECTRUM",
                    target=target,
                    constraints=Constraints(max_airmass=3.0),
                    instrument_configs=[
                        SoarTriplespec.config_class(
                            rotator_mode="SKY",
                            exposure_count=1,
                            exposure_time=10,
                            mode="fowler1_coadds1",
                            optical_elements=SoarTriplespec.optical_elements_class(),
                        )
                    ],
                    acquisition_config=SoarTriplespec.acquisition_config_class(
                        mode="MANUAL"
                    ),
                    guiding_config=SoarTriplespec.guiding_config_class(
                        mode="ON", optional=True
                    ),
                )
            ],
            windows=[window],
        )
    ],
)

soar_bulecam_imager = RequestGroup(
    name="test",
    observation_type="NORMAL",
    operator="SINGLE",
    proposal="TEST_PROPOSAL",
    ipp_value=1.0,
    requests=[
        Request(
            location=Location(telescope_class="4m0"),
            configurations=[
                SoarGhtsBluecamImager(
                    type="EXPOSE",
                    target=target,
                    constraints=Constraints(max_airmass=3.0),
                    instrument_configs=[
                        SoarGhtsBluecamImager.config_class(
                            rotator_mode="SKY",
                            exposure_count=1,
                            exposure_time=10,
                            mode="GHTS_B_Image_2x2",
                            optical_elements=SoarGhtsBluecamImager.optical_elements_class(
                                filter="g-SDSS"
                            ),
                        )
                    ],
                    acquisition_config=SoarGhtsBluecamImager.acquisition_config_class(
                        mode="MANUAL"
                    ),
                    guiding_config=SoarGhtsBluecamImager.guiding_config_class(
                        mode="ON", optional=True
                    ),
                )
            ],
            windows=[window],
        )
    ],
)

SOAR_REQUESTS = {
    "soar_triplespec": soar_triplespec,
    "soar_bluecam_imager": soar_bulecam_imager,
}
