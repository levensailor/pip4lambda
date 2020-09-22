import sys
import base64
from base64 import b64encode, b64decode
import traceback
import os

try:
    from StringIO import StringIO
except:
    from io import BytesIO

from PIL import Image
from six import string_types


def pdf_preprocess(pdf, batch=False):
    """
    Load pdfs from local filepath if not already b64 encoded
    """
    if batch:
        return [pdf_preprocess(doc, batch=False) for doc in pdf]

    if os.path.isfile(pdf):
        # a filepath is provided, read and encode
        return b64encode(open(pdf, "rb").read())
    else:
        # assume pdf is already b64 encoded
        return pdf


def postprocess_image(image):
    raw_data = image.get("data")

    try:
        if (2, 6) <= sys.version_info < (3, 0):
            data = b64decode(raw_data)
            return Image.open(StringIO(data))
        elif sys.version_info >= (3, 0):
            if not isinstance(raw_data, bytes):
                raw_data = bytes(raw_data, "utf-8")
            data = base64.decodestring(raw_data)
            return Image.open(BytesIO(data))
        else:
            raise AssertionError(
                "Unsupport python version: {version}".format(
                    version=str(sys.version_info)
                )
            )
    except IOError:
        traceback.print_exc()
        return None


def postprocess_images(images):
    images = [postprocess_image(image) for image in images]
    images = [image for image in images if image]  # remove Nones
    return images
