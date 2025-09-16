import json
from typing import Annotated, Union

import pytest
from astropy import units as u
from astropy.units import Quantity
from pydantic import BaseModel

from aeonlib.salt.models.types.quantity import AstropyQuantityTypeAnnotation

Wavelength = Annotated[
    Union[Quantity, float], AstropyQuantityTypeAnnotation(u.Angstrom)
]

ProperMotion = Annotated[
    Union[Quantity, float], AstropyQuantityTypeAnnotation(u.arcsec / u.year)
]


class CelestialObject(BaseModel):
    peak_wavelength: Wavelength
    proper_motion: ProperMotion


class TestAstropyQuantityTypeAnnotation:
    @pytest.mark.parametrize(
        "peak_wavelength, proper_motion",
        [
            # 1 year = 8766 hours
            (4107 * u.Angstrom, 4383 * u.arcsec / u.year),
            (410.7 * u.nm, 0.5 * u.arcsec / u.hour),
        ],
    )
    def test_from_quantity(self, peak_wavelength, proper_motion):
        """
        Test objects constructed from astropy Quantity objects dump to json as floats
        """
        asteroid = CelestialObject(
            peak_wavelength=peak_wavelength, proper_motion=proper_motion
        )
        dumped = asteroid.model_dump_json()
        assert pytest.approx(json.loads(dumped)) == {
            "peak_wavelength": 4107.0,
            "proper_motion": 4383.0,
        }

    def test_from_float(self):
        """Test objects constructed from floats dump to json as floats"""
        t = CelestialObject(peak_wavelength=7567.6, proper_motion=0.98)
        dumped = t.model_dump_json()
        assert pytest.approx(json.loads(dumped)) == {
            "peak_wavelength": 7567.6,
            "proper_motion": 0.98,
        }

    @pytest.mark.parametrize(
        "peak_wavelength, proper_motion",
        [
            # 1 year = 8766 hours
            (4107 * u.Angstrom, 4383 * u.arcsec / u.year),
            (410.7 * u.nm, 0.5 * u.arcsec / u.hour),
        ],
    )
    def test_quantity_attributes(self, peak_wavelength, proper_motion):
        """Test quantities are accessible on the model"""
        asteroid = CelestialObject(
            peak_wavelength=peak_wavelength, proper_motion=proper_motion
        )
        assert isinstance(asteroid.peak_wavelength, Quantity)
        assert pytest.approx(asteroid.peak_wavelength.value) == 4107
        assert asteroid.peak_wavelength.unit == u.Angstrom
        assert pytest.approx(asteroid.proper_motion.value) == 4383.0
        assert asteroid.proper_motion.unit == u.arcsec / u.year

    def test_from_json(self):
        """Test models can be constructed from json"""
        target_json = json.dumps(
            {
                "peak_wavelength": "5516.89",
                "proper_motion": "0.076",
            }
        )
        target = CelestialObject.model_validate_json(target_json)
        assert isinstance(target.peak_wavelength, Quantity)
        assert pytest.approx(target.peak_wavelength.value) == 5516.89
        assert target.peak_wavelength.unit == u.Angstrom
        assert isinstance(target.proper_motion, Quantity)
        assert pytest.approx(target.proper_motion.value) == 0.076
        assert target.proper_motion.unit == u.arcsec / u.year
