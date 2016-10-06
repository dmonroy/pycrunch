from unittest import TestCase
from unittest import mock

from pycrunch.recodes import validate_category_map
from pycrunch.recodes import combine_categories
from pycrunch.recodes import combine_responses


CATEGORY_MAP = {
    1: {
        "name": "China",
        "missing": False,
        "combined_ids": [2, 3]
    },
    2: {
        "name": "Other",
        "missing": False,
        "combined_ids": [1]
    }
}

RESPONSE_MAP = {
    'newsubvar': ['sub1', 'sub2']
}


class TestRecodes(TestCase):

    def test_validate_category_map(self):
        """ Validate that a variable name returns a valid url """
        expected_map = [
            {
                "id": 1,
                "name": "China",
                "missing": False,
                "combined_ids": [2, 3]
            },
            {
                "id": 2,
                "name": "Other",
                "missing": False,
                "combined_ids": [1]
            }
        ]
        modified_map = validate_category_map(CATEGORY_MAP)
        assert modified_map == expected_map

    def test_combine_categories(self):
        ds = mock.MagicMock()
        var_url = 'http://test.crunch.io/api/datasets/123/variables/0001/'
        ds.entity.self = 'http://test.crunch.io/api/datasets/123/'
        entity_mock = mock.MagicMock()
        entity_mock.entity.self = var_url
        ds.variables.by.return_value = {
            'test': entity_mock
        }
        combine_categories(ds, 'test', CATEGORY_MAP, 'name', 'alias')
        call = ds.variables.create.call_args_list[0][0][0]
        recodes_payload = {
            "element": "shoji:entity",
            "body": {
                "name": "name",
                "description": "",
                "alias": "alias",
                "expr": {
                    "function": "combine_categories",
                    "args": [
                        {
                            "variable": 'http://test.crunch.io/api/datasets/123/variables/0001/'
                        },
                        {
                            "value": [
                                {
                                    "name": "China",
                                    "id": 1,
                                    "missing": False,
                                    "combined_ids": [2, 3]
                                },
                                {
                                    "name": "Other",
                                    "id": 2,
                                    "missing": False,
                                    "combined_ids": [1]
                                }
                            ]
                        }
                    ]
                }
            }
        }
        assert call == recodes_payload

    def test_combine_responses(self):
        ds = mock.MagicMock()
        var_url = 'http://test.crunch.io/api/datasets/123/variables/0001/'
        subvar1_url = 'http://test.crunch.io/api/datasets/123/variables/0001/subvariables/00001/'
        subvar2_url = 'http://test.crunch.io/api/datasets/123/variables/0001/subvariables/00002/'
        ds.entity.self = 'http://test.crunch.io/api/datasets/123/'
        entity_mock = mock.MagicMock()
        entity_mock.entity.self = var_url
        # mock subvariables
        subvar_mock = mock.MagicMock()
        subvar_mock.entity.self = subvar1_url
        subvar2_mock = mock.MagicMock()
        subvar2_mock.entity.self = subvar2_url
        # add dictionaries return to by function
        entity_mock.entity.subvariables.by.return_value = {
            'sub1': subvar_mock,
            'sub2': subvar2_mock
        }
        ds.variables.by.return_value = {
            'test': entity_mock
        }
        # make the actual response call
        combine_responses(ds, 'test', RESPONSE_MAP, 'name', 'alias')
        call = ds.variables.create.call_args_list[0][0][0]
        expected_payload = {
            'element': 'shoji:entity',
            'body': {
                'alias': 'alias',
                'description': '',
                'name': 'name',
                'expr': {
                    'function': 'combine_responses',
                    'args': [
                        {
                            'variable': 'http://test.crunch.io/api/datasets/123/variables/0001/'
                        },
                        {
                            'value': [
                                {
                                    'name': 'newsubvar',
                                    'combined_ids': [
                                        'http://test.crunch.io/api/datasets/123/variables/0001/subvariables/00001/',
                                        'http://test.crunch.io/api/datasets/123/variables/0001/subvariables/00002/'
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }
        assert call == expected_payload
