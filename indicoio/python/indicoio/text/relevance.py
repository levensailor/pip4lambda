from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def relevance(
    data, queries, cloud=None, batch=False, api_key=None, version=None, **kwargs
):
    """
    Given input text and a list of query terms / phrases, returns how relevant the query is
    to the input text.

    Example usage:

    .. code-block:: python

       >>> import indicoio
       >>> text = 'On Monday, president Barack Obama will be giving his keynote address at...'
       >>> relevance = indicoio.relevance(text, queries=['president'])
       >>> print "Relevance: " + str(relevance[0])
       u'Relevance: [0.44755361996336784]'

    :param text: The text to be analyzed.
    :param queries: a list of terms or phrases to measure similarity against
    :type text: str or unicode
    :rtype: Dictionary of feature score pairs
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    kwargs["queries"] = queries
    kwargs["synonyms"] = False
    return api_handler(
        data, cloud=cloud, api="relevance", url_params=url_params, **kwargs
    )
