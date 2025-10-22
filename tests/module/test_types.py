import json
import math
from datetime import datetime
from typing import Annotated, Union

import pytest
from astropy.coordinates import Angle
from astropy.time import Time
from astropy import units as u
from astropy.units import Quantity
from pydantic import BaseModel, ValidationError

import aeonlib.types


class Window(BaseModel):
    """
    A window of time similar to ocs.request_models.Window
    used for testing the custom time type
    """

    start: aeonlib.types.Time | None = None
    end: aeonlib.types.Time


Wavelength = Annotated[
    Union[Quantity, float], aeonlib.types.AstropyQuantityTypeAnnotation(u.Angstrom)
]


ProperMotion = Annotated[
    Union[Quantity, float],
    aeonlib.types.AstropyQuantityTypeAnnotation(u.arcsec / u.year),
]


class CelestialObject(BaseModel):
    peak_wavelength: Wavelength
    proper_motion: ProperMotion


class TestAstropyTime:
    def test_with_astropy_time(self):
        """
        Test that the window constructed with astropy Times has datetimes when dumped
        """
        window = Window(
            start=Time(60775.0, scale="utc", format="mjd"),
            end=Time(60776.0, scale="utc", format="mjd"),
        )
        assert window.model_dump()["start"] == datetime(2025, 4, 10, 0, 0, 0, 0)
        assert window.model_dump()["end"] == datetime(2025, 4, 11, 0, 0, 0, 0)

    def test_with_astropy_time_json(self):
        """
        Test that the window constructed with astropy Times dumps to JSON properly
        """
        window = Window(
            start=Time(60775.0, scale="utc", format="mjd"),
            end=Time(60776.0, scale="utc", format="mjd"),
        )
        as_json = json.loads(window.model_dump_json())
        assert as_json["start"] == "2025-04-10T00:00:00"
        assert as_json["end"] == "2025-04-11T00:00:00"

    def test_from_datetime(self):
        """
        Test that we can construct windows using datetimes instead of astropy Times
        """
        window = Window(
            start=datetime(2025, 4, 10, 0, 0, 0, 0),
            end=datetime(2025, 4, 11, 0, 0, 0, 0),
        )
        assert window.model_dump()["start"] == datetime(2025, 4, 10, 0, 0, 0, 0)
        assert window.model_dump()["end"] == datetime(2025, 4, 11, 0, 0, 0, 0)

    def test_from_datetime_json(self):
        """
        Test that the window constructed with datetimes dumps to JSON properly
        """
        window = Window(
            start=datetime(2025, 4, 10, 0, 0, 0, 0),
            end=datetime(2025, 4, 11, 0, 0, 0, 0),
        )
        as_json = json.loads(window.model_dump_json())
        assert as_json["start"] == "2025-04-10T00:00:00"
        assert as_json["end"] == "2025-04-11T00:00:00"

    def test_from_json(self):
        """
        Test that windows can be parsed from JSON and the resulting object contains
        astropy Time objects
        """
        window_json = json.dumps(
            {
                "start": "2025-04-10T00:00:00",
                "end": "2025-04-11T00:00:00",
            }
        )
        window = Window.model_validate_json(window_json)
        assert isinstance(window.start, Time)
        assert window.start == Time(datetime(2025, 4, 10, 0, 0, 0, 0))
        assert isinstance(window.end, Time)
        assert window.end == Time(datetime(2025, 4, 11, 0, 0, 0, 0))


class Target(BaseModel):
    """
    Test model for testing custom angle type
    """

    ra: aeonlib.types.Angle
    dec: aeonlib.types.Angle


class TestAstropyAngle:
    def test_from_angle(self):
        """Test angles constructed from astropy Angle objects dump to json as strings"""
        t = Target(ra=Angle(10, unit="deg"), dec=Angle(20, unit="deg"))
        dumped = t.model_dump_json()
        assert dumped == '{"ra":10.0,"dec":20.0}'

    def test_from_quantity(self):
        """
        Test angles constructed from astropy Quantity objects dump to json as formatted
        strings
        """
        t = Target(ra=10.5 * u.deg, dec=20 * (math.pi / 180) * u.rad)
        dumped = t.model_dump_json()
        assert dumped == '{"ra":10.5,"dec":20.0}'

    def test_quantity_conversion(self):
        """
        Test angles constructed from astropy Quantity objects are converted to a
        corresponding AstroPy Angle object
        """
        t = Target(ra=40 * u.deg, dec=-76.8 * (math.pi / 180) * u.rad)
        assert isinstance(t.ra, Angle)
        assert pytest.approx(t.ra.to(u.deg).value) == 40
        assert pytest.approx(t.dec.to(u.deg).value) == -76.8
        assert isinstance(t.dec, Angle)

    def test_from_str(self):
        """Test angles constructed from strings dump to json as formatted strings"""
        t = Target(ra="1h0m0s", dec="2d")
        dumped = t.model_dump_json()
        parsed = json.loads(dumped)
        assert parsed["ra"] == pytest.approx(15)
        assert parsed["dec"] == 2.0

    def test_from_float(self):
        """Test angles constructed from floats dump to json as formatted strings"""
        t = Target(ra=10.5, dec=20)
        dumped = t.model_dump_json()
        assert dumped == '{"ra":10.5,"dec":20.0}'

    def test_angle_attributes(self):
        """Test angles are accessible on the model"""
        t = Target(ra="1h", dec="2d")
        assert isinstance(t.ra, Angle)
        assert t.ra.hour == 1
        assert isinstance(t.dec, Angle)
        assert t.dec.degree == 2

    def test_from_json(self):
        """Test models can be constructed from json"""
        target_json = json.dumps(
            {
                "ra": "1h",
                "dec": "2d",
            }
        )
        target = Target.model_validate_json(target_json)
        assert isinstance(target.ra, Angle)
        assert target.ra.hour == 1
        assert isinstance(target.dec, Angle)
        assert target.dec.degree == 2

    def test_from_json_float(self):
        """Test models can be constructed from json with float values"""
        target_json = json.dumps(
            {
                "ra": 10.0,
                "dec": 20.0,
            }
        )
        target = Target.model_validate_json(target_json)
        assert isinstance(target.ra, Angle)
        assert target.ra.degree == 10
        assert isinstance(target.dec, Angle)
        assert target.dec.degree == 20


class MjdObject(BaseModel):
    time: aeonlib.types.TimeMJD


class TestTimeMJD:
    def test_from_jd_float(self):
        obj = MjdObject(time=2460826.5)
        assert isinstance(obj.time, Time)
        assert obj.time.to_datetime() == datetime(2025, 5, 31)

    def test_from_mjd_float(self):
        obj = MjdObject(time=60826.0)
        assert isinstance(obj.time, Time)
        assert obj.time.to_datetime() == datetime(2025, 5, 31)

    def test_from_json_float(self):
        target_json = json.dumps(
            {
                "time": 60826.0,
            }
        )
        target = MjdObject.model_validate_json(target_json)
        assert isinstance(target.time, Time)
        assert target.time.to_datetime() == datetime(2025, 5, 31)

    def test_outputs_mjd(self):
        obj = MjdObject(time=datetime(2025, 5, 31))
        dumped = obj.model_dump_json()
        assert dumped == '{"time":60826.0}'

    def test_from_datetime(self):
        obj = MjdObject(time=datetime(2025, 5, 5))
        assert isinstance(obj.time, Time)
        assert obj.time.scale == "tt"
        assert obj.time.mjd == 60800.0


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

    def test_rejects_incorrect_unit(self):
        with pytest.raises(ValidationError, match="peak_wavelength"):
            CelestialObject(
                peak_wavelength=5000 * u.hour, proper_motion=1.0 * u.arcsec / u.year
            )
