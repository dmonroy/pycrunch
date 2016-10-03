import json


def exclusion(ds, expr=None):
    """
    Given a dataset object, apply an exclusion filter to it (defined as an
    expression dictionary).
    """
    if expr is None:
        # An empty dictionary will effectively clear the exclusion filter.
        expr = dict()

    return ds.session.patch(
        ds.fragments.exclusion,
        data=json.dumps(dict(expression=expr))
    )
