from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def text_features(text, cloud=None, batch=False, api_key=None, version=None, **kwargs):
    """
    Given input text, returns a numeric feature vector that represents the content.

    Example usage:

    .. code-block:: python

       >>> from indicoio import text_features
       >>> text_features("Queen of England")
       [0.04509247093572533, -0.052756784338865576, ...]

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: List of floats which represents the content of the input text
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    kwargs["synonyms"] = False
    return api_handler(
        text, cloud=cloud, api="textfeatures", url_params=url_params, **kwargs
    )
