from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def personas(text, cloud=None, batch=False, api_key=None, version=None, **kwargs):
    """
    Given input text, returns the authors likelihood of being 16 different personality
    types in a dict.

    Example usage:

    .. code-block:: python

       >>> text = "I love going out with my friends"
       >>> entities = indicoio.personas(text)
       {'architect': 0.2191890478134155, 'logician': 0.0158474326133728,
        'commander': 0.07654544115066528 ...}

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: The authors 'Extraversion', 'Conscientiousness',
    'Openness', and 'Agreeableness' score (a float between 0 and 1) in a dictionary.
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    kwargs["persona"] = True
    return api_handler(
        text, cloud=cloud, api="personality", url_params=url_params, **kwargs
    )
