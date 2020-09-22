from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def emotion(text, cloud=None, batch=False, api_key=None, version=None, **kwargs):
    """
    Given input text, returns a probability distribution over 5 possible
    emotions of what language the text was written in.

    Example usage:

    .. code-block:: python

       >>> import indicoio
       >>> import numpy as np
       >>> text = "I did it. I got into Grad School. Not just any program, but a GREAT program. :-)"
       >>> possible = indicoio.emotion(text)
       >>> emotion = possible.keys()[np.argmax(possible.values())]
       >>> probability = np.max(possible.values())
       >>> 'Predicted `%s` with probability %.4f' % (emotion, probability)
       u'Predicted `joy` with probability 0.7744'

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of emotion probability pairs
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(
        text, cloud=cloud, api="emotion", url_params=url_params, **kwargs
    )
