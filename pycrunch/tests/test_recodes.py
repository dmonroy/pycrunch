from unittest import TestCase
from unittest import mock

import pycrunch
from pycrunch.datasets import Dataset
from pycrunch.datasets import validate_category_map


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
        """ Validate we are properly converting the given map of categories """
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

    def test_validate_range_expression(self):
        test_map = {
            1: {
                "name": "China",
                "missing": False,
                "combined_ids": range(1, 5)
            }
        }
        modified_map = validate_category_map(test_map)
        assert modified_map[0]['combined_ids'] == [1, 2, 3, 4]

    def test_combine_categories(self):
        ds = mock.MagicMock()
        ds.combine_categories = Dataset.combine_categories
        var_url = 'http://test.crunch.io/api/datasets/123/variables/0001/'
        ds.entity.self = 'http://test.crunch.io/api/datasets/123/'
        entity_mock = mock.MagicMock()
        entity_mock.entity.self = var_url
        ds.variables.by.return_value = {
            'test': entity_mock
        }
        ds.combine_categories(ds, 'test', CATEGORY_MAP, 'name', 'alias')
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
        ds.combine_responses = Dataset.combine_responses
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
        ds.combine_responses(ds, 'test', RESPONSE_MAP, 'name', 'alias')
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
