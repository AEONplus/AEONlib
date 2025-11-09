import pathlib

import astropy.coordinates
import pytest
from astropy import units as u

from aeonlib.salt.models import (
    Acquisition,
    Block,
    Constraints,
    MagnitudeRange,
    ReferenceStar,
    Request,
    Salticam,
    SalticamDitherPattern,
    SaltSiderealTarget,
    SalticamFilterSequenceStep,
    SalticamDetector,
    Rss,
    RssImaging,
    RssPolarimetry,
    RssSpectroscopy,
)


@pytest.fixture()
def base_request(base_block):
    """A simple request to edit or build from."""
    return Request(proposal_code="2025-1-SCI-042", blocks=[base_block])


@pytest.fixture()
def base_block(base_acquisition, base_constraints, base_target):
    """A simple block to build or edit from."""
    return Block(
        name="Test",
        priority=1,
        ranking="high",
        num_visits=1,
        constraints=base_constraints,
        target=base_target,
        acquisition=base_acquisition,
        instrument=None,
    )


@pytest.fixture()
def base_target(base_magnitude_range):
    """A simple sidereal target to build or edit from."""
    return SaltSiderealTarget(
        name="Test Target",
        type="ICRS",
        ra=0,
        dec=0,
        target_type="Nova",
        magnitude_range=base_magnitude_range,
    )


@pytest.fixture()
def base_magnitude_range():
    """A simple magnitude range to build or edit from."""
    return MagnitudeRange(min_magnitude=17.1, max_magnitude=17.5, bandpass="V")


@pytest.fixture()
def base_constraints():
    return Constraints(
        transparency="thick cloud",
        max_lunar_phase_percentage=50,
        min_lunar_distance=astropy.coordinates.Angle("45d"),
        max_seeing=3,
    )


@pytest.fixture()
def base_acquisition():
    finder_chart = (
        pathlib.Path(__file__).parent.parent / "data" / "dummy_finder_chart.pdf"
    )
    return Acquisition(finder_charts=[finder_chart])


@pytest.fixture()
def base_reference_star():
    return ReferenceStar(ra=117.564 * u.deg, dec=-63.9 * u.deg)


@pytest.fixture()
def base_salticam(base_salticam_detector, base_salticam_filter_sequence_step):
    return Salticam(
        filter_sequence=[base_salticam_filter_sequence_step],
        detector=base_salticam_detector,
        include_flat=True,
    )


@pytest.fixture()
def base_salticam_filter_sequence_step():
    return SalticamFilterSequenceStep(filter="Johnson B", exposure_time=409 * u.s)


@pytest.fixture()
def base_salticam_detector():
    return SalticamDetector(
        num_exposures=1,
        gain="bright",
        readout_speed="fast",
        num_prebinned_rows=2,
        num_prebinned_columns=2,
    )


@pytest.fixture()
def base_salticam_dither_pattern():
    return SalticamDitherPattern(num_rows=3, num_columns=4, offset=12.9)


@pytest.fixture()
def base_rss(base_rss_imaging):
    return Rss(configuration=base_rss_imaging, detector=None, dither_pattern=None)


@pytest.fixture()
def base_rss_polarimetry():
    return RssPolarimetry(wave_plate_pattern="linear")


@pytest.fixture()
def base_rss_imaging():
    return RssImaging(filter="pi04400", polarimetry=None, include_flat=True)


@pytest.fixture()
def base_rss_spectroscopy(base_rss_polarimetry):
    return RssSpectroscopy(
        grating="pg0900",
        grating_angle=20 * u.deg,
        articulation_angle=40 * u.deg,
        order_blocking_filter="pc04600",
        polarimetry=base_rss_polarimetry,
        include_flat=True,
        include_arc=True,
        request_spectrophotometric_standard=False,
    )
