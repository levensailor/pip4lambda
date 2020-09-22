import time
import sys

from ..utils.api import api_handler
from ..utils.decorators import detect_batch
from ..utils.preprocessing import data_preprocess
from ..utils.errors import IndicoError


def _unpack_list(example):
    """
    Input data format standardization
    """
    try:
        x = example[0]
        y = example[1]
        meta = None
        return x, y, meta
    except IndexError:
        raise IndicoError(
            "Invalid input data.  Please ensure input data is "
            "formatted as a list of `[data, target]` pairs."
        )


def _unpack_dict(example, target=None):
    """
    Input data format standardization
    """
    if target is None:
        try:
            x = example["data"]
            y = example["target"]
            meta = example.get("metadata", {})
            return x, y, meta
        except KeyError:
            raise IndicoError(
                "Invalid input data.  Please ensure input data is "
                "formatted as a list of dicts with `data` and `target` keys. "
                "A `metadata` key may optionally be included."
            )
    else:
        # multi-field input
        y = example.pop(target, None)
        x = example
        meta = {}
        return x, y, meta


def _unpack_data(data, target=None):
    """
    Break Xs, Ys, and metadata out into separate lists for data preprocessing.
    Run basic data validation.
    """
    xs = [None] * len(data)
    ys = [None] * len(data)
    metadata = [None] * len(data)
    for idx, example in enumerate(data):
        if isinstance(example, (list, tuple)):
            xs[idx], ys[idx], metadata[idx] = _unpack_list(example)
        if isinstance(example, dict):
            xs[idx], ys[idx], metadata[idx] = _unpack_dict(example, target=target)

    return xs, ys, metadata


def _pack_data(X, Y, metadata, target=None):
    """
    After modifying / preprocessing inputs,
    reformat the data in preparation for JSON serialization
    """
    if target is None:
        if not any(metadata):
            # legacy list of list format is acceptable
            return list(zip(X, Y))

        else:
            # newer dictionary-based format is required in order to save metadata
            return [
                {"data": x, "target": y, "metadata": meta}
                for x, y, meta in zip(X, Y, metadata)
            ]
    else:
        # multi-field input
        for i in range(len(X)):
            assert isinstance(X[i], dict)
            X[i][target] = Y[i]
        return X


def visualize_explanation(explanation, label=None):
    """
    Given the output of the explain() endpoint, produces a terminal visual that plots response strength over a sequence
    """
    if not sys.version_info[:2] >= (3, 5):
        raise IndicoError("Python >= 3.5+ is required for explanation visualization")

    try:
        from colr import Colr as C
    except ImportError:
        raise IndicoError(
            "Package colr >= 0.8.1 is required for explanation visualization."
        )

    cursor = 0
    text = explanation["text"]
    for token in explanation.get("token_predictions"):
        try:
            class_confidence = token.get("prediction")[label]
        except KeyError:
            raise IndicoError("Invalid label: {}".format(label))

        if class_confidence > 0.5:
            fg_color = (255, 255, 255)
        else:
            fg_color = (0, 0, 0)
        rg_value = 255 - int(class_confidence * 255)
        token_end = token.get("token").get("end")
        token_text = text[cursor:token_end]
        cursor = token_end
        sys.stdout.write(
            str(
                C()
                .b_rgb(rg_value, rg_value, 255)
                .rgb(fg_color[0], fg_color[1], fg_color[2], token_text)
            )
        )
    sys.stdout.write("\n")
    sys.stdout.flush()


class Collection(object):
    def __init__(self, collection, *args, **kwargs):
        self.keywords = {
            "domain": kwargs.get("domain"),
            "shared": kwargs.get("shared"),
            "collection": collection,
        }

    def _api_handler(self, *args, **kwargs):
        """
        Thin wrapper around api_handler from `indicoio.utils.api` to add in stored keyword argument to the JSON body
        """
        keyword_arguments = {}
        keyword_arguments.update(self.keywords)
        keyword_arguments.update(kwargs)
        return api_handler(*args, **keyword_arguments)

    def add_data(
        self, data, cloud=None, batch=False, api_key=None, version=None, **kwargs
    ):
        """
        This is the basic training endpoint. Given a piece of text and a score, either categorical
        or numeric, this endpoint will train a new model given the additional piece of information.

        Inputs
        data - List: The text and collection/score associated with it. The length of the text (string) should ideally
          be longer than 100 characters and contain at least 10 words. While the API will support
          shorter text, you will find that the accuracy of results improves significantly with longer
          examples. For an additional fee, this end point will support image input as well. The collection/score
          can be a string or float. This is the variable associated with the text. This can either be categorical
          (the tag associated with the post) or numeric (the number of Facebook shares the post
          received). However it can only be one or another within a given label.
        domain (optional) - String: This is an identifier that helps determine the appropriate techniques for indico
          to use behind the scenes to train your model.  One of {"standard", "topics"}.
        api_key (optional) - String: Your API key, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        cloud (optional) - String: Your private cloud domain, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        """
        if not len(data):
            raise IndicoError("No input data provided.")
        batch = isinstance(data[0], (list, tuple, dict))

        # standarize format for preprocessing batch of examples
        if not batch:
            data = [data]

        target = kwargs.get("target")
        X, Y, metadata = _unpack_data(data, target=target)
        X = data_preprocess(X, batch=True)
        data = _pack_data(X, Y, metadata, target=target)

        # if a single example was passed in, unpack
        if not batch:
            data = data[0]

        url_params = {
            "batch": batch,
            "api_key": api_key,
            "version": version,
            "method": "add_data",
        }
        return self._api_handler(
            data, cloud=cloud, api="custom", url_params=url_params, **kwargs
        )

    def train(self, cloud=None, batch=False, api_key=None, version=None, **kwargs):
        """
        This is the basic training endpoint. Given an existing dataset this endpoint will train a model.

        Inputs
        api_key (optional) - String: Your API key, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        cloud (optional) - String: Your private cloud domain, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        """
        url_params = {
            "batch": batch,
            "api_key": api_key,
            "version": version,
            "method": "train",
        }
        return self._api_handler(
            self.keywords["collection"],
            cloud=cloud,
            api="custom",
            url_params=url_params,
            **kwargs
        )

    def predict(
        self, data, cloud=None, batch=False, api_key=None, version=None, **kwargs
    ):
        """
        This is the prediction endpoint. This will be the primary interaction point for all predictive
        analysis.

        Inputs
        data - String: The text example being provided to the API. As a general rule, the data should be as
          similar to the examples given to the train function (above) as possible. Because language
          in different domains is used very differently the accuracy will generally drop as the
          difference between this text and the training text increases. Base64 encoded image data, image urls, and
          text content are all valid.
        domain (optional) - String: This is an identifier that helps determine the appropriate techniques for indico
          to use behind the scenes to train your model.  One of {"standard", "topics"}.
        api_key (optional) - String: Your API key, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        cloud (optional) - String: Your private cloud domain, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        """
        batch = detect_batch(data)
        data = data_preprocess(data, batch=batch)
        url_params = {"batch": batch, "api_key": api_key, "version": version}
        return self._api_handler(
            data, cloud=cloud, api="custom", url_params=url_params, **kwargs
        )

    def explain(
        self, data, cloud=None, batch=False, api_key=None, version=None, **kwargs
    ):
        """
        This is the explain endpoint. This allows for predictions that also include information
        about the training data that led to the models decision.

        Inputs
        data - String: The text example being provided to the API. As a general rule, the data should be as
          similar to the examples given to the train function (above) as possible. Because language
          in different domains is used very differently the accuracy will generally drop as the
          difference between this text and the training text increases. Base64 encoded image data, image urls, and
          text content are all valid.
        domain (optional) - String: This is an identifier that helps determine the appropriate techniques for indico
          to use behind the scenes to train your model.  One of {"standard", "topics"}.
        api_key (optional) - String: Your API key, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        cloud (optional) - String: Your private cloud domain, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        """
        batch = detect_batch(data)
        data = data_preprocess(data, batch=batch)
        url_params = {
            "batch": batch,
            "api_key": api_key,
            "version": version,
            "method": "explain",
        }
        return self._api_handler(
            data, cloud=cloud, api="custom", url_params=url_params, **kwargs
        )

    def clear(self, cloud=None, api_key=None, version=None, **kwargs):
        """
        This is an API made to remove all of the data associated from a given colletion. If there's been a data
        corruption issue, or a large amount of incorrect data has been fed into the API it is often difficult
        to correct. This allows you to clear a colletion and start from scratch. Use with caution! This is not
        reversible.

        Inputs
        api_key (optional) - String: Your API key, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        cloud (optional) - String: Your private cloud domain, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        """
        url_params = {
            "batch": False,
            "api_key": api_key,
            "version": version,
            "method": "clear_collection",
        }
        return self._api_handler(
            None, cloud=cloud, api="custom", url_params=url_params, **kwargs
        )

    def info(self, cloud=None, api_key=None, version=None, **kwargs):
        """
        Return the current state of the model associated with a given collection
        """
        url_params = {
            "batch": False,
            "api_key": api_key,
            "version": version,
            "method": "info",
        }
        return self._api_handler(
            None, cloud=cloud, api="custom", url_params=url_params, **kwargs
        )

    def remove_example(
        self, data, cloud=None, batch=False, api_key=None, version=None, **kwargs
    ):
        """
        This is an API made to remove a single instance of training data. This is useful in cases where a
        single instance of content has been modified, but the remaining examples remain valid. For
        example, if a piece of content has been retagged.

        Inputs
        data - String: The exact text you wish to remove from the given collection. If the string
          provided does not match a known piece of text then this will fail. Again, this is required if
          an id is not provided, and vice-versa.
        api_key (optional) - String: Your API key, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        cloud (optional) - String: Your private cloud domain, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        """
        batch = detect_batch(data)
        data = data_preprocess(data, batch=batch)
        url_params = {
            "batch": batch,
            "api_key": api_key,
            "version": version,
            "method": "remove_example",
        }
        return self._api_handler(
            data, cloud=cloud, api="custom", url_params=url_params, **kwargs
        )

    def wait(self, interval=1, timeout=None, **kwargs):
        """
        Block until the collection's model is completed training
        """
        start = time.time()
        while True:
            status = self.info(**kwargs).get("status")
            if timeout and time.time() - start > timeout:
                break
            if status == "ready":
                break
            if status != "training":
                raise IndicoError("Collection status failed with: {0}".format(status))
            time.sleep(interval)

    def register(
        self, make_public=False, cloud=None, api_key=None, version=None, **kwargs
    ):
        """
        This API endpoint allows you to register you collection in order to share read or write
        access to the collection with another user.

        Inputs:
        api_key (optional) - String: Your API key, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        cloud (optional) - String: Your private cloud domain, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        make_public (optional) - Boolean: When True, this option gives all indico users read access to your model.
        """
        kwargs["make_public"] = make_public
        url_params = {
            "batch": False,
            "api_key": api_key,
            "version": version,
            "method": "register",
        }
        return self._api_handler(
            None, cloud=cloud, api="custom", url_params=url_params, **kwargs
        )

    def deregister(self, cloud=None, api_key=None, version=None, **kwargs):
        """
        If you've shared access to your collection in the past, and now want to revoke all other user's access
        to your collection, simply deregister your collection.

        Inputs:
        api_key (optional) - String: Your API key, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        cloud (optional) - String: Your private cloud domain, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        """
        url_params = {
            "batch": False,
            "api_key": api_key,
            "version": version,
            "method": "deregister",
        }
        return self._api_handler(
            None, cloud=cloud, api="custom", url_params=url_params, **kwargs
        )

    def authorize(
        self,
        email,
        permission_type="read",
        cloud=None,
        api_key=None,
        version=None,
        **kwargs
    ):
        """
        This API endpoint allows you to authorize another user to access your model in a read or write capacity.
        Before calling authorize, you must first make sure your model has been registered.

        Inputs:
        email - String: The email of the user you would like to share access with.
        permission_type (optional) - String: One of ['read', 'write'].  Users with read permissions can only call `predict`.
          Users with `write` permissions can add new input examples and train models.
        api_key (optional) - String: Your API key, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        cloud (optional) - String: Your private cloud domain, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        """
        kwargs["permission_type"] = permission_type
        kwargs["email"] = email
        url_params = {
            "batch": False,
            "api_key": api_key,
            "version": version,
            "method": "authorize",
        }
        return self._api_handler(
            None, cloud=cloud, api="custom", url_params=url_params, **kwargs
        )

    def deauthorize(self, email, cloud=None, api_key=None, version=None, **kwargs):
        """
        This API endpoint allows you to remove another user's access to your collection.

        Inputs:
        email - String: The email of the user you would like to share access with.
        api_key (optional) - String: Your API key, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        cloud (optional) - String: Your private cloud domain, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        """
        kwargs["email"] = email
        url_params = {
            "batch": False,
            "api_key": api_key,
            "version": version,
            "method": "deauthorize",
        }
        return self._api_handler(
            None, cloud=cloud, api="custom", url_params=url_params, **kwargs
        )

    def rename(self, name, cloud=None, api_key=None, version=None, **kwargs):
        """
        If you'd like to change the name you use to access a given collection, you can call the rename endpoint.
        This is especially useful if the name you use for your model is not available for registration.

        Inputs:
        name - String: The new name used to access your model.
        api_key (optional) - String: Your API key, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        cloud (optional) - String: Your private cloud domain, required only if the key has not been declared
          elsewhere. This allows the API to recognize a request as yours and automatically route it
          to the appropriate destination.
        """
        kwargs["name"] = name
        url_params = {
            "batch": False,
            "api_key": api_key,
            "version": version,
            "method": "rename",
        }
        result = self._api_handler(
            None, cloud=cloud, api="custom", url_params=url_params, **kwargs
        )
        self.keywords["collection"] = name
        return result


def collections(cloud=None, api_key=None, version=None, **kwargs):
    """
    This is a status report endpoint. It is used to get the status on all of the collections currently trained, as
    well as some basic statistics on their accuracies.

    Inputs
    api_key (optional) - String: Your API key, required only if the key has not been declared
      elsewhere. This allows the API to recognize a request as yours and automatically route it
      to the appropriate destination.
    cloud (optional) - String: Your private cloud domain, required only if the key has not been declared
      elsewhere. This allows the API to recognize a request as yours and automatically route it
      to the appropriate destination.

    Example usage:

      .. code-block:: python

         >>> collections = indicoio.collections()
        {
          "tag_predictor": {
            "input_type": "text",
            "model_type": "classification",
            "number_of_samples": 224
            'status': 'ready'
          }, "popularity_predictor": {
            "input_type": "text",
            "model_type": "regression",
            "number_of_samples": 231
            'status': 'training'
          }
        }
      }
    """
    url_params = {
        "batch": False,
        "api_key": api_key,
        "version": version,
        "method": "collections",
    }
    return api_handler(None, cloud=cloud, api="custom", url_params=url_params, **kwargs)


def vectorize(data, cloud=None, api_key=None, version=None, **kwargs):
    """
    Support for raw features from the custom collections API
    """
    batch = detect_batch(data)
    data = data_preprocess(data, batch=batch)
    url_params = {
        "batch": batch,
        "api_key": api_key,
        "version": version,
        "method": "vectorize",
    }
    return api_handler(data, cloud=cloud, api="custom", url_params=url_params, **kwargs)


class FinetuneCollection(Collection):
    def __init__(self, collection, **kwargs):
        self.keywords = {
            "shared": kwargs.get("shared"),
            "collection_name": collection,
            "job_options": {"job": True},
        }
        self.keywords.update(kwargs)

    def add_data(self, *args, **kwargs):
        raise NotImplementedError("Add Data not supported yet.")

    def train(self, *args, **kwargs):
        raise NotImplementedError("Train not supported yet.")

    def clear(self, *args, **kwargs):
        raise NotImplementedError("Clear not supported yet.")

    def explain(self, *args, **kwargs):
        raise NotImplementedError("Explain not supported yet.")

    def remove_example(self, *args, **kwargs):
        raise NotImplementedError("Remove Example not supported yet.")

    def rename(self, *args, **kwargs):
        raise NotImplementedError("Rename not supported yet.")

    def authorize(self, *args, **kwargs):
        return super().authorize(*args, **kwargs)

    def deauthorize(self, *args, **kwargs):
        return super().deauthorize(*args, **kwargs)

    def register(self, *args, **kwargs):
        return super().register(*args, **kwargs)

    def deregister(self, *args, **kwargs):
        return super().deregister(*args, **kwargs)

    def info(self, version=2, cloud=None, **kwargs):
        return self._api_handler(
            None, cloud=cloud, api="custom", method="info", version=version, **kwargs
        )

    def predict(self, data, version=2, cloud=None, **kwargs):
        return self._api_handler(
            data, cloud=cloud, api="custom", method="predict", version=version, **kwargs
        )

    def load(self, version=2, cloud=None, **kwargs):
        info = self.info(version=version, cloud=cloud, **kwargs)
        if info.get("load_status") == "ready":
            return info

        return self._api_handler(
            None, cloud=cloud, api="custom", method="load", version=version, **kwargs
        )
