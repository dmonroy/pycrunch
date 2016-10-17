import re

from pycrunch import elements

VARIABLE_URL_REGEX = re.compile(
    r"^(http|https):\/\/(.*)\/api\/datasets\/([\w\d]+)\/variables\/([\w\d]+)"
    r"(\/subvariables\/([\w\d]*))?\/?$"
)


def cast(variable, type, format=None, offset=None, resolution=None):
    """Alter the given variable Entity to a new type.

    Various parameters may need to be sent to properly convert from one type
    to another. Datetime is particularly demanding.
    """
    payload = elements.JSONObject(cast_as=type)
    if format is not None:
        payload['format'] = format
    if offset is not None:
        payload['offset'] = offset
    if resolution is not None:
        payload['resolution'] = resolution

    return variable.cast.post(data=payload.json)


def validate_variable_url(url):
    """
    Checks if a given url matches the variable url regex or not.
    """
    return VARIABLE_URL_REGEX.match(url)
