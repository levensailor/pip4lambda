from ..utils.preprocessing import data_preprocess
from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def facial_features(
    image, cloud=None, batch=False, api_key=None, version=None, **kwargs
):
    """
    Given an grayscale input image of a face, returns a 48 dimensional feature vector explaining that face.
    Useful as a form of feature engineering for face oriented tasks.
    Input should be in a list of list format, resizing will be attempted internally but for best
    performance, images should be already sized at 48x48 pixels.

    Example usage:

    .. code-block:: python

       >>> from indicoio import facial_features
       >>> import numpy as np
       >>> face = np.zeros((48,48))
       >>> features = facial_features(face)
       >>> len(features)
       48

    :param image: The image to be analyzed.
    :type image: list of lists
    :rtype: List containing feature responses
    """
    image = data_preprocess(
        image, batch=batch, size=None if kwargs.get("detect") else (48, 48)
    )
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(
        image, cloud=cloud, api="facialfeatures", url_params=url_params, **kwargs
    )
