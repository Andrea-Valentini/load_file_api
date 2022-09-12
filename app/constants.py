"""
Constant definition
"""
from pathlib import Path
from enum import Enum
from os import environ

APP_PATH = Path(__file__).parent
CLOUDMERSIVE_API_KEY = environ["CLOUDMERSIVE_API_KEY"]

class FormatFile(Enum):
    """
    List of file formats
    """
    PDF = "%PDF"
    WORD = "DOCFILE0"
