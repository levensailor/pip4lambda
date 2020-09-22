from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def summarization(text, cloud=None, batch=False, api_key=None, version=1, **kwargs):
    """
    Given input text, returns a `top_n` length sentence summary.

    Example usage:

    .. code-block:: python

       >>> from indicoio import summarization
       >>> summary = summarization("https://en.wikipedia.org/wiki/Yahoo!_data_breach")
       >>> summary
       ["This information was disclosed two years later on September 22, 2016.", "[1] The data breach is one of the largest in the history of the Internet.", "Specific details of material taken include names, email addresses, telephone numbers, dates of birth, and encrypted passwords.", "[2]\\n\\nEvents [ edit ]\\n\\nYahoo alleged in its statement that the breach was carried out by \\"state-sponsored\\" hackers,[3] but the organization did not name any country.", "We had our own use for it and other buyers did as well."]

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of party probability pairs
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(
        text, cloud=cloud, api="summarization", url_params=url_params, **kwargs
    )
