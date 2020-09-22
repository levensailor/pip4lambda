from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def keywords(
    text, cloud=None, batch=False, api_key=None, version=2, batch_size=None, **kwargs
):
    """
    Given input text, returns series of keywords and associated scores

    Example usage:

    .. code-block:: python

       >>> import indicoio
       >>> import numpy as np
       >>> text = 'Monday: Delightful with mostly sunny skies. Highs in the low 70s.'
       >>> keywords = indicoio.keywords(text, top_n=3)
       >>> print "The keywords are: "+str(keywords.keys())
       u'The keywords are ['delightful', 'highs', 'skies']

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of feature score pairs
    """
    if kwargs.get("language", "english") != "english":
        version = 1
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(
        text,
        cloud=cloud,
        api="keywords",
        url_params=url_params,
        batch_size=batch_size,
        **kwargs
    )
