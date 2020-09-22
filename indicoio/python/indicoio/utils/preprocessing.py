"""
Image Utils
Handles preprocessing images before they are sent to the server
"""
import os.path, base64, re, warnings
from six import BytesIO, string_types, PY3

from PIL import Image

from indicoio.utils.errors import IndicoError

B64_PATTERN = re.compile(
    "^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)"
)


def file_exists(filename):
    """
    Check if a file exists (and don't error out on unicode inputs)
    """
    try:
        return os.path.isfile(filename)
    except (UnicodeDecodeError, UnicodeEncodeError, ValueError):
        return False


def data_preprocess(data, size=None, min_axis=None, batch=False):
    """
    Takes data and prepares it for sending to the api including
    resizing and image data/structure standardizing.
    """
    if batch:
        return [
            data_preprocess(el, size=size, min_axis=min_axis, batch=False)
            for el in data
        ]

    if isinstance(data, dict):
        return {
            key: data_preprocess(value, size=size, min_axis=min_axis, batch=False)
            for key, value in data.items()
        }
    if isinstance(data, string_types):
        if file_exists(data):
            # probably a path to an image
            preprocessed = Image.open(data)
        else:
            # base 64 encoded image data, a url, or raw content
            # send raw data to the server and let the server infer type
            b64_or_url = re.sub("^data:image/.+;base64,", "", data)
            return b64_or_url

    elif isinstance(data, Image.Image):
        # data is image from PIL
        preprocessed = data

    elif type(data).__name__ == "ndarray":
        # data is likely image from numpy/scipy
        if "float" in str(data.dtype) and data.min() >= 0 and data.max() <= 1:
            data *= 255.0
        try:
            preprocessed = Image.fromarray(data.astype("uint8"))
        except TypeError:
            raise IndicoError(
                "Please ensure the numpy array is in a format by PIL. "
                "Values must be between 0 and 1 or between 0 and 255 in greyscale, rgb, or rgba format."
            )

    else:
        # at this point we are unsure of the type -- it could be malformatted text or image data.
        raise IndicoError(
            "Invalid input datatype: `{}`. "
            "Ensure input data is one of the following types: "
            "`str`, `unicode`, `PIL.Image`, `np.ndarray`.".format(
                data.__class__.__name__
            )
        )

    #
    if size or min_axis:
        preprocessed = resize_image(preprocessed, size, min_axis)

    # standardize on b64 encoding for sending image data over the wire
    temp_output = BytesIO()
    preprocessed.save(temp_output, format="PNG")
    temp_output.seek(0)
    output_s = temp_output.read()
    return (
        base64.b64encode(output_s).decode("utf-8")
        if PY3
        else base64.b64encode(output_s)
    )


def resize_image(image, size, min_axis):
    if min_axis:
        min_idx, other_idx = (0, 1) if image.size[0] < image.size[1] else (1, 0)
        aspect = image.size[other_idx] / float(image.size[min_idx])
        if aspect > 10:
            warnings.warn(
                "An aspect ratio greater than 10:1 is not recommended", Warning
            )
        size_arr = [0, 0]
        size_arr[min_idx] = size
        size_arr[other_idx] = int(size * aspect)
        image = image.resize(tuple(size_arr))
    elif size:
        image = image.resize(size)
    return image


def get_list_dimensions(_list):
    """
    Takes a nested list and returns the size of each dimension followed
    by the element type in the list
    """
    if isinstance(_list, list) or isinstance(_list, tuple):
        return [len(_list)] + get_list_dimensions(_list[0])
    return []


def get_element_type(_list, dimens):
    """
    Given the dimensions of a nested list and the list, returns the type of the
    elements in the inner list.
    """
    elem = _list
    for _ in range(len(dimens)):
        elem = elem[0]
    return type(elem)
