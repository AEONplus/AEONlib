import io
import logging

from pyastrosalt.session import Session
from pyastrosalt.submission import Submission, validate, submit

from aeonlib.conf import settings
from aeonlib.salt.models import Request

logger = logging.getLogger(__name__)


class SALTFacility:
    """
    SALT facility for validating and submitting SALT observation requests.

    By default, the facility is using the production server. For testing purposes you
    should call the facility constructor with the `use_playground` parameter set to
    `True`.
    """

    def __init__(self, use_playground: bool = False):
        self._session = Session()
        if use_playground:
            self._session.use_playground()
        username = settings.salt_username
        if not username:
            raise ValueError("salt_username is not set.")
        password = settings.salt_password
        if not password:
            raise ValueError("salt_password is not set.")
        self._session.login(username, password)

    def validate(self, request: Request) -> tuple[bool, list[str]]:
        """
        Send an observation request to the server for validation.

        The method waits for the validation request to complete and then returns a tuple
        with a boolean indicating whether the request is valid (`True`) or invalid
        (`False`) and the list of errors found by the validation.

        Parameters
        ----------
        request
            The observation request.

        Returns
        -------
        A tuple of a boolean indicating whether the request is valid and the list of
        errors.
        """
        logger.debug(f"Validating request:\n{request.model_dump()}")
        zip_content = io.BytesIO()
        request.export(zip_content)
        zip_content.seek(0)
        return validate(self._session, zip_content, request.proposal_code)

    def submit(self, request: Request) -> Submission:
        """
        Submit an observation request.

        The method returns a `pyastrosalt.submission.Submision` object, which you can
        use to follow the submission progress.

        Parameters
        ----------
        request
            The observation request.

        Returns
        -------
        A `pyastrosalt.submission.Submission` object.
        """
        logger.debug(f"Submitting request:\n{request.model_dump()}")
        zip_content = io.BytesIO()
        request.export(zip_content)
        zip_content.seek(0)
        return submit(self._session, zip_content, request.proposal_code)
