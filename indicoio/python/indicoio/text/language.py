from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def language(text, cloud=None, batch=False, api_key=None, version=None, **kwargs):
    """
    Given input text, returns a probability distribution over 33 possible
    languages of what language the text was written in.

    Example usage:

    .. code-block:: python

       >>> import indicoio
       >>> import numpy as np
       >>> text = 'Monday: Delightful with mostly sunny skies. Highs in the low 70s.'
       >>> possible = indicoio.language(text)
       >>> language = possible.keys()[np.argmax(possible.values())]
       >>> probability = np.max(possible.values())
       >>> 'Predicted %s with probability %.4f'%(language,probability)
       u'Predicted English with probability 0.8548'

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of language probability pairs
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(
        text, cloud=cloud, api="language", url_params=url_params, **kwargs
    )
