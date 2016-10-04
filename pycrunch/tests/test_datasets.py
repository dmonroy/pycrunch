import json

from unittest import TestCase
from unittest import mock

from pycrunch.datasets import exclusion
from pycrunch.datasets import parse_expr


class TestExclusionFilters(TestCase):

    exclusion_url = 'http://test.crunch.io/api/datasets/123/exclusion/'

    def test_apply_exclusion(self):
        """
        Tests that the proper PATCH request is sent to Crunch in order to
        apply an exclusion filter to a dataset.
        """
        exclusion_filter = 'disposition != 0'
        var_url = 'http://test.crunch.io/api/datasets/123/variables/0001/'

        # Mocking setup.
        ds = mock.MagicMock()
        ds.fragments.exclusion = self.exclusion_url
        _disposition_mock = mock.MagicMock()
        _disposition_mock.entity.self = var_url
        ds.variables.by.return_value = {
            'disposition': _disposition_mock
        }

        # Action!
        exclusion(ds, exclusion_filter)

        # Ensure .patch was called the right way.
        assert len(ds.session.patch.call_args_list) == 1

        call = ds.session.patch.call_args_list[0]
        assert call[0][0] == self.exclusion_url

        expected_expr_obj = {
            'expression': {
                'function': '!=',
                'args': [
                    {'variable': var_url},  # Crunch needs variable URLs!
                    {'value': 0}
                ]
            }
        }
        assert json.loads(call[1]['data']) == expected_expr_obj

    def test_remove_exclusion(self):
        """
        Tests that the proper PATCH request is sent to Crunch in order to
        clear (i.e. remove) the exclusion filter from a dataset.
        """
        ds = mock.MagicMock()
        ds.fragments.exclusion = self.exclusion_url

        exclusion(ds)

        ds.session.patch.assert_called_once_with(
            self.exclusion_url,
            data=json.dumps({'expression': {}})
        )


class TestFilterExpressionParsing(TestCase):

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
