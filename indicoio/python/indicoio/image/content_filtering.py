from ..utils.api import api_handler
from ..utils.preprocessing import data_preprocess
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def content_filtering(
    image, cloud=None, batch=False, api_key=None, version=None, **kwargs
):
    """
    Given a grayscale input image, returns how obcene the image is.
    Input should be in a list of list format.

    Example usage:

    .. code-block:: python

       >>> from indicoio import content_filtering
       >>> import numpy as np
       >>> face = np.zeros((48,48)).tolist()
       >>> res = content_filtering(face)
       >>> res
	   .056

    :param image: The image to be analyzed.
    :type image: list of lists
    :rtype: float of nsfwness
    """
    image = data_preprocess(image, batch=batch, size=128, min_axis=True)
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(
        image, cloud=cloud, api="contentfiltering", url_params=url_params, **kwargs
    )
