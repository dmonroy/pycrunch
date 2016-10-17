import json
import six

from .shoji import Entity

from pycrunch.expressions import parse_expr
from pycrunch.expressions import process_expr


class Dataset(Entity):
    """
    class for adding methods to the dataset entity
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
            expr_obj = process_expr(expr_obj, self)  # cause we need variable URLs
        elif expr is None:
            expr_obj = {}
        else:
            expr_obj = expr
        return self.session.patch(
            self.fragments.exclusion,
            data=json.dumps(dict(expression=expr_obj))
        )

    def create_categorical(self, categories, rules,
                           name, alias, description=''):

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
