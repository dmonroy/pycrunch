import ast
import json

import six


NOT_IN = object()


def parse_expr(expr):

    def _parse(node):
        obj = {}
        args = []
        op = None

        if isinstance(node, ast.AST):
            # Get the current node fields.
            fields = list(ast.iter_fields(node))

            # "Terminal" nodes. Recursion ends with these guys.
            if isinstance(node, ast.Name):
                _id = fields[0][1]
                return {
                    'variable': _id
                }
            elif isinstance(node, ast.Num) or isinstance(node, ast.Str):
                _val = fields[0][1]
                return {
                    'value': _val
                }
            elif isinstance(node, ast.Eq):
                return '=='
            elif isinstance(node, ast.NotEq):
                return '!='
            elif isinstance(node, ast.Lt):
                return '<'
            elif isinstance(node, ast.LtE):
                return '<='
            elif isinstance(node, ast.Gt):
                return '>'
            elif isinstance(node, ast.GtE):
                return '>='
            elif isinstance(node, ast.In):
                return 'in'
            elif isinstance(node, ast.NotIn):
                return NOT_IN
            elif isinstance(node, ast.List):
                _list = fields[0][1]
                if not (all(isinstance(el, ast.Str) for el in _list) or
                        all(isinstance(el, ast.Num) for el in _list)):
                    # Only list-of-int or list-of-str are currently supported
                    raise ValueError

                return {
                    'value': [
                        getattr(el, 's', None) or getattr(el, 'n')
                        for el in _list
                    ]
                }

            # "Non-terminal" nodes.
            else:
                for _name, _val in fields:
                    if isinstance(_val, ast.BoolOp) or isinstance(_val, ast.Compare):
                        # Descend.
                        obj.update(_parse(_val))
                    elif isinstance(_val, ast.And):
                        op = 'and'
                    elif isinstance(_val, ast.Or):
                        op = 'or'
                    elif _name == 'left':
                        left = _parse(_val)
                        args.append(left)
                    elif _name == 'ops':
                        if len(_val) != 1:
                            raise ValueError
                        op = _parse(_val[0])
                    elif _name == 'comparators':  # i.e. "the right side"
                        if len(_val) != 1:
                            raise ValueError
                        right = _parse(_val[0])
                        args.append(right)
                    elif isinstance(_val, list):
                        args = [_parse(arg) for arg in _val]

                if op:
                    if op is NOT_IN:
                        # Special treatment for the `not in` operator.
                        obj = {
                            'function': 'not',
                            'args': [
                                {
                                    'function': 'in',
                                    'args': []
                                }
                            ]
                        }
                    else:
                        obj = {
                            'function': op,
                            'args': []
                        }

            if args and 'args' in obj:
                if op is NOT_IN:
                    # Special treatment for the `not in` operator.
                    obj['args'][0]['args'] = args
                else:
                    obj['args'] = args

        return obj

    if expr is None:
        return dict()

    return _parse(ast.parse(expr, mode='eval'))


def post_process_expr(obj, variables):
    """
    Transform variable aliases into variable IDs (i.e. URLs)
    """
    for key, val in obj.items():
        if isinstance(val, dict):
            post_process_expr(val, variables)
        elif isinstance(val, list) or isinstance(val, tuple):
            for subitem in val:
                post_process_expr(subitem, variables)
        elif key == 'variable':
            obj[key] = variables[val].entity.self

    return obj


def exclusion(ds, expr=None):
    """
    Given a dataset object, apply an exclusion filter to it (defined as an
    expression string).

    If the `expr` parameter is None, an empty expression object is sent
    as part of the PATCH request, which effectively removes the exclusion
    filter (if any).
    """
    if isinstance(expr, six.string_types):
        expr_obj = parse_expr(expr)
        expr_obj = post_process_expr(expr_obj, ds.variables.by('alias'))
    elif expr is None:
        expr_obj = {}
    else:
        expr_obj = expr
    return ds.session.patch(
        ds.fragments.exclusion,
        data=json.dumps(dict(expression=expr_obj))
    )
