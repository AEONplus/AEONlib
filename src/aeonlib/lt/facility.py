import time
from logging import getLogger

from astropy.coordinates import Angle
from lxml import etree
from suds.client import Client

from aeonlib.conf import settings
from aeonlib.lt.models import LT_INSTRUMENTS, LTObservation
from aeonlib.models import SiderealTarget, Window

LT_XML_NS = "http://www.rtml.org/v3.1a"
LT_XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
LT_SCHEMA_LOCATION = (
    "http://www.rtml.org/v3.1a http://telescope.livjm.ac.uk/rtml/RTML-nightly.xsd"
)

logger = getLogger(__name__)


class LTFacility:
    def __init__(self):
        headers = {
            "Username": settings.lt_username,
            "Password": settings.lt_password,
        }
        url = "{0}://{1}:{2}/node_agent2/node_agent?wsdl".format(
            "http", settings.lt_host, settings.lt_port
        )
        self.client = Client(url, headers=headers)

    def validate_observation(self, observation_payload: str) -> bool:
        validate_payload = etree.fromstring(observation_payload)
        # Change the payload to an inquiry mode document to test connectivity
        validate_payload.set("mode", "inquiry")
        try:
            response = self.client.service.handle_rtml(validate_payload).replace(
                'encoding="ISO-8859-1"', ""
            )
        except Exception:
            logger.exception("Error while connection to Liverpool Telescope")
            return False

        response_rtml = etree.fromstring(response)
        if response_rtml.get("mode") == "offer":
            return True
        elif response_rtml.get("mode") == "reject":
            logger.error("Error with RTML submission to Liverpool Telescope")

        return False

    def observation_payload(
        self,
        instrument: LT_INSTRUMENTS,
        target: SiderealTarget,
        window: Window,
        obs: LTObservation,
    ) -> str:
        payload = self.prolog()
        project = self.build_project("TEST-PROJECT")
        payload.append(project)
        schedules = instrument.build_inst_schedule()
        for schedule in schedules:
            schedule.append(self.build_target(target))
            for const in self.build_constraints(obs, window):
                schedule.append(const)
            payload.append(schedule)

        return etree.tostring(payload, encoding="unicode")

    def prolog(self) -> etree._Element:
        namespaces = {"xsi": LT_XSI_NS}
        schemaLocation = str(etree.QName(LT_XSI_NS, "schemaLocation"))
        uid = format(int(time.time()))

        return etree.Element(
            "RTML",
            {schemaLocation: LT_SCHEMA_LOCATION},
            xmlns=LT_XML_NS,
            mode="request",
            uid=uid,
            version="3.1a",
            nsmap=namespaces,
        )

    def build_project(self, project_id: str) -> etree._Element:
        project = etree.Element("Project", ProjectId=project_id)
        contact = etree.SubElement(project, "Contact")
        etree.SubElement(contact, "Username").text = settings.lt_username
        etree.SubElement(contact, "Name").text = ""

        return project

    def build_target(self, aeon_target: SiderealTarget) -> etree._Element:
        target = etree.Element("Target", name=aeon_target.name)
        coordinates = etree.SubElement(target, "Coordinates")
        etree.SubElement(coordinates, "Equinox").text = str(aeon_target.epoch)

        ra = etree.SubElement(coordinates, "RightAscension")
        assert isinstance(aeon_target.ra, Angle)
        etree.SubElement(ra, "Hours").text = str(aeon_target.ra.hms.h)
        etree.SubElement(ra, "Minutes").text = str(aeon_target.ra.hms.m)
        etree.SubElement(ra, "Seconds").text = str(aeon_target.ra.hms.s)

        dec = etree.SubElement(coordinates, "Declination")
        assert isinstance(aeon_target.dec, Angle)
        sign = "+" if aeon_target.dec.signed_dms.sign == 1.0 else "-"
        etree.SubElement(dec, "Degrees").text = sign + str(
            int(aeon_target.dec.signed_dms.d)
        )
        etree.SubElement(dec, "Arcminutes").text = str(
            int(aeon_target.dec.signed_dms.m)
        )
        etree.SubElement(dec, "Arcseconds").text = str(aeon_target.dec.signed_dms.s)

        return target

    def build_constraints(
        self, lt_observation: LTObservation, window: Window
    ) -> list[etree._Element]:
        airmass_const = etree.Element(
            "AirmassConstraint", maximum=str(lt_observation.max_airmass)
        )

        sky_const = etree.Element("SkyConstraint")
        etree.SubElement(sky_const, "Flux").text = str(lt_observation.max_skybrightness)
        etree.SubElement(sky_const, "Units").text = "magnitudes/square-arcsecond"

        seeing_const = etree.Element(
            "SeeingConstraint",
            maximum=str(lt_observation.max_seeing),
            units="arcseconds",
        )

        photom_const = etree.Element("ExtinctionConstraint")
        if lt_observation.photometric:
            etree.SubElement(photom_const, "Photometric").text = "clear"
        else:
            etree.SubElement(photom_const, "Photometric").text = "light"

        date_const = etree.Element("DateTimeConstraint", type="include")
        assert window.start
        start = window.start.strftime("%Y-%m-%dT%H:%M:00+00:00")
        end = window.end.strftime("%Y-%m-%dT%H:%M:00+00:00")
        etree.SubElement(date_const, "DateTimeStart", system="UT", value=str(start))
        etree.SubElement(date_const, "DateTimeEnd", system="UT", value=str(end))

        return [airmass_const, sky_const, seeing_const, photom_const, date_const]
