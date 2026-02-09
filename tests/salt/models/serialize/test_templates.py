import pytest

import astropy.units as u

from aeonlib.salt.models import SalticamFilterSequenceStep
from aeonlib.salt.models.util import render_template, validate_xml


def test_salticam_detector_template(base_salticam_detector):
    """Test that the Salticam detector template generates valid XML."""
    xml = render_template(
        "salticam_detector.xml", detector=base_salticam_detector.model_dump()
    )
    validate_xml(xml)
    assert True


@pytest.mark.parametrize("full", [False, True])
def test_salticam_template(full: bool, base_salticam, base_salticam_dither_pattern):
    salticam = base_salticam
    salticam.filter_sequence.append(
        SalticamFilterSequenceStep(filter="Cousins R", exposure_time=42)
    )
    if full:
        salticam.dither_pattern = base_salticam_dither_pattern
        salticam.include_flat = True
    else:
        salticam.dither_pattern = None
        salticam.include_flat = False
    xml = render_template("salticam.xml", salticam=salticam.model_dump())

    if full:
        assert "Dither" in xml
        assert "Flat" in xml
    else:
        assert "Dither" not in xml
        assert "Flat" not in xml

    validate_xml(xml)
    assert True


@pytest.mark.parametrize("full", [False, True])
def test_rss_detector_template(full: bool, base_rss_detector):
    """Test that the RSS detector template generates valid XML."""
    detector = base_rss_detector

    if full:
        detector.window_height = 45 * u.arcsec
    else:
        detector.window_height = None

    xml = render_template("rss_detector.xml", detector=detector.model_dump())

    if full:
        assert "Height" in xml
    else:
        assert "Height" not in xml

    validate_xml(xml)
    assert True


@pytest.mark.parametrize("full", [False, True])
def test_rss_imaging(full: bool, base_rss_imaging, base_rss_polarimetry):
    """Tests that the RSS imaging template generates valid XML."""
    configuration = base_rss_imaging

    if full:
        configuration.polarimetry = base_rss_polarimetry
    else:
        configuration.polarimetry = None

    xml = render_template("rss_imaging.xml", configuration=configuration.model_dump())

    if full:
        assert "BeamsplitterOrientation" in xml
    else:
        assert "BeamsplitterOrientation" not in xml

    validate_xml(xml)
    assert True


@pytest.mark.parametrize(
    "filter_name, expected_element",
    [("pi04340", "FilterId"), ("Johnson V", "SalticamFilter")],
)
def test_rss_imaging_filter(filter_name: str, expected_element: str, base_rss_imaging):
    """Tests that RSS imaging filters are handled correctly when generating XML."""
    configuration = base_rss_imaging
    configuration.filter = filter_name

    xml = render_template("rss_imaging.xml", configuration=configuration.model_dump())
    assert expected_element in xml

    validate_xml(xml)
    assert True


@pytest.mark.parametrize("full", [False, True])
def test_rss_longslit_spectroscopy(
    full: bool, base_rss_longslit_spectroscopy, base_rss_polarimetry
):
    configuration = base_rss_longslit_spectroscopy

    if full:
        configuration.polarimetry = base_rss_polarimetry
    else:
        configuration.polarimetry = None

    xml = render_template(
        "rss_spectroscopy.xml", configuration=configuration.model_dump()
    )

    assert "PredefinedMask" in xml

    if full:
        assert "BeamsplitterOrientation" in xml
    else:
        assert "BeamsplitterOrientation" not in xml

    validate_xml(xml)
    assert True
