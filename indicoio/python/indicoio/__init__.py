from functools import wraps, partial
import warnings


Version, version, __version__, VERSION = ("1.4.1",) * 4

JSON_HEADERS = {
    "Content-type": "application/json",
    "Accept": "application/json",
    "client-lib": "python",
    "version-number": VERSION,
}

from .text import *
from .image import *
from .multi import *
from .pdf import *
from .docx import *
from .detection import *

from indicoio.utils.errors import (
    IndicoError,
    InvalidAPIKey,
    MissingAPIKey,
    MalformattedData,
    BatchProcessingError,
    APIDoesNotExist,
)
