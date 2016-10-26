import json
import six

from pycrunch.expressions import parse_expr
from pycrunch.expressions import process_expr
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
    :param alias: the alias of the variable name we want to check
    :return: the id of the given varname or None
    """
    try:
        return ds.variables.by('alias')[alias].entity.self
    except KeyError:
        raise KeyError(
            "Variable %s does not exist in Dataset %s" % (alias,
                                                          ds['body']['name']))


def variable_to_url(ds, variable):
    """Receive a valid variable reference and return the variable url.

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
    :param ds: a dataset object
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
                "Unexistant variables %s in Dataset %s" % (
                    values, ds['body']['alias']))
    return mapped_urls


def validate_category_map(map):
    """
    :param map: categories keyed by new category id mapped to existing ones
    :return: a list of dictionary objects that the Crunch API expects
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
    :return: a list of dictionaries describing the new responses to create for
             the variable
    """
    rebuilt = list()
    for key, value in map.items():
        response = dict()
        response['name'] = key
        response['combined_ids'] = value
        rebuilt.append(response)
    return rebuilt


class Dataset(Entity):
    """
    A pycrunch.shoji.Entity subclass that provides dataset-specific methods.
    """

    def exclusion(self, expr=None):
        """
        Given a dataset object, apply an exclusion filter to it (defined as an
        expression string).

        If the `expr` parameter is None, an empty expression object is sent
        as part of the PATCH request, which effectively removes the exclusion
        filter (if any).
        """
        if isinstance(expr, six.string_types):
            expr_obj = parse_expr(expr)
            expr_obj = process_expr(expr_obj, self)  # cause we need URLs
        elif expr is None:
            expr_obj = {}
        else:
            expr_obj = expr
        return self.session.patch(
            self.fragments.exclusion,
            data=json.dumps(dict(expression=expr_obj))
        )

    def create_categorical(self, categories, rules,
                           name, alias, description='', missing=True):
        """
        creates a categorical variable deriving from other variables
        """
        if not ((len(categories) - 1) <= len(rules) <= len(categories)):
            raise ValueError(
                'Amount of rules should match categories (or categories -1')

        if not hasattr(self, 'variables'):
            self.refresh()

        args = [{
            'column': [c['id'] for c in categories],
            'type': {
                'value': {
                    'class': 'categorical',
                    'categories': categories}}}]

        for cat in args[0]['type']['value']['categories']:
            cat.setdefault('missing', False)

        if missing:
            args[0]['column'].append(-1)
            args[0]['type']['value']['categories'].append(dict(
                id=-1,
                name='No Data',
                numeric_value=None,
                missing=True))

        more_args = []
        for rule in rules:
            more_args.append(parse_expr(rule))

        more_args = process_expr(more_args, self)

        expr = dict(function='case', args=args + more_args)

        payload = dict(element='shoji:entity',
                       body=dict(alias=alias,
                                 name=name,
                                 expr=expr,
                                 description=description))

        return self.variables.create(payload)

    def combine_categories(self, variable, category_map,
                           name, alias, description=''):
        """
        Create a new variable in the given dataset that is a recode
        of an existing variable
        category_map = {
            1: {
                "name": "Favorable",
                "missing": True,
                "combined_ids": [1,2]
            },
        }
        :param variable: alias of the variable to recode
        :param name: name for the new variable
        :param alias: alias for the new variable
        :param description: description for the new variable
        :return: the new created variable
        """
        variable_url = variable_to_url(self, variable)
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
        return self.variables.create(payload)

    def combine_responses(self, variable, response_map,
                          name, alias, description=''):

        """
        Creates a new variable in the given dataset that combines existing
        responses into new categorized ones

        response_map = {
            new_subvar_name1:[old_subvar_alias1, old_subvar_alias2],
            new_subvar_name2: [old_subvar_alias3, old_subvar_alias4]
        }
        :return: newly created variable
        """
        variable_url = variable_to_url(self, variable)
        trans_responses = aliases_to_urls(self, variable_url, response_map)
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
        return self.variables.create(payload)
