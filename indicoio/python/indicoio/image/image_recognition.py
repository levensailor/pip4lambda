from ..utils.preprocessing import data_preprocess
from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def image_recognition(
    image, cloud=None, batch=False, api_key=None, version=None, **kwargs
):
    """
    Given an input image, returns a dictionary of image classifications with associated scores

    * Input can be either grayscale or rgb color and should either be a numpy array or nested list format.
    * Input data should be either uint8 0-255 range values or floating point between 0 and 1.
    * Large images (i.e. 1024x768+) are much bigger than needed, minaxis resizing will be done internally to 144 if needed.
    * For ideal performance, images should be square aspect ratio but non-square aspect ratios are supported as well.

    Example usage:

    .. code-block:: python

       >>> from indicoio import image_recognition
       >>> features = image_recognition(<filename>)

    :param image: The image to be analyzed.
    :type image: str
    :rtype: dict containing classifications
    """
    image = data_preprocess(image, batch=batch, size=144, min_axis=True)
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(
        image, cloud=cloud, api="imagerecognition", url_params=url_params, **kwargs
    )
