from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def political(text, cloud=None, batch=False, api_key=None, version=2, **kwargs):
    """
    Given input text, returns a probability distribution over the political alignment of the speaker.

    Example usage:

    .. code-block:: python

       >>> from indicoio import political
       >>> import numpy as np
       >>> text = 'Wish we had more bike lanes. \
       Hopefully, driverless cars will chance economics from ownership to fee for service.'
       >>> affiliation = political(text)
       >>> affiliation
       {u'Libertarian': 0.4923755446986322, u'Green': 0.2974443102818122,
       u'Liberal': 0.13730032938784784, u'Conservative': 0.07287981563170784}
       >>> least_like = affiliation.keys()[np.argmin(affiliation.values())]
       >>> most_like = affiliation.keys()[np.argmax(affiliation.values())]
       >>> 'This text is most like %s and least like %s'%(most_like,least_like)
       u'This text is most like Libertarian and least like Conservative'

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of party probability pairs
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(
        text, cloud=cloud, api="political", url_params=url_params, **kwargs
    )
