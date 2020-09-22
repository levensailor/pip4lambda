from ..utils.preprocessing import data_preprocess
from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def image_features(image, cloud=None, batch=False, api_key=None, version=3, **kwargs):
    """
    Given an input image, returns a 2048 dimensional sparse feature vector explaining that image.
    Useful as a form of feature engineering for image oriented tasks.

    * Input can be either grayscale or rgb color and should either be a numpy array or nested list format.
    * Input data should be either uint8 0-255 range values or floating point between 0 and 1.
    * Large images (i.e. 1024x768+) are much bigger than needed, resizing will be done internally to 144x144 if needed.
    * For ideal performance, images should be square aspect ratio but non-square aspect ratios are supported as well.

    Example usage:

    .. code-block:: python

       >>> from indicoio import image_features
       >>> import numpy as np
       >>> image = np.zeros((144,144,3))
       >>> features = image_features(image)
       >>> len(features),np.min(features),np.max(features),np.sum(np.asarray(f)!=0)
       (2048, 0.0, 6.97088623046875, 571)

    Since the image features returned are a semantic description of the contents of an image they can be used
    to implement many other common image related tasks such as object recognition or image similarity and retrieval.

    For image similarity, simple distance metrics applied to collections of image feature vectors can work very well.

    :param image: The image to be analyzed.
    :type image: numpy.ndarray
    :rtype: List containing features
    """
    image = data_preprocess(image, batch=batch, size=512, min_axis=True)
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(
        image, cloud=cloud, api="imagefeatures", url_params=url_params, **kwargs
    )
