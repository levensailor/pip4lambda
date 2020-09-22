from ..utils.api import api_handler


def object_detection(image_urls, api_key=None, version=1, **kwargs):
    """
    Given a pdf, returns the text and metadata associated with the given pdf.
    PDFs may be provided as base64 encoded data or as a filepath.
    Base64 image data and formatted table is optionally returned by setting
    `images=True` or `tables=True`.

    Example usage:

    .. code-block:: python

       >>> from indicoio import pdf_extraction
       >>> results = pdf_extraction(pdf_file)
       >>> results.keys()
       ['text', 'metadata']

    :param pdf: The pdf to be analyzed.
    :type pdf: str or list of strs
    :rtype: dict or list of dicts
    """
    results = api_handler(
        None,
        None,
        urls=image_urls,
        api="detect",
        method="api/detect",
        version=None,
        batch=None,
        **kwargs
    )

    return results
