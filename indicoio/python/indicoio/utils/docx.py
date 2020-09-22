from base64 import b64encode, b64decode
import os


def docx_preprocess(docx, batch=False):
    """
    Load docx files from local filepath if not already b64 encoded
    """
    if batch:
        return [docx_preprocess(doc, batch=False) for doc in docx]

    if os.path.isfile(docx):
        # a filepath is provided, read and encode
        return b64encode(open(docx, "rb").read())
    else:
        # assume doc is already b64 encoded
        return docx
