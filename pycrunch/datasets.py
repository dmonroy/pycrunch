import json

import six

from pycrunch.expressions import parse_expr
from pycrunch.expressions import process_expr


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
        expr_obj = process_expr(expr_obj, ds)  # cause we need variable URLs
    elif expr is None:
        expr_obj = {}
    else:
        expr_obj = expr
    return ds.session.patch(
        ds.fragments.exclusion,
        data=json.dumps(dict(expression=expr_obj))
    )
