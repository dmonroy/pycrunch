import pytest
from unittest import TestCase

from pycrunch.datasets import parse_expr


class TestExpressionParsing(TestCase):

    def test_parse_equal_int(self):
        expr = "age == 1"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '==',
            'args': [
                {
                    'variable': 'age'
                },
                {
                    'value': 1
                }
            ]
        }

        # Reversed.
        expr = "1 == age"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '==',
            'args': [
                {
                    'value': 1
                },
                {
                    'variable': 'age'
                }
            ]
        }

    def test_parse_equal_string(self):
        expr = "name == 'John Doe'"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '==',
            'args': [
                {
                    'variable': 'name'
                },
                {
                    'value': 'John Doe'
                }
            ]
        }

        # Reversed.
        expr = "'John Doe' == name"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '==',
            'args': [
                {
                    'value': 'John Doe'
                },
                {
                    'variable': 'name'
                }
            ]
        }

    def test_parse_notequal_int(self):
        expr = "age != 1"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '!=',
            'args': [
                {
                    'variable': 'age'
                },
                {
                    'value': 1
                }
            ]
        }

        # Reversed.
        expr = "1 != age"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '!=',
            'args': [
                {
                    'value': 1
                },
                {
                    'variable': 'age'
                }
            ]
        }

    def test_parse_notequal_string(self):
        expr = "name != 'John Doe'"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '!=',
            'args': [
                {
                    'variable': 'name'
                },
                {
                    'value': 'John Doe'
                }
            ]
        }

        # Reversed.
        expr = "'John Doe' != name"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '!=',
            'args': [
                {
                    'value': 'John Doe'
                },
                {
                    'variable': 'name'
                }
            ]
        }

    def test_parse_less_than(self):
        expr = "caseid < 1234"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '<',
            'args': [
                {
                    'variable': 'caseid'
                },
                {
                    'value': 1234
                }
            ]
        }

        # Reversed.
        expr = "1234 < caseid"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '<',
            'args': [
                {
                    'value': 1234
                },
                {
                    'variable': 'caseid'
                }
            ]
        }

    def test_parse_less_than_equal(self):
        expr = "caseid <= 1234"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '<=',
            'args': [
                {
                    'variable': 'caseid'
                },
                {
                    'value': 1234
                }
            ]
        }

        # Reversed.
        expr = "1234 <= caseid"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '<=',
            'args': [
                {
                    'value': 1234
                },
                {
                    'variable': 'caseid'
                }
            ]
        }

    def test_parse_greater_than(self):
        expr = "caseid > 1234"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '>',
            'args': [
                {
                    'variable': 'caseid'
                },
                {
                    'value': 1234
                }
            ]
        }

        # Reversed.
        expr = "1234 > caseid"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '>',
            'args': [
                {
                    'value': 1234
                },
                {
                    'variable': 'caseid'
                }
            ]
        }

    def test_parse_greater_than_equal(self):
        expr = "caseid >= 1234"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '>=',
            'args': [
                {
                    'variable': 'caseid'
                },
                {
                    'value': 1234
                }
            ]
        }

        # Reversed.
        expr = "1234 >= caseid"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '>=',
            'args': [
                {
                    'value': 1234
                },
                {
                    'variable': 'caseid'
                }
            ]
        }

    def test_parse_compare_variable_against_another_variable(self):
        expr = "starttdate == arrivedate"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '==',
            'args': [
                {
                    'variable': 'starttdate'
                },
                {
                    'variable': 'arrivedate'
                }
            ]
        }

        expr = "starttdate != arrivedate"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '!=',
            'args': [
                {
                    'variable': 'starttdate'
                },
                {
                    'variable': 'arrivedate'
                }
            ]
        }

        expr = "starttdate < arrivedate"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '<',
            'args': [
                {
                    'variable': 'starttdate'
                },
                {
                    'variable': 'arrivedate'
                }
            ]
        }

        expr = "starttdate <= arrivedate"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '<=',
            'args': [
                {
                    'variable': 'starttdate'
                },
                {
                    'variable': 'arrivedate'
                }
            ]
        }

        expr = "starttdate > arrivedate"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '>',
            'args': [
                {
                    'variable': 'starttdate'
                },
                {
                    'variable': 'arrivedate'
                }
            ]
        }

        expr = "starttdate >= arrivedate"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '>=',
            'args': [
                {
                    'variable': 'starttdate'
                },
                {
                    'variable': 'arrivedate'
                }
            ]
        }

    def test_parse_multiple_boolean_conditions(self):
        expr = '(identity == 1 and caseid <= surveyid) or identity >= 2'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'or',
            'args': [
                {
                    'function': 'and',
                    'args': [
                        {
                            'function': '==',
                            'args': [
                                {
                                    'variable': 'identity'
                                },
                                {
                                    'value': 1
                                }
                            ]
                        },
                        {
                            'function': '<=',
                            'args': [
                                {
                                    'variable': 'caseid'
                                },
                                {
                                    'variable': 'surveyid'
                                }
                            ]
                        }
                    ]
                },
                {
                    'function': '>=',
                    'args': [
                        {
                            'variable': 'identity'
                        },
                        {
                            'value': 2
                        }
                    ]
                }
            ]
        }

    def test_parse_value_in_list(self):
        expr = "web_browser in ['abc', 'dfg', 'hij']"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'in',
            'args': [
                {
                    'variable': 'web_browser'
                },
                {
                    'value': ['abc', 'dfg', 'hij']
                }
            ]
        }

    def test_parse_value_not_in_list(self):
        expr = 'country not in [1, 2, 3]'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'in',
                    'args': [
                        {
                            'variable': 'country'
                        },
                        {
                            'value': [1, 2, 3]
                        }
                    ]
                }
            ]
        }

    def test_parse_omnibus_rule_1(self):
        # 'text': 'diposition code 0 (screenouts)',
        # 'index_mapper': intersection(
        #        [{'disposition': [0]}, {'exit_status': [0]}])})
        expr = "disposition == 0 and exit_status == 0"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'and',
            'args': [
                {
                    'function': '==',
                    'args': [
                        {
                            'variable': 'disposition'
                        },
                        {
                            'value': 0
                        }
                    ]
                },
                {
                    'function': '==',
                    'args': [
                        {
                            'variable': 'exit_status'
                        },
                        {
                            'value': 0
                        }
                    ]
                }
            ]
        }

    def test_parse_has_any(self):
        expr = 'Q2.has_any([1, 2, 3])'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'any',
            'args': [
                {
                    'variable': 'Q2'
                },
                {
                    'value': [1, 2, 3]
                }
            ]
        }

        expr = 'Q2.has_any(1)'
        with pytest.raises(ValueError):
            parse_expr(expr)

        expr = 'Q2.has_any(Q3)'
        with pytest.raises(ValueError):
            parse_expr(expr)

    def test_parse_has_all(self):
        expr = 'Q2.has_all([1, 2, 3])'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'all',
            'args': [
                {
                    'variable': 'Q2'
                },
                {
                    'value': [1, 2, 3]
                }
            ]
        }

        expr = 'Q2.has_all(1)'
        with pytest.raises(ValueError):
            parse_expr(expr)

        expr = 'Q2.has_all(Q3)'
        with pytest.raises(ValueError):
            parse_expr(expr)

    def test_parse_has_count(self):
        expr = 'Q2.has_count(1)'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'has_count',
            'args': [
                {
                    'variable': 'Q2'
                },
                {
                    'value': 1
                }
            ]
        }

        expr = 'Q2.has_count(1, 2)'
        with pytest.raises(ValueError):
            parse_expr(expr)

        expr = 'Q2.has_count([1,2])'
        with pytest.raises(ValueError):
            parse_expr(expr)

    def test_parse_omnibus_rule_2_complex(self):
        # Lets combine this with the previous one:
        # 'text': 'diposition code 0 (quotafull)',
        # 'index_mapper': intersection(
        #     [{'disposition': [0]}, {'exit_status': [1]}])
        expr = "(disposition == 0 and exit_status == 1) or " \
               "(disposition == 0 and exit_status == 0)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'or',
            'args': [{
                    'function': 'and',
                    'args': [
                        {
                            'function': '==',
                            'args': [
                                {
                                    'variable': 'disposition'
                                },
                                {
                                    'value': 0
                                }
                            ]
                        },
                        {
                            'function': '==',
                            'args': [
                                {
                                    'variable': 'exit_status'
                                },
                                {
                                    'value': 1
                                }
                            ]
                        }
                    ]
                },
                {
                    'function': 'and',
                    'args': [
                        {
                            'function': '==',
                            'args': [
                                {
                                    'variable': 'disposition'
                                },
                                {
                                    'value': 0
                                }
                            ]
                        },
                        {
                            'function': '==',
                            'args': [
                                {
                                    'variable': 'exit_status'
                                },
                                {
                                    'value': 0
                                }
                            ]
                        }
                    ]
                }
            ]}

    def test_parse_omnibus_has_any(self):
        # 'text': 'CompanyTurnover is NA',
        # 'index_mapper': {'CompanyTurnover': has_any([99])}},

        # 'text': 'Not Private Sector',
        # 'index_mapper': {'sector': has_any([2, 3, 98, 99])}},
        expr = "CompanyTurnover.has_any([99])"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'any',
            'args': [
                {
                    'variable': 'CompanyTurnover'
                },
                {
                    'value': [99]
                }
            ]
        }

        expr = "sector.has_any([2, 3, 98, 99])"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'any',
            'args': [
                {
                    'variable': 'sector'
                },
                {
                    'value': [2, 3, 98, 99]
                }
            ]
        }

    def test_parse_negated_expr(self):
        expr = "not (age == 1)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': '==',
                    'args': [
                        {
                            'variable': 'age'
                        },
                        {
                            'value': 1
                        }
                    ]
                }
            ]
        }

    def test_parse_negated_method_call(self):
        expr = 'not Q2.has_any([1, 2, 3])'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'any',
                    'args': [
                        {
                            'variable': 'Q2'
                        },
                        {
                            'value': [1, 2, 3]
                        }
                    ]
                }
            ]
        }

        expr = 'not Q2.has_all([1, 2, 3])'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'all',
                    'args': [
                        {
                            'variable': 'Q2'
                        },
                        {
                            'value': [1, 2, 3]
                        }
                    ]
                }
            ]
        }

    def test_parse_duplicates_method(self):
        expr = "identity.duplicates()"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'duplicates',
            'args': [
                {
                    'variable': 'identity'
                }
            ]
        }

        # Negated.
        expr = "not identity.duplicates()"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'duplicates',
                    'args': [
                        {
                            'variable': 'identity'
                        }
                    ]
                }
            ]
        }

        # Parameters not allowed.
        with pytest.raises(ValueError):
            parse_expr("identity.duplicates([1,2,3])")

        with pytest.raises(ValueError):
            parse_expr("identity.duplicates(1)")

        with pytest.raises(ValueError):
            parse_expr("identity.duplicates('hello')")

        with pytest.raises(ValueError):
            parse_expr("identity.duplicates(False)")

    def test_parse_helper_functions(self):
        # One variable.
        expr = "valid(birthyear)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'is_valid',
            'args': [
                {
                    'variable': 'birthyear'
                }
            ]
        }

        expr = "missing(birthyear)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'is_missing',
            'args': [
                {
                    'variable': 'birthyear'
                }
            ]
        }

        # One variable, negated.
        expr = "not valid(birthyear)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'is_valid',
                    'args': [
                        {
                            'variable': 'birthyear'
                        }
                    ]
                }
            ]
        }

        expr = "not missing(birthyear)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'is_missing',
                    'args': [
                        {
                            'variable': 'birthyear'
                        }
                    ]
                }
            ]
        }

        # Multiple variables.
        expr = "valid(birthyear, birthmonth)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'and',
            'args': [
                {
                    'function': 'is_valid',
                    'args': [
                        {
                            'variable': 'birthyear'
                        }
                    ]
                },
                {
                    'function': 'is_valid',
                    'args': [
                        {
                            'variable': 'birthmonth'
                        }
                    ]
                }
            ]
        }

        expr = "missing(birthyear, birthmonth)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'and',
            'args': [
                {
                    'function': 'is_missing',
                    'args': [
                        {
                            'variable': 'birthyear'
                        }
                    ]
                },
                {
                    'function': 'is_missing',
                    'args': [
                        {
                            'variable': 'birthmonth'
                        }
                    ]
                }
            ]
        }

        # Multiple variables, negated.
        expr = "not valid(birthyear, birthmonth)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'and',
                    'args': [
                        {
                            'function': 'is_valid',
                            'args': [
                                {
                                    'variable': 'birthyear'
                                }
                            ]
                        },
                        {
                            'function': 'is_valid',
                            'args': [
                                {
                                    'variable': 'birthmonth'
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        expr = "not missing(birthyear, birthmonth)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'and',
                    'args': [
                        {
                            'function': 'is_missing',
                            'args': [
                                {
                                    'variable': 'birthyear'
                                }
                            ]
                        },
                        {
                            'function': 'is_missing',
                            'args': [
                                {
                                    'variable': 'birthmonth'
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        # More advanced combinations.
        expr = "caseid < 12345 and missing(birthyear, birthmonth)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'and',
            'args': [
                {
                    'function': '<',
                    'args': [
                        {
                            'variable': 'caseid'
                        },
                        {
                            'value': 12345
                        }
                    ]
                },
                {
                    'function': 'and',
                    'args': [
                        {
                            'function': 'is_missing',
                            'args': [
                                {
                                    'variable': 'birthyear'
                                }
                            ]
                        },
                        {
                            'function': 'is_missing',
                            'args': [
                                {
                                    'variable': 'birthmonth'
                                }
                            ]
                        }
                    ]
                }
            ]
        }


# 'diposition code 0 (incompletes)':
# intersection(
#     [{'disposition': not_any([1])},
#      union([{'exit_status': has_count(0)},
#             {'exit_status': is_ge(1)}])
#      ]
# )




# 'text': 'sta: nicht aus Deutschland',
# 'index_mapper': {'sta': has_any([17])}},

# 'text': '(age >= 18) & profile_julesage is NaN',
#             'index_mapper': intersection(
#                 [
#                     {'age': is_ge(18)},
#                     {'profile_julesage': has_count(0)}])},

#'text': '(age >= 18) & profile_bpcagesex is NaN',
# 'index_mapper': intersection(
#     [{'age': is_ge(18)}, {'profile_bpcagesex': has_count(0)}])}],

# 'text': 'LONDON 18 NAN (profile_bpcagesex)',
# 'index_mapper': intersection(
#     [{'age': is_ge(18)}, {'profile_bpcagesex': has_count(0)}])},

# 'text': 'profile_GOR not code 11',
# 'index_mapper': {'profile_GOR': not_any([11])}}],

# 'text': '(age >= 18) & profile_julesage is NaN',
# 'index_mapper': intersection(
#     [{'age': is_ge(18)}, {'profile_julesage': has_count(0)}])},


# 'text': 'Not the right decision maker',
# 'index_mapper': {'DecisionMaking2': not_any(frange('1-10'))}},

# 'text': 'Duplicate identity',
# 'columns': 'identity',
# 'duplicated': True}])


# {  Drop anything missing (not asked/skipped/don't know/missing)
#     'text': 'DE PET OWNER NaN',
#     'columns': [
#                 'age_omnibus_18', 'gender',
#                 'nielsenregion', ''],
#     'dropna': True}


# { 'text': 'pets_omnibus not codes 1-4',
#     'index_mapper': {'pets_omnibus': not_any([1, 2, 3, 4])}}]
