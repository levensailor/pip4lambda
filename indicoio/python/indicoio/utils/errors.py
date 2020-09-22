"""
Contains Indico Custom Errors
"""


# skeleton error classes to allow
# more specific exception handling
class IndicoError(ValueError):
    pass


class InvalidAPIKey(IndicoError):
    pass


class MissingAPIKey(IndicoError):
    pass


class MalformattedData(IndicoError):
    pass


class APIDoesNotExist(IndicoError):
    pass


class BatchProcessingError(IndicoError):
    pass


class DataStructureException(Exception):
    """
    If a non-accepted datastructure is passed, throws an exception
    """

    def __init__(self, callback, passed_structure, accepted_structures):
        self.callback = callback.__name__
        self.structure = str(type(passed_structure))
        self.accepted = [str(structure) for structure in accepted_structures]

    def __str__(self):
        return """
        function %s does not accept %s, accepted types are: %s
        """ % (
            self.callback,
            self.structure,
            str(self.accepted),
        )


ERR_MSGS = (
    ("invalid api key", InvalidAPIKey),
    ("api key not found", MissingAPIKey),
    ("input contains one or more empty strings", MalformattedData),
)


def convert_to_py_error(error_message):
    """
    Raise specific exceptions for ease of error handling
    """
    message = error_message.lower()
    for err_msg, err_type in ERR_MSGS:
        if err_msg in message:
            return err_type(error_message)
    else:
        return IndicoError(error_message)
