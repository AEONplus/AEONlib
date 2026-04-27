import pathlib
import uuid

import astropy.coordinates
import pytest
from astropy import units as u

from aeonlib.salt.models import (
    Acquisition,
    Block,
    Constraints,
    Hrs,
    HrsDetector,
    MagnitudeRange,
    ReferenceStar,
    Request,
    Salticam,
    SalticamDitherPattern,
    SaltSiderealTarget,
    SalticamFilterSequenceStep,
    SalticamDetector,
    Rss,
    RssDetector,
    RssDitherPattern,
    RssImaging,
    RssPolarimetry,
    RssSpectroscopy,
    RssLongslitSpectroscopy,
    RssMultiObjectSpectroscopy,
    RssSlitMaskIFUSpectroscopy,
    Nirwals,
    NirwalsDitherPatternStep,
)


@pytest.fixture()
def base_request(base_block):
    """A simple request to edit or build from."""
    return Request(
        proposal_code="2025-1-SCI-042", semester="2026-1", blocks=[base_block]
    )


@pytest.fixture()
def base_block(base_acquisition, base_constraints, base_target, base_salticam):
    """A simple block to build or edit from."""
    return Block(
        name="Test",
        priority=1,
        ranking="high",
        num_visits=1,
        min_nights_between_visits=0,
        constraints=base_constraints,
        target=base_target,
        acquisition=base_acquisition,
        instrument=base_salticam,
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
    finder_chart = pathlib.Path(__file__).parent / "data" / "dummy_finder_chart_1.pdf"
    return Acquisition(finder_charts=[finder_chart], position_angle=45 * u.deg)


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
def base_rss(base_rss_imaging, base_rss_detector, base_rss_dither_pattern):
    return Rss(
        configuration=base_rss_imaging,
        detector=base_rss_detector,
        dither_pattern=base_rss_dither_pattern,
    )


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


@pytest.fixture()
def base_rss_longslit_spectroscopy(base_rss_spectroscopy):
    return RssLongslitSpectroscopy(
        **base_rss_spectroscopy.model_dump(), slit="PL0125N001"
    )


@pytest.fixture()
def base_rss_multi_object_spectroscopy(base_rss_spectroscopy):
    return RssMultiObjectSpectroscopy(
        **base_rss_spectroscopy.model_dump(),
        mask=pathlib.Path(__file__).parent / "data" / "dummy_rss_mos_mask.rsmt",
    )


@pytest.fixture()
def base_rss_slit_mask_ifu_spectroscopy(base_rss_spectroscopy):
    return RssSlitMaskIFUSpectroscopy(
        **base_rss_spectroscopy.model_dump(),
        slit_mask_ifu="PF0200N001",
    )


@pytest.fixture()
def base_rss_detector():
    return RssDetector(
        exposure_time=120 * u.s,
        gain="bright",
        readout_speed="fast",
        num_prebinned_rows=2,
        num_prebinned_columns=2,
        window_height=100 * u.arcsec,
    )


@pytest.fixture()
def base_rss_dither_pattern():
    return RssDitherPattern(num_rows=3, num_columns=4, offset=12.9)


@pytest.fixture()
def base_hrs(base_hrs_detector):
    return Hrs(
        mode="medium resolution", blue_arm=base_hrs_detector, red_arm=base_hrs_detector
    )


@pytest.fixture()
def base_hrs_detector():
    return HrsDetector(exposure_times=[50 * u.s, 45])


@pytest.fixture()
def base_nirwals(base_nirwals_dither_pattern_step):
    return Nirwals(
        grating="NG0950",
        grating_angle=25 * u.deg,
        articulation_angle=50 * u.deg,
        camera_filter="cutoff 1.5um",
        dither_pattern=[
            base_nirwals_dither_pattern_step,
            base_nirwals_dither_pattern_step,
        ],
        include_flat=False,
    )


@pytest.fixture()
def base_nirwals_dither_pattern_step():
    return NirwalsDitherPatternStep(
        offset_type="FIF offset",
        horizontal_offset=-20 * u.arcsec,
        vertical_offset=35 * u.arcsec,
        exposure_type="science",
        exposure_time=200 * u.s,
        gain="faint",
        sampling="up-the-ramp",
    )


@pytest.fixture()
def create_test_binary_file(tmp_path: pathlib.Path):
    """
    Return a function for generating test files.

    The returned function accepts content (as bytes, such as b"I'm a test file." and a
    file extension (such as ".pdf"), generates a temporary file with the given content
    and file extension, and returns the path to the generated file.
    """

    def _create_file(content: bytes, extension: str) -> pathlib.Path:
        file_path = tmp_path / f"{str(uuid.uuid4())}{extension}"
        file_path.write_bytes(content)
        return file_path

    return _create_file
