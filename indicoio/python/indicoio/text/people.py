from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def people(text, cloud=None, batch=None, api_key=None, version=2, **kwargs):
    """
    Given input text, returns references to specific persons found in the text

    Example usage:

    .. code-block:: python

       >>> text = "London Underground's boss Mike Brown warned that the strike ..."
       >>> entities = indicoio.people(text)
        [
          {
            u'text': "Mike Brown",
            u'confidence': 0.09470917284488678,
            u'position': [26, 36]
          },
          ...
        ]

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of language probability pairs
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(text, cloud=cloud, api="people", url_params=url_params, **kwargs)
