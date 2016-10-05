"""
TODO:
    - Validate category_map ids
    -
"""

SKELETON = {
    "element": "shoji:entity",
    "body": {
        "name": "name",
        "description": "description",
        "alias": "alias",
        "expr": {
            "function": "combine_categories",
            "args": []
        }
    }
}


REQUIRED_VALUES = {"name", "id", "missing", "combined_ids"}


def var_name_to_url(ds, varname):
    """
    :param ds: The dataset we are gonna inspect
    :param varname: the variable name we want to check
    :return: the id of the given varname or None
    """
    try:
        return ds.variables.by('name')[varname].entity.self
    except KeyError:
        raise KeyError("Variable %s does not exist in Dataset %s" % (varname, ds['body']['name']))


def validate_category_map(map):
    """
    :param map: categories keyed by new category id mapped to existing ones
    :return: a list of dictionary objects that the Crunch Api expects
    """
    for value in map.values():
        keys = set(value.keys())
        assert keys & REQUIRED_VALUES, (
            "category_map has one or more missing keys of " % REQUIRED_VALUES)
    rebuilt = []
    for key, value in map.items():
        category = {}
        category.update(value)
        category['id'] = key
        rebuilt.append(category)
    return rebuilt


def combine_categories(ds, from_name, category_map, name, alias, description=''):
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
    :param ds: pycrunch session dataset
    :param from_name: name of the variable to recode
    :param name: name for the new variable
    :param alias: alias for the new variable
    :param description: description for the new variable
    :return: the new created variable
    """
    variable_url = var_name_to_url(ds, from_name)
    categories = validate_category_map(category_map)
    payload = SKELETON.copy()
    payload['body']['name'] = name
    payload['body']['alias'] = alias
    payload['body']['description'] = description
    payload['body']['expr']['args'] = [
        {
            "variable": variable_url
        },
        {
            "value": categories
        }
    ]
    return ds.variables.create(payload)


# ===    T E S T S
from pycrunch import connect, connect_with_token


def crunch_session():
    site = connect('gryphon-streaming@yougov.com', '71N8bDIoLwkqvvy7', 'https://alpha.crunch.io/api/')
    return connect_with_token(site.session.cookies['token'], 'https://alpha.crunch.io/api/')


if __name__ == '__main__':
    session = crunch_session()
    # get Mathias test dataset
    ds = session.projects.by('id')['614a7b2ebe9a4292bba54edce83563ae'].entity.datasets.by('id')['71f9ff66a4ad4e9385bbc4172f681d5f'].entity
    category_map = {
        1: {
            "name": "China",
            "missing": False,
            "combined_ids": [2, 3]
        },
        2: {
            "name": "Other",
            "missing": False,
            "combined_ids": [1]
        },
        -1: {
            "name": "Missing",
            "missing": True,
            "combined_ids": [-1]
        },
    }
    var = combine_categories(
        ds=ds,
        from_name='countryofresidence',
        category_map=category_map,
        name='Recode',
        alias='recode',
        description='Recoding variable'
    )
    var.refresh()
    print(var)
