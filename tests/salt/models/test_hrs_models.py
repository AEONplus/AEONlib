from contextlib import nullcontext

import pytest

from aeonlib.salt.models import Hrs
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
    def test_default_prv_calibration(self, mode: HrsMode, prv_calibration, base_hrs):
        # Test that the default value for the precision radial velocity calibration is
        # correct.
        hrs = Hrs(
            num_cycles=base_hrs.num_cycles,
            mode=mode,
            fibre_separation=base_hrs.fibre_separation,
            blue_arm=base_hrs.blue_arm,
            red_arm=base_hrs.red_arm,
        )
        if prv_calibration is not None:
            assert hrs.prv_calibration == prv_calibration
        else:
            assert hrs.prv_calibration is None

    @pytest.mark.parametrize(
        "mode, prv_calibration_is_none",
        [
            ("low resolution", True),
            ("medium resolution", True),
            ("high resolution", True),
            ("high stability", False),
        ],
    )
    def test_allowed_prv_calibration_depends_on_mode(
        self, mode: HrsMode, prv_calibration_is_none, base_hrs
    ):
        # Test that the precision radial velocity calibration must be "ThAr" for the
        # high stability mode and None for all other modes.
        hrs_data = base_hrs.model_dump()
        del hrs_data["mode"]
        if "prv_calibration" in hrs_data:
            del hrs_data["prv_calibration"]
        if prv_calibration_is_none:
            with pytest.raises(ValueError):
                Hrs(**hrs_data, mode=mode, prv_calibration="ThAr")
            with nullcontext():
                Hrs(**hrs_data, mode=mode, prv_calibration=None)
        else:
            with nullcontext():
                Hrs(**hrs_data, mode=mode, prv_calibration="ThAr")
            with pytest.raises(ValueError):
                Hrs(**hrs_data, mode=mode, prv_calibration=None)


class TestHrsDetector:
    def test_hrs_detector(self, base_hrs_detector):
        # Test that HRS detector setups can be built.
        assert True
