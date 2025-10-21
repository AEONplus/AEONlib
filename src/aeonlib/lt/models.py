# pyright: reportPrivateUsage=false
from typing import Annotated, Literal

from annotated_types import Ge, Le
from lxml import etree
from pydantic import BaseModel


class LTConfig(BaseModel):
    """Some LT specific parameters, this could probably be replaced with the
    Constraints class for the main models"""

    project: str
    max_airmass: Annotated[float, Ge(1.0), Le(3.0)] = 2.0
    max_seeing: Annotated[float, Ge(1.0), Le(5.0)] = 1.2
    max_skybrightness: Annotated[float, Ge(0.0), Le(10.0)] = 1.0
    photometric: Literal["clear", "light"] = "clear"


IooFilterTimeCnt = tuple[Annotated[float, Ge(0.0)], Annotated[int, Ge(1)]]
"""Tuple of exposure time, exposure count"""


class Ioo(BaseModel):
    binning: Literal["1x1", "2x2"] = "2x2"
    U: IooFilterTimeCnt = (120.0, 1)
    R: IooFilterTimeCnt = (120.0, 1)
    G: IooFilterTimeCnt = (120.0, 1)
    I: IooFilterTimeCnt = (120.0, 1)  # noqa: E741
    Z: IooFilterTimeCnt = (120.0, 1)
    B: IooFilterTimeCnt = (120.0, 1)
    V: IooFilterTimeCnt = (120.0, 1)
    Halpha6566: IooFilterTimeCnt = (120.0, 1)
    Halpha6634: IooFilterTimeCnt = (120.0, 1)
    Halpha6705: IooFilterTimeCnt = (120.0, 1)
    Halpha6755: IooFilterTimeCnt = (120.0, 1)
    Halpha6822: IooFilterTimeCnt = (120.0, 1)

    def build_inst_schedule(self) -> list[etree._Element]:
        filters = self.model_dump(exclude={"binning"}).items()

        return [self.build_schedule(filter, cfg) for filter, cfg in filters]

    def build_schedule(self, filter: str, cfg: IooFilterTimeCnt) -> etree._Element:
        schedule = etree.Element("Schedule")
        device = etree.SubElement(schedule, "Device", name="IO:O", type="camera")
        etree.SubElement(device, "SpectralRegion").text = "optical"
        setup = etree.SubElement(device, "Setup")
        _ = etree.SubElement(setup, "Filter", type=filter)
        detector = etree.SubElement(setup, "Detector")
        binning = etree.SubElement(detector, "Binning")
        etree.SubElement(binning, "X", units="pixels").text = self.binning.split("x")[0]
        etree.SubElement(binning, "Y", units="pixels").text = self.binning.split("x")[1]
        exposure = etree.SubElement(schedule, "Exposure", count=str(cfg[1]))
        etree.SubElement(exposure, "Value", units="seconds").text = str(cfg[0])

        return schedule


class Sprat(BaseModel):
    exp_time: Annotated[float, Ge(0.0)] = 120.0
    exp_count: Annotated[int, Ge(1)] = 1
    grating: Literal["red", "blue"] = "red"

    def build_inst_schedule(self) -> list[etree._Element]:
        schedule = etree.Element("Schedule")
        device = etree.SubElement(schedule, "Device", name="Sprat", type="spectrograph")
        etree.SubElement(device, "SpectralRegion").text = "optical"
        setup = etree.SubElement(device, "Setup")
        _ = etree.SubElement(setup, "Grating", name=self.grating)
        detector = etree.SubElement(setup, "Detector")
        binning = etree.SubElement(detector, "Binning")
        etree.SubElement(binning, "X", units="pixels").text = "1"
        etree.SubElement(binning, "Y", units="pixels").text = "1"
        exposure = etree.SubElement(schedule, "Exposure", count=str(self.exp_count))
        etree.SubElement(exposure, "Value", units="seconds").text = str(self.exp_time)

        return [schedule]


class Frodo(BaseModel):
    exp_time_blue: Annotated[float, Ge(0.0)] = 120.0
    exp_count_blue: Annotated[int, Ge(0)] = 1
    res_blue: Literal["high", "low"] = "low"
    exp_time_red: Annotated[float, Ge(0.0)] = 120.0
    exp_count_red: Annotated[int, Ge(0)] = 1
    res_red: Literal["high", "low"] = "low"

    def build_inst_schedule(self) -> list[etree._Element]:
        return [
            self.build_schedule(
                "FrodoSpec-Blue", self.res_blue, self.exp_count_blue, self.exp_time_blue
            ),
            self.build_schedule(
                "FrodoSpec-Red", self.res_red, self.exp_count_red, self.exp_time_red
            ),
        ]

    def build_schedule(
        self, device_name: str, grating: str, exp_count: int, exp_time: float
    ) -> etree._Element:
        schedule = etree.Element("Schedule")
        device = etree.SubElement(
            schedule, "Device", name=device_name, type="spectrograph"
        )
        etree.SubElement(device, "SpectralRegion").text = "optical"
        setup = etree.SubElement(device, "Setup")
        _ = etree.SubElement(setup, "Grating", name=grating)
        exposure = etree.SubElement(schedule, "Exposure", count=str(exp_count))
        etree.SubElement(exposure, "Value", units="seconds").text = str(exp_time)

        return schedule


LT_INSTRUMENTS = Ioo | Frodo | Sprat
