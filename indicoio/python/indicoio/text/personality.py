from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def personality(text, cloud=None, batch=False, api_key=None, version=None, **kwargs):
    """
    Given input text, returns the authors 'Extraversion', 'Conscientiousness',
    'Openness', and 'Agreeableness' score (a float between 0 and 1) in a dictionary.

    Example usage:

    .. code-block:: python

       >>> text = "I love going out with my friends"
       >>> entities = indicoio.personality(text)
       {'Extraversion': 0.69691890478134155, 'Conscientiousness': 0.4658474326133728,
        'Openness': 0.42654544115066528, 'Agreeableness': 0.7414245903}

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: The authors 'Extraversion', 'Conscientiousness',
    'Openness', and 'Agreeableness' score (a float between 0 and 1) in a dictionary.
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(
        text, cloud=cloud, api="personality", url_params=url_params, **kwargs
    )
