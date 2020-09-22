from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def places(text, cloud=None, batch=None, api_key=None, version=2, **kwargs):
    """
    Given input text, returns references to specific places found in the text

    Example usage:

    .. code-block:: python

       >>> text = "London Underground's boss Mike Brown warned that the strike ..."
       >>> entities = indicoio.places(text)
        [
          {
            u'text': "London",
            u'confidence': 0.18549786508083344,
            u'position': [0, 6]
          },
          ...
        ]

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of language probability pairs
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(text, cloud=cloud, api="places", url_params=url_params, **kwargs)
