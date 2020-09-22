from .utils import multi, MULTIAPI_NOT_SUPPORTED
from ..image import IMAGE_APIS
from ..utils.preprocessing import data_preprocess
from ..utils.decorators import detect_batch_decorator

DEFAULT_APIS = list(set(IMAGE_APIS.keys()) - set(MULTIAPI_NOT_SUPPORTED))


@detect_batch_decorator
def analyze_image(image, apis=DEFAULT_APIS, **kwargs):
    """
    Given input image, returns the results of specified image apis. Possible apis
    include: ['fer', 'facial_features', 'image_features']

    Example usage:

    .. code-block:: python

       >>> import indicoio
       >>> import numpy as np
       >>> face = np.zeros((48,48)).tolist()
       >>> results = indicoio.analyze_image(image = face, apis = ["fer", "facial_features"])
       >>> fer = results["fer"]
       >>> facial_features = results["facial_features"]

    :param text: The text to be analyzed.
    :param apis: List of apis to use.
    :type text: str or unicode
    :type apis: list of str
    :rtype: Dictionary of api responses
    """
    cloud = kwargs.pop("cloud", None)
    batch = kwargs.pop("batch", False)
    api_key = kwargs.pop("api_key", None)

    return multi(
        data=data_preprocess(image, batch=batch),
        datatype="image",
        cloud=cloud,
        batch=batch,
        api_key=api_key,
        apis=apis,
        accepted_apis=IMAGE_APIS,
        **kwargs
    )
