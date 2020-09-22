from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def organizations(text, cloud=None, batch=None, api_key=None, version=2, **kwargs):
    """
    Given input text, returns references to specific organizations found in the text

    Example usage:

    .. code-block:: python

       >>> text = "London Underground's boss Mike Brown warned that the strike ..."
       >>> entities = indicoio.organizations(text)
        [
          {
            u'text': "London Underground",
            u'confidence': 0.8643872141838074,
            u'position': [0, 18]
          }
        ]

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of language probability pairs
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(
        text, cloud=cloud, api="organizations", url_params=url_params, **kwargs
    )
