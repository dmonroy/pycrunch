import pprint

pp = pprint.PrettyPrinter(indent=4)


COMPARATORS = {'>=', '>', '==', '<', '<=', '!=', 'in', 'not in'}
OPERATORS = {'+', '-', '*', '/'}
CONCATENATORS = {'and', 'or'}


def get_function_dict(function, variable, value):
    """
    :param function: one of the COMPARATORS
    :param variable: dataset variable name or categorical
    :param value: numeric, iterable or string
    :return: a dict representation of the filter:
    """
    return {
        "function": function,
        "args": [
            {
                "variable": variable
            },
            {
                "value": value
            }
        ]
    }


def get_function_concatenate(function, *args):
    """
    :param function: one of CONCATENATORS
    :param args: arguments we want concatenated
    :return: a dict representation of the concatenation
    """
    return {
        "function": function,
        "args": [arg for arg in args]
    }


def gt(variable, value):
    return get_function_dict('>', variable, value)


def ge(variable, value):
    return get_function_dict('>=', variable, value)


def eq(variable, value):
    return get_function_dict('==', variable, value)


def lt(variable, value):
    return get_function_dict('<', variable, value)


def le(variable, value):
    return get_function_dict('<=', variable, value)


def and_op(left, right):
    return get_function_concatenate('and', left, right)


def or_op(left, right):
    return get_function_concatenate('or', left, right)


if __name__ == '__main__':
    expression = or_op(and_op(gt('exit_status', 178), eq('age', 21)), le('birthyr', 2000))
    pp.pprint(expression)
