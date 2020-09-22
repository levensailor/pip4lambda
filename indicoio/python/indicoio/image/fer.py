from ..utils.api import api_handler
from ..utils.preprocessing import data_preprocess
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def fer(image, cloud=None, batch=False, api_key=None, version=None, **kwargs):
    """
    Given a grayscale input image of a face, returns a probability distribution over emotional state.
    Input should be in a list of list format, resizing will be attempted internally but for best
    performance, images should be already sized at 48x48 pixels..

    Example usage:

    .. code-block:: python

       >>> from indicoio import fer
       >>> import numpy as np
       >>> face = np.zeros((48,48)).tolist()
       >>> emotions = fer(face)
       >>> emotions
	   {u'Angry': 0.6340586827229989, u'Sad': 0.1764309536057839,
	   u'Neutral': 0.05582989039191157, u'Surprise': 0.0072685938275375344,
	   u'Fear': 0.08523385724298838, u'Happy': 0.04117802220878012}

    :param image: The image to be analyzed.
    :type image: list of lists
    :rtype: Dictionary containing emotion probability pairs
    """

    image = data_preprocess(
        image, batch=batch, size=None if kwargs.get("detect") else (48, 48)
    )

    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(image, cloud=cloud, api="fer", url_params=url_params, **kwargs)
