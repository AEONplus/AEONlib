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


class LTException(Exception):
    pass


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

    def submit_observation(self, observation_payload: etree._Element) -> str:
        return self._send_payload(observation_payload)

    def validate_observation(self, observation_payload: etree._Element) -> str:
        # Change the payload to an inquiry mode document to test connectivity
        observation_payload.set("mode", "inquiry")

        return self._send_payload(observation_payload)

    def cancel_observation(self, uid: str, project_id: str) -> str:
        cancel_payload = self._prolog(mode="abort", uid=uid)
        project = self._build_project(project_id)
        cancel_payload.append(project)

        return self._send_payload(cancel_payload)

    def observation_payload(
        self,
        instrument: LT_INSTRUMENTS,
        target: SiderealTarget,
        window: Window,
        obs: LTObservation,
    ) -> etree._Element:
        uid = "aeon_" + format(int(time.time()))
        payload = self._prolog(mode="request", uid=uid)
        project = self._build_project(obs.project)
        payload.append(project)
        schedules = instrument.build_inst_schedule()
        for schedule in schedules:
            schedule.append(self._build_target(target))
            for const in self._build_constraints(obs, window):
                schedule.append(const)
            payload.append(schedule)

        return payload

    def _send_payload(self, payload: etree._Element) -> str:
        str_payload = etree.tostring(payload, encoding="unicode", pretty_print=True)
        try:
            response = self.client.service.handle_rtml(str_payload).replace(
                'encoding="ISO-8859-1"', ""
            )
        except Exception as e:
            logger.exception("Error while connection to Liverpool Telescope")
            raise LTException(e)

        response_rtml = etree.fromstring(response)
        if response_rtml.get("mode") in ["offer", "confirm"]:
            return response_rtml.get("uid", "")
        elif response_rtml.get("mode") == "reject":
            logger.error(
                "Error with RTML submission to Liverpool Telescope: %s", response
            )
            raise LTException(response)
        else:
            logger.error("Unexpected mode response: %s", response_rtml.get("mode"))
            raise LTException()

    def _prolog(self, mode: str, uid: str) -> etree._Element:
        namespaces = {"xsi": LT_XSI_NS}
        schemaLocation = str(etree.QName(LT_XSI_NS, "schemaLocation"))

        return etree.Element(
            "RTML",
            {schemaLocation: LT_SCHEMA_LOCATION},
            xmlns=LT_XML_NS,
            mode=mode,
            uid=uid,
            version="3.1a",
            nsmap=namespaces,
        )

    def _build_project(self, project_id: str) -> etree._Element:
        project = etree.Element("Project", ProjectID=project_id)
        contact = etree.SubElement(project, "Contact")
        etree.SubElement(contact, "Username").text = settings.lt_username
        etree.SubElement(contact, "Name").text = ""
        etree.SubElement(contact, "Communication")

        return project

    def _build_target(self, aeon_target: SiderealTarget) -> etree._Element:
        target = etree.Element("Target", name=aeon_target.name)
        coordinates = etree.SubElement(target, "Coordinates")
        etree.SubElement(coordinates, "Equinox").text = str(aeon_target.epoch)

        ra = etree.SubElement(coordinates, "RightAscension")
        assert isinstance(aeon_target.ra, Angle)
        etree.SubElement(ra, "Hours").text = str(int(aeon_target.ra.hms.h))
        etree.SubElement(ra, "Minutes").text = str(int(aeon_target.ra.hms.m))
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

    def _build_constraints(
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
            etree.SubElement(photom_const, "Clouds").text = "clear"
        else:
            etree.SubElement(photom_const, "Clouds").text = "light"

        date_const = etree.Element("DateTimeConstraint", type="include")
        assert window.start
        start = window.start.strftime("%Y-%m-%dT%H:%M:00+00:00")
        end = window.end.strftime("%Y-%m-%dT%H:%M:00+00:00")
        etree.SubElement(date_const, "DateTimeStart", system="UT", value=str(start))
        etree.SubElement(date_const, "DateTimeEnd", system="UT", value=str(end))

        return [airmass_const, sky_const, seeing_const, photom_const, date_const]
