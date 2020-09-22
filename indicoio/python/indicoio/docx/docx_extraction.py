from ..utils.docx import docx_preprocess
from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def docx_extraction(
    docx, cloud=None, batch=False, api_key=None, version=None, **kwargs
):
    """
    Given a .docx file, returns the raw text associated with the given .docx file.
    The .docx file may be provided as base64 encoded data or as a filepath.

    Example usage:

    .. code-block:: python

       >>> from indicoio import docx_extraction
       >>> results = docx_extraction(docx_file)

    :param docx: The docx to be analyzed.
    :type docx: str or list of strs
    :rtype: dict or list of dicts
    """
    docx = docx_preprocess(docx, batch=batch)
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    results = api_handler(
        docx, cloud=cloud, api="docxextraction", url_params=url_params, **kwargs
    )
    return results
