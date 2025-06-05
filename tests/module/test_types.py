import json
from datetime import datetime

import pytest
from astropy.coordinates import Angle
from astropy.time import Time
from pydantic import BaseModel

import aeonlib.types


class Window(BaseModel):
    """
    A window of time similar to ocs.request_models.Window
    used for testing the custom time type
    """

    start: aeonlib.types.Time | None = None
    end: aeonlib.types.Time


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
