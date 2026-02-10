import pytest

from aeonlib.salt.models.types import HrsMode


class TestHrs:
    def test_hrs(self, base_hrs):
        # Test that HRS configurations can be built.
        assert True

    @pytest.mark.parametrize(
        "mode, prv_calibration",
        [
            ("low resolution", None),
            ("medium resolution", None),
            ("high resolution", None),
            ("high stability", "ThAr"),
        ],
    )
    def test_prv_calibration(self, mode: HrsMode, prv_calibration, base_hrs):
        # Test that the default value for the precision radial velocity calibration is
        # correct.
        hrs = base_hrs
        hrs.mode = mode

        if prv_calibration is not None:
            assert hrs.prv_calibration == prv_calibration
        else:
            assert hrs.prv_calibration is None


class TestHrsDetector:
    def test_hrs_detector(self, base_hrs_detector):
        # Test that HRS detector setups can be built.
        assert True
