import time
from logging import getLogger

from lxml import etree
from suds.client import Client

from aeonlib.conf import settings

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

    def observation_payload(self) -> str:
        payload = self.prolog()
        payload.append(self.build_project("TEST-PROJECT"))

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
