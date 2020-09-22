from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def text_tags(text, cloud=None, batch=False, api_key=None, version=None, **kwargs):
    """
    Given input text, returns a probability distribution over 100 document categories

    Example usage:

    .. code-block:: python

       >>> import indicoio
       >>> import numpy as np
       >>> text = 'Monday: Delightful with mostly sunny skies. Highs in the low 70s.'
       >>> possible = indicoio.classification(text)
       >>> category = possible.keys()[np.argmax(possible.values())]
       >>> probability = np.max(possible.values())
       >>> "Predicted category '%s' with probability %.4f"%(category,probability)
       u'Predicted 'Weather' with probability 0.8548'

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of class probability pairs
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(
        text, cloud=cloud, api="texttags", url_params=url_params, **kwargs
    )
