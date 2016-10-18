import six

from pycrunch.shoji import Entity
from pycrunch.variables import validate_variable_url

SKELETON = {
    "element": "shoji:entity",
    "body": {
        "name": "name",
        "description": "description",
        "alias": "alias",
        "expr": {
            "function": "function",
            "args": []
        }
    }
}


REQUIRED_VALUES = {"name", "id", "missing", "combined_ids"}
REQUIRES_RESPONSES = {"combined_ids", "name"}


def var_name_to_url(ds, alias):
    """
    :param ds: The dataset we are gonna inspect
    :param varname: the variable name we want to check
    :return: the id of the given varname or None
    """
    try:
        return ds.variables.by('alias')[alias].entity.self
    except KeyError:
        raise KeyError(
            "Variable %s does not exist in Dataset %s" % (alias, ds['body']['name']))


def variable_to_url(ds, variable):
    """Receive an valid variable reference and return the variable url.

    :param ds: The crunch dataset
    :param variable: A valid variable reference in the form of a shoji Entity
                     of the variable or a string containing the variable url
                     or alias.
    :return: The variable url
    """
    assert isinstance(variable, (six.string_types, Entity))

    if isinstance(variable, Entity):
        return variable.self

    elif validate_variable_url(variable):
        return variable
    else:
        return var_name_to_url(ds, variable)


def aliases_to_urls(ds, variable_url, response_map):
    """
    Maps subvariable aliases to urls
    :param ds: /Users/mbc/Yougov/Crunch/pycrunch/pycrunch/recodes.py
    :param variable_url: url of the variable we want to inspect
    :param response_map: mapping of new subvariables
    :return:
    """
    suvars = ds.session.get(variable_url).payload.subvariables.by('alias')
    mapped_urls = {}
    for key, values in response_map.items():
        try:
            mapped_urls[key] = [suvars[x].entity.self for x in values]
        except KeyError:
            raise KeyError(
                "Unexistant variables %s in Dataset %s" % (values, ds['body']['alias']))
    return mapped_urls


def validate_category_map(map):
    """
    :param map: categories keyed by new category id mapped to existing ones
    :return: a list of dictionary objects that the Crunch Api expects
    """
    for value in map.values():
        keys = set(list(value.keys()))
        assert keys & REQUIRED_VALUES, (
            "category_map has one or more missing keys of " % REQUIRED_VALUES)
    rebuilt = list()
    for key, value in map.items():
        category = dict()
        category.update(value)
        # unfold expressions like range(1,5) to a list of ids
        category['combined_ids'] = list(category['combined_ids'])
        category['id'] = key
        rebuilt.append(category)
    return rebuilt


def validate_response_map(map):
    """
    :param map: responses keyed by new alias mapped to existing aliases
    :return: a list of dictionaries describing the new responses to create for the variable
    """
    rebuilt = list()
    for key, value in map.items():
        response = dict()
        response['name'] = key
        response['combined_ids'] = value
        rebuilt.append(response)
    return rebuilt


def combine_categories(dataset, variable, category_map, name, alias, description=''):
    """
    Create a new variable in the given dataset that is a recode
    of an existing variable
    category_map = {
        1: {
            "label": "Favorable",
            "missing": True,
            "num_value": 1,
            "ids": [1,2]
        },
    }
    :param dataset: pycrunch session dataset
    :param variable: alias of the variable to recode
    :param name: name for the new variable
    :param alias: alias for the new variable
    :param description: description for the new variable
    :return: the new created variable
    """
    variable_url = variable_to_url(dataset, variable)
    categories = validate_category_map(category_map)
    payload = SKELETON.copy()
    payload['body']['name'] = name
    payload['body']['alias'] = alias
    payload['body']['description'] = description
    payload['body']['expr']['function'] = 'combine_categories'
    payload['body']['expr']['args'] = [
        {
            "variable": variable_url
        },
        {
            "value": categories
        }
    ]
    return dataset.variables.create(payload)


def combine_responses(dataset, variable, response_map, name, alias, description=''):
    """
    Creates a new variable in the given dataset that combines existing responses
    into new categorized ones
    response_map = {
        new_subvar_name1:[old_subvar_alias1, old_subvar_alias2],
        new_subvar_name2: [old_subvar_alias3, old_subvar_alias4]
    }
    :return: newly created variable
    """
    variable_url = variable_to_url(dataset, variable)
    trans_responses = aliases_to_urls(dataset, variable_url, response_map)
    responses = validate_response_map(trans_responses)
    payload = SKELETON.copy()
    payload['body']['name'] = name
    payload['body']['alias'] = alias
    payload['body']['description'] = description
    payload['body']['expr']['function'] = 'combine_responses'
    payload['body']['expr']['args'] = [
        {
            "variable": variable_url
        },
        {
            "value": responses
        }
    ]
    return dataset.variables.create(payload)

