from contextlib import nullcontext
from typing import Any

import astropy.coordinates
import pytest
from pydantic import ValidationError

from aeonlib.salt.models import Block, Acquisition
from aeonlib.salt.models.block_models import ReferenceStar
from aeonlib.salt.models.util import render_template, validate_xml


class TestBlock:
    def test_block(self, base_block):
        """Test that a simple block can be built."""
        assert True

    @pytest.mark.parametrize(
        "num_visits, max_num_visits, expectation",
        [
            (7, None, nullcontext()),
            (7, 8, nullcontext()),
            (7, 7, nullcontext()),
            (7, 6, pytest.raises(ValidationError, match="greater than")),
        ],
    )
    def test_max_visits_and_visits(
        self, num_visits, max_num_visits, expectation, base_block
    ):
        """
        Test that the maximum number of visits must not be less than the number of
        visits.
        """
        block = base_block

        with expectation:
            block.num_visits = num_visits
            block.max_num_visits = max_num_visits

        assert True

    def test_salticam(self, base_block, base_salticam):
        """Test that Salticam as a block instrument is handled correctly."""
        block = base_block
        block.instrument = base_salticam

        xml = render_template("block.xml", block=block.model_dump())

        assert "<Salticam>" in xml

        validate_xml(xml)
        assert True

    def test_rss(self, base_block, base_rss):
        """Test that RSS as a block instrument is handled correctly."""
        block = base_block
        block.instrument = base_rss

        xml = render_template("block.xml", block=block.model_dump())

        assert "<Rss>" in xml

        validate_xml(xml)
        assert True

    def test_hrs(self, base_block, base_hrs):
        """Test that HRS as a block instrument is handled correctly."""
        block = base_block
        block.instrument = base_hrs

        xml = render_template("block.xml", block=block.model_dump())

        assert "<Hrs>" in xml

        validate_xml(xml)
        assert True

    def test_nirwals(self, base_block, base_nirwals):
        """Test that RSS as a block instrument is handled correctly."""
        block = base_block
        block.instrument = base_nirwals

        xml = render_template("block.xml", block=block.model_dump())

        assert "<Nir>" in xml

        validate_xml(xml)
        assert True


class TestConstraints:
    def test_constraints(self, base_constraints):
        """Test that constraints can be built."""
        assert True


class TestAcquisition:
    def test_acquisition(self, base_acquisition):
        """Test that acquisitions can be built."""
        assert True

    @pytest.mark.parametrize(
        "position_angle, do_not_flip, expected",
        [
            (45, True, nullcontext()),
            (-34, False, nullcontext()),
            (124, None, pytest.raises(ValueError)),
            ("parallactic", True, nullcontext()),
            ("parallactic", False, nullcontext()),
            ("parallactic", None, nullcontext()),
            (None, True, nullcontext()),
            (None, False, nullcontext()),
            (None, None, nullcontext()),
        ],
    )
    def test_do_not_flip_position_angle(
        self, position_angle: Any, do_not_flip: bool | None, expected, base_acquisition
    ):
        """
        Test that the do_not_flip_position_angle field must be True or False if the
        position angle value is an actual angle (rather than "parallactic" or None) and
        must be None otherwise.
        """
        a = base_acquisition
        with expected:
            Acquisition(
                finder_charts=a.finder_charts,
                filter=a.filter,
                exposure_time=a.exposure_time,
                reference_star=a.reference_star,
                position_angle=position_angle,
                do_not_flip_position_angle=do_not_flip,
                include_focused_image=a.include_focused_image,
            )

    @pytest.mark.parametrize(
        "position_angle, do_not_flip",
        [(63, False), ("parallactic", None), (None, None)],
    )
    def test_default_do_not_flip_position_angle(
        self, position_angle: Any, do_not_flip: bool | None, base_acquisition
    ):
        """
        Test that the default value for the do_not_flip_position_angle field is correct.
        """
        a = base_acquisition
        acquisition = Acquisition(
            finder_charts=a.finder_charts,
            filter=a.filter,
            exposure_time=a.exposure_time,
            reference_star=a.reference_star,
            position_angle=position_angle,
            include_focused_image=a.include_focused_image,
        )
        if do_not_flip is not None:
            assert acquisition.do_not_flip_position_angle == do_not_flip
        else:
            assert acquisition.do_not_flip_position_angle is None


class TestReferenceStar:
    def test_reference_star(self, base_reference_star):
        """Test that reference stars can be built."""
        assert True

    @pytest.mark.parametrize(
        "dec, expectation",
        [
            (astropy.coordinates.Angle("-76.001d"), pytest.raises(ValueError)),
            (astropy.coordinates.Angle("-76d"), nullcontext()),
            (astropy.coordinates.Angle("11d"), nullcontext()),
            (astropy.coordinates.Angle("11.0001d"), pytest.raises(ValueError)),
        ],
    )
    def test_dec_range(self, dec, expectation, base_reference_star):
        ref_star = base_reference_star.model_dump()
        ref_star["dec"] = dec
        with expectation:
            ReferenceStar(**ref_star)  # type: ignore
