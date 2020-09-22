from ..utils.preprocessing import data_preprocess
from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def facial_localization(
    image, cloud=None, batch=False, api_key=None, version=None, **kwargs
):
    """
    Given an image, returns a list of faces found within the image.
    For each face, we return a dictionary containing the upper left corner and lower right corner.
    If crop is True, the cropped face is included in the dictionary.
    Input should be in a numpy ndarray or a filename.

    Example usage:

    .. code-block:: python

       >>> from indicoio import facial_localization
       >>> import numpy as np
       >>> img = np.zeros([image of a face])
       >>> faces = facial_localization(img)
       >>> len(faces)
       1

    :param image: The image to be analyzed.
    :type image: filepath or ndarray
    :rtype: List of faces (dict) found.
    """
    image = data_preprocess(image, batch=batch)
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(
        image, cloud=cloud, api="faciallocalization", url_params=url_params, **kwargs
    )
