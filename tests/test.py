"""
API testing module
"""
# pylint: disable=missing-function-docstring
from unittest import TestCase, main
from pathlib import Path
from requests import post


unittests_path = Path(__file__).parent
API_URL = str(r"http://localhost:8888/load")

class TestAPI(TestCase):
    """
    Class defining test cases for API
    """

    def test_successful_file_upload(self):
        with open(unittests_path / "Test_PDF.pdf", "rb") as file:
            result = post(url = API_URL,  files={'file': file})
        self.assertEqual(result.status_code,200)


    def test_invalid_header_content_type(self):
        with open(unittests_path / "Test_PDF.pdf", "rb") as file:
            result = post(url = API_URL,  files={'file': file},\
                 headers = {"Content-Type": "application/json"})

        self.assertEqual(result.reason,\
            "Invalid header Content-Type application/json. multipart/form-data is expected.")
        self.assertEqual(result.status_code,406)


    def test_invalid_body_wrong_key(self):
        with open(unittests_path / "Test_PDF.pdf", "rb") as file:
            result = post(url = API_URL,  files={'invalid_body_content': file})
        self.assertEqual(result.reason,\
            "Invalid body structure. A dict with 'file' key is expected.")
        self.assertEqual(result.status_code,406)


    def test_invalid_body_multiple_key(self):
        with open(unittests_path / "Test_PDF.pdf", "rb") as file:
            result = post(url = API_URL,  files={'file': file, 'another_file': file})
        self.assertEqual(result.reason,"Invalid body structure. Only one file is allowed.")
        self.assertEqual(result.status_code,406)


    def test_not_pdf_file(self):
        with open(unittests_path / "Test_TXT.txt", "rb") as file:
            result = post(url = API_URL,  files={'file': file})
        self.assertEqual(result.reason,\
            "Invalid file format %txt, pdf required.")
        self.assertEqual(result.status_code,406)


    def test_invalid_filename(self):
        with open(unittests_path / "Test_PDF_too_long.pdf", "rb") as file:
            result = post(url = API_URL,  files={'file': file})
        self.assertEqual(result.reason,\
            "File name shall be less than 20 char.")
        self.assertEqual(result.status_code,406)


if __name__ == "__main__":
    main()
