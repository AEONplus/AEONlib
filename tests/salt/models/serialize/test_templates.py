import pytest

import astropy.units as u

from aeonlib.salt.models import SalticamFilterSequenceStep
from aeonlib.salt.models.util import render_template, validate_xml


class TestSalticamTemplates:
    def test_salticam_detector_template(self, base_salticam_detector):
        """Test that the Salticam detector template generates valid XML."""
        xml = render_template(
            "salticam_detector.xml", detector=base_salticam_detector.model_dump()
        )
        validate_xml(xml)
        assert True

    def test_salticam_dithering_pattern(self, base_salticam_dither_pattern):
        """Test that the Salticam dither pattern template generates valid XML."""
        dither_pattern = base_salticam_dither_pattern

        xml = render_template(
            "salticam_dither_pattern.xml", dither_pattern=dither_pattern.model_dump()
        )

        validate_xml(xml)

    @pytest.mark.parametrize("full", [False, True])
    def test_salticam_template(
        self, full: bool, base_salticam, base_salticam_dither_pattern
    ):
        """Test that the Salticam template generates valid XML."""
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
            assert "SalticamDefaultCalibrationFlat" in xml
        else:
            assert "Dither" not in xml
            assert "SalticamDefaultCalibrationFlat" not in xml

        validate_xml(xml)
        assert True


class TestRssTemplates:
    @pytest.mark.parametrize("full", [False, True])
    def test_rss_detector_template(self, full: bool, base_rss_detector):
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
    def test_rss_imaging(self, full: bool, base_rss_imaging, base_rss_polarimetry):
        """Tests that the RSS imaging template generates valid XML."""
        configuration = base_rss_imaging

        if full:
            configuration.polarimetry = base_rss_polarimetry
        else:
            configuration.polarimetry = None

        xml = render_template(
            "rss_imaging.xml", configuration=configuration.model_dump()
        )

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
    def test_rss_imaging_filter(
        self, filter_name: str, expected_element: str, base_rss_imaging
    ):
        """Tests that RSS imaging filters are handled correctly when generating XML."""
        configuration = base_rss_imaging
        configuration.filter = filter_name

        xml = render_template(
            "rss_imaging.xml", configuration=configuration.model_dump()
        )
        assert expected_element in xml

        validate_xml(xml)
        assert True

    @pytest.mark.parametrize("full", [False, True])
    def test_rss_longslit_spectroscopy(
        self, full: bool, base_rss_longslit_spectroscopy, base_rss_polarimetry
    ):
        """Test that the template for RSS longslit spectroscopy generates valid XML."""
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

    @pytest.mark.parametrize("full", [False, True])
    def test_rss_mos_spectroscopy(
        self, full: bool, base_rss_multi_object_spectroscopy, base_rss_polarimetry
    ):
        """
        Test that the template for RSS multi-object spectroscopy generates valid XML.
        """
        configuration = base_rss_multi_object_spectroscopy

        if full:
            configuration.polarimetry = base_rss_polarimetry
        else:
            configuration.polarimetry = None

        xml = render_template(
            "rss_spectroscopy.xml", configuration=configuration.model_dump()
        )

        assert "MOS" in xml
        assert "Path" in xml

        if full:
            assert "BeamsplitterOrientation" in xml
        else:
            assert "BeamsplitterOrientation" not in xml

        validate_xml(xml)
        assert True

    @pytest.mark.parametrize("full", [False, True])
    def test_rss_slit_mask_ifu_spectroscopy(
        self, full: bool, base_rss_slit_mask_ifu_spectroscopy, base_rss_polarimetry
    ):
        """
        Test that the template for RSS slit mask IFY spectroscopy generates valid XML.
        """
        configuration = base_rss_slit_mask_ifu_spectroscopy

        if full:
            configuration.polarimetry = base_rss_polarimetry
        else:
            configuration.polarimetry = None

        xml = render_template(
            "rss_spectroscopy.xml", configuration=configuration.model_dump()
        )

        assert "SMI" in xml

        if full:
            assert "BeamsplitterOrientation" in xml
        else:
            assert "BeamsplitterOrientation" not in xml

        validate_xml(xml)
        assert True

    def test_rss_dithering_pattern(self, base_rss_dither_pattern):
        dither_pattern = base_rss_dither_pattern
        """Test that the template for RSS dither patterns generates valid XML."""

        xml = render_template(
            "rss_dither_pattern.xml", dither_pattern=dither_pattern.model_dump()
        )

        validate_xml(xml)

    @pytest.mark.parametrize("full", [False, True])
    def test_rss(
        self, full: bool, base_rss, base_rss_polarimetry, base_rss_longslit_spectroscopy
    ):
        """Test that the RSS template generates valid XML."""
        rss = base_rss
        rss.configuration = base_rss_longslit_spectroscopy

        if full:
            rss.configuration.polarimetry.wave_plate_pattern = (
                "circular"  # base_rss_polarimetry
            )
            rss.configuration.include_flat = True
            rss.configuration.include_arc = True
            rss.configuration.request_spectrophotometric_standard = True
        else:
            rss.configuration.polarimetry = None
            rss.configuration.include_flat = False
            rss.configuration.include_arc = False
            rss.configuration.request_spectrophotometric_standard = False

        xml = render_template("rss.xml", rss=rss.model_dump())

        if full:
            assert "RssProcedure" in xml
            assert "WaveplatePattern" in xml
            assert "RssDefaultCalibrationFlat" in xml
            assert "RssDefaultArc" in xml
            assert "RssStandard" in xml
        else:
            assert "RssProcedure" not in xml
            assert "WaveplatePattern" not in xml
            assert "RssDefaultCalibrationFlat" not in xml
            assert "RssDefaultArc" not in xml
            assert "RssStandard" not in xml

        validate_xml(xml)
        assert True

    def test_rss_wave_plate_pattern_step_values(
        self, base_rss, base_rss_longslit_spectroscopy, base_rss_polarimetry
    ):
        """Test that the wave plate pattern step values are correct."""
        rss = base_rss
        rss.configuration = base_rss_longslit_spectroscopy
        rss.configuration.polarimetry = base_rss_polarimetry
        rss.configuration.polarimetry.wave_plate_pattern = "circular"

        xml = render_template("rss.xml", rss=rss.model_dump())

        assert "<HWStation>0_0</HWStation>" in xml
        assert "<QWStation>4_45.00</QWStation>" in xml
        assert "<QWStation>28_315.00</QWStation>" in xml


class TestNirwalsTemplates:
    def test_nirwals_dither_pattern_step(self, base_nirwals_dither_pattern_step):
        """Test that the NIRWALS dither pattern step templates generates valid XML."""
        step = base_nirwals_dither_pattern_step

        xml = render_template("nirwals_dither_pattern_step.xml", step=step.model_dump())

        validate_xml(xml)
        assert True
