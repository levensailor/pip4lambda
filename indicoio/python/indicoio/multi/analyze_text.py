from .utils import multi, MULTIAPI_NOT_SUPPORTED
from ..text import TEXT_APIS
from ..utils.decorators import detect_batch_decorator

DEFAULT_APIS = list(set(TEXT_APIS.keys()) - set(MULTIAPI_NOT_SUPPORTED))


@detect_batch_decorator
def analyze_text(input_text, apis=DEFAULT_APIS, **kwargs):
    """
    Given input text, returns the results of specified text apis. Possible apis
    include: [ 'text_tags', 'political', 'sentiment', 'language' ]

    Example usage:

    .. code-block:: python

       >>> import indicoio
       >>> text = 'Monday: Delightful with mostly sunny skies. Highs in the low 70s.'
       >>> results = indicoio.analyze_text(data = text, apis = ["language", "sentiment"])
       >>> language_results = results["language"]
       >>> sentiment_results = results["sentiment"]

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
        data=input_text,
        datatype="text",
        cloud=cloud,
        batch=batch,
        api_key=api_key,
        apis=apis,
        accepted_apis=TEXT_APIS,
        **kwargs
    )
