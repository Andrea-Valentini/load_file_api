"""
Objects file

Provides various objects
"""
# pylint: disable=import-error
from os import path, remove
from dataclasses import dataclass
from cloudmersive_virus_api_client.rest import ApiException
from cloudmersive_virus_api_client import Configuration, ScanApi, ApiClient
from constants import APP_PATH, CLOUDMERSIVE_API_KEY


@dataclass
class Metadata:
    """
    Metadata class

    Defines data structure
    """

    filename: str
    upload_date: str


class Scanner:
    """
    Scanner class

    Provides methods to perform the file sanity check via the Cloudmersive API service.
    """

    def __init__(self):

        self.configuration = Configuration()
        self.configuration.api_key['Apikey'] = CLOUDMERSIVE_API_KEY
        self.api_instance = ScanApi(ApiClient(self.configuration))
        self.scanned_file_path = APP_PATH / 'file_to_scan.pdf'

    def scan_file_for_virus(self, file: bytes) -> bool:
        """
        Performs the sanity check of the file.
        It sends the file to Cloudmersive and wait for a succesfull return.

        Args:
            file {bytes}: file to scan

        Returns:
            sanity_check {bool}: True if the file is harmless, False otherwise.
        """
        try:

            self.save_file(file)
            api_response = self.api_instance.scan_file(self.scanned_file_path)

        except ApiException as error:
            print(f"Exception when calling ScanApi->scan_file: {error}")

        finally:
            self.clean()
        return api_response._clean_result #pylint: disable=W0212

    def save_file(self, file: bytes):
        """
        Save file in local path.

        This step is needed to provide a valid filepath to scan_file_for_virus() 

        Args:
            file {bytes}: file to scan
        """
        with open(self.scanned_file_path, 'wb') as f:
            f.write(file)

    def clean(self):
        """
        Remove the saved file.

        Args:
            file {bytes}: scanned file
        """
        if path.exists(self.scanned_file_path):
            remove(self.scanned_file_path)
