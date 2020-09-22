import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..utils.errors import IndicoError
from ..utils.decorators import detect_batch_decorator

MULTIAPI_NOT_SUPPORTED = ["relevance"]

EXECUTOR = ThreadPoolExecutor(max_workers=4)


def multi(data, datatype, apis, accepted_apis, batch=False, **kwargs):
    """
    Helper to make multi requests of different types.

    :param data: Data to be sent in API request
    :param datatype: String type of API request
    :param apis: List of apis to use.
    :param batch: Is this a batch request?
    :rtype: Dictionary of api responses
    """
    # Client side api name checking - strictly only accept func name api
    invalid_apis = [
        api for api in apis if api not in accepted_apis or api in MULTIAPI_NOT_SUPPORTED
    ]
    if invalid_apis:
        raise IndicoError(
            "The following are not valid %s APIs: %s. Please reference the available APIs below:\n%s"
            % (datatype, ", ".join(invalid_apis), ", ".join(accepted_apis.keys()))
        )

    # Convert client api names to server names before sending request
    cloud = kwargs.pop("cloud", None)
    api_key = kwargs.pop("api_key", None)

    api_results_executor = {}
    for api in apis:
        api_results_executor[
            EXECUTOR.submit(
                accepted_apis[api],
                data,
                cloud=cloud,
                api_key=api_key,
                batch=batch,
                **kwargs
            )
        ] = api

    api_results = {}
    for future in concurrent.futures.as_completed(api_results_executor):
        api_results[api_results_executor[future]] = future.result()

    return api_results
