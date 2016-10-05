from pycrunch.elements import Element, JSONObject
from pycrunch.datasets import parse_expr


def create_categorical(ds, alias, name, categories, rules, description=''):
    """
    some docstring
    """

    print(len(categories), len(rules))
    print(rules)
    if not ((len(categories) - 1) <= len(rules) <= len(categories)):
        raise ValueError(
            'Amount of rules should match categories (or categories -1')

    if not hasattr(ds, 'variables'):
        ds.refresh()

    args = [{
        'column': [c['id'] for c in categories],
        'type': {
            'value': {
                'class': 'categorical',
                'categories': categories}}}]

    for rule in rules:
        args.append(parse_expr(rule, ds, urls=True))

    expr = dict(function='case', args=args)

    payload = dict(element='shoji:entity',
                   body=dict(alias=alias,
                             name=name,
                             expr=expr,
                             description=description))

    return ds.variables.create(payload)
