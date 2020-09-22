from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def sentiment(text, cloud=None, batch=False, api_key=None, version=None, **kwargs):
    """
    Given input text, returns a scalar estimate of the sentiment of that text.
    Values are roughly in the range 0 to 1 with 0.5 indicating neutral sentiment.
    For reference, 0 suggests very negative sentiment and 1 suggests very positive sentiment.

    Example usage:

    .. code-block:: python

       >>> from indicoio import sentiment
       >>> text = 'Thanks everyone for the birthday wishes!! It was a crazy few days ><'
       >>> sentiment = sentiment(text)
       >>> sentiment
       0.6946439339979863

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Float
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(
        text, cloud=cloud, api="sentiment", url_params=url_params, **kwargs
    )
