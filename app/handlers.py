"""
Tornado Handlers definition
"""
# pylint: disable=import-error
from json import dumps
from datetime import date
from tornado.web import RequestHandler, HTTPError
from tornado.httputil import HTTPHeaders
from objects import Metadata
from constants import FormatFile


class LoadHandler(RequestHandler): # pylint: disable=abstract-method
    """
    Loads pdf files and store metadata in the database.
    """

    def get_db(self):
        """
        Allows the handler to retrieve the database object.

        Returns:
            {Database}
        """
        return self.settings["database"]

    def get_scanner(self):
        """
        Allows the handler to retrieve the scanner object.

        Returns:
            {Scanner}: object providing methods to perform the files sanity check
        """
        return self.settings["scanner"]

    def validate_request(self, header:HTTPHeaders, body: dict):
        """
        Validates the HTTP request format.

        Args:
            header {HTTPHeaders}: HTTPHeaders object from tornado.httputil
            body {dict}: request content

        Raises:
            HTTPError: if the header content-type is not "multipart/form-data"
            HTTPError: if the body does not have the "file" key
            HTTPError: if the body has more than one key

        """
        content_type = header.get("Content-Type")
        if "multipart/form-data" not in content_type:
            raise HTTPError(status_code = 406,
                reason = f"Invalid header Content-Type {content_type}. " +
                 "multipart/form-data is expected.")

        if "file" not in body.keys():
            raise HTTPError(status_code = 406,\
                reason = "Invalid body structure. A dict with 'file' key is expected.")

        if len(body.keys()) > 1 :
            raise HTTPError(status_code = 406,\
                reason = "Invalid body structure. Only one file is allowed.")


    def validate_file(self, filename:str, filebody:str):
        """
        Validates the file format and performs the sanity check.

        Args:
            filename {str}
            filebody {str}: file content

        Raises:
            HTTPError: if the file is not a pdf
            HTTPError: if the sanity check fail
            HTTPError: if filename is too long
        """
        # Checking file format
        expected_format = FormatFile.PDF.value
        value_utf8 = filebody.decode("utf-8")
        if expected_format != str(value_utf8)[:len(expected_format)]:
            raise HTTPError(status_code = 406,\
                reason = f"Invalid file format {value_utf8}, pdf required.")

        # Sanity check
        scanner = self.get_scanner()
        if not scanner.scan_file_for_virus(filebody):
            raise HTTPError(status_code = 406,\
                reason = "A virus have been found in the file!")

        if len(filename) > 20:
            raise HTTPError(status_code = 406,\
                reason = "File name shall be less than 20 char.")

    def post(self):
        """
        Loads handler API endpoint
        """
        self.validate_request(header = self.request.headers,
                                 body = self.request.files)

        filename = self.request.files["file"][0]["filename"]
        filebody = self.request.files["file"][0]["body"]

        self.validate_file(filename = filename, filebody = filebody)

        database = self.get_db()

        database.update_db(
            Metadata(
                filename=filename,
                upload_date=date.today().strftime("%Y-%m-%d"),
            ))

    def write_error(self, status_code:int , **kwargs):
        """
        Sends messages if an exception is raised

        Args:
            status_code {int}: HTTP error code
        """
        self.finish(dumps({
                'error': {
                    'code': status_code,
                    'message': self._reason,
                }
            }))
