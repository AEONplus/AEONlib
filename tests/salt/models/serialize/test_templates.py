import pytest

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
    salticam = base_salticam.model_dump()
    salticam["filter_sequence"].append({"filter": "Cousins R", "exposure_time": 42})
    if full:
        salticam["dither_pattern"] = base_salticam_dither_pattern.model_dump()
        salticam["include_flat"] = True
    else:
        salticam["dither_pattern"] = None
        salticam["include_flat"] = False
    xml = render_template("salticam.xml", salticam=salticam)

    if full:
        assert "Dither" in xml
        assert "Flat" in xml
    else:
        assert "Dither" not in xml
        assert "Flat" not in xml

    validate_xml(xml)
    assert True


@pytest.mark.parametrize("full", [False, True])
def test_salticam_detector_template(full: bool, base_rss_detector):
    """Test that the RSS detector template generates valid XML."""
    detector = base_rss_detector.model_dump()

    if full:
        detector["window_height"] = 45
    else:
        detector["window_height"] = None

    xml = render_template("rss_detector.xml", detector=detector)

    if full:
        assert "Height" in xml
    else:
        assert "Height" not in xml

    validate_xml(xml)
    assert True
