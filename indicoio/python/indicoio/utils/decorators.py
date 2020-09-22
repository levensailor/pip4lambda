from functools import wraps


def detect_batch(data):
    return isinstance(data, list)


def detect_batch_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if isinstance(args[0], list):
            kwargs["batch"] = True
        return f(*args, **kwargs)

    return wrapper
