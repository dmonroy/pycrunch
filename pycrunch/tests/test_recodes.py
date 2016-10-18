import json
from unittest import TestCase
from unittest import mock

from pycrunch.recodes import validate_category_map
from pycrunch.recodes import combine_categories
from pycrunch.recodes import combine_responses
from pycrunch.shoji import Entity

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

RECODES_PAYLOAD = {
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

COMBINE_RESPONSES_PAYLOAD = {
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

    def test_combine_categories_from_alias(self):
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

        assert call == RECODES_PAYLOAD

    def test_combine_categories_from_url(self):
        ds = mock.MagicMock()
        var_url = 'http://test.crunch.io/api/datasets/123/variables/0001/'
        ds.entity.self = 'http://test.crunch.io/api/datasets/123/'
        entity_mock = mock.MagicMock()
        entity_mock.entity.self = var_url
        ds.variables.by.return_value = {
            'test': entity_mock
        }
        combine_categories(ds, var_url, CATEGORY_MAP, 'name', 'alias')
        call = ds.variables.create.call_args_list[0][0][0]

        assert call == RECODES_PAYLOAD

    def test_combine_categories_from_entity(self):
        ds = mock.MagicMock()
        var_url = 'http://test.crunch.io/api/datasets/123/variables/0001/'
        ds.entity.self = 'http://test.crunch.io/api/datasets/123/'
        entity_mock = mock.MagicMock()
        entity_mock.entity.self = var_url
        ds.variables.by.return_value = {
            'test': entity_mock
        }
        entity = Entity(mock.MagicMock(), self=var_url, body={})
        combine_categories(ds, entity, CATEGORY_MAP, 'name', 'alias')
        call = ds.variables.create.call_args_list[0][0][0]

        assert call == RECODES_PAYLOAD

    def test_combine_responses_by_alias(self):
        ds = mock.MagicMock()
        var_url = 'http://test.crunch.io/api/datasets/123/variables/0001/'
        subvar1_url = 'http://test.crunch.io/api/datasets/123/variables/0001/subvariables/00001/'
        subvar2_url = 'http://test.crunch.io/api/datasets/123/variables/0001/subvariables/00002/'
        ds.entity.self = 'http://test.crunch.io/api/datasets/123/'

        # mock subvariables
        subvar_mock = mock.MagicMock()
        subvar_mock.entity.self = subvar1_url
        subvar2_mock = mock.MagicMock()
        subvar2_mock.entity.self = subvar2_url

        # mock parent variable
        entity_mock = mock.MagicMock()
        entity_mock.entity.self = var_url

        # add dictionaries return to by functions
        entity_mock.entity.subvariables.by.return_value = {
            'sub1': subvar_mock,
            'sub2': subvar2_mock
        }

        ds.variables.by.return_value = {
            'test': entity_mock
        }

        # mock response from ds.session.get(variable_url)
        var_response = mock.MagicMock()
        var_response.payload = entity_mock.entity
        ds.session.get.return_value = var_response

        # make the actual response call
        combine_responses(ds, 'test', RESPONSE_MAP, 'name', 'alias')
        call = ds.variables.create.call_args_list[0][0][0]

        assert call == COMBINE_RESPONSES_PAYLOAD

    def test_combine_responses_by_url(self):
        ds = mock.MagicMock()
        var_url = 'http://test.crunch.io/api/datasets/123/variables/0001/'
        subvar1_url = 'http://test.crunch.io/api/datasets/123/variables/0001/subvariables/00001/'
        subvar2_url = 'http://test.crunch.io/api/datasets/123/variables/0001/subvariables/00002/'
        ds.entity.self = 'http://test.crunch.io/api/datasets/123/'

        # mock subvariables
        subvar_mock = mock.MagicMock()
        subvar_mock.entity.self = subvar1_url
        subvar2_mock = mock.MagicMock()
        subvar2_mock.entity.self = subvar2_url

        # mock parent variable
        entity_mock = mock.MagicMock()
        entity_mock.entity.self = var_url

        # add dictionaries return to by functions
        entity_mock.entity.subvariables.by.return_value = {
            'sub1': subvar_mock,
            'sub2': subvar2_mock
        }

        ds.variables.by.return_value = {
            'test': entity_mock
        }

        # mock response from ds.session.get(variable_url)
        var_response = mock.MagicMock()
        var_response.payload = entity_mock.entity
        ds.session.get.return_value = var_response

        # make the actual response call
        combine_responses(ds, var_url, RESPONSE_MAP, 'name', 'alias')
        call = ds.variables.create.call_args_list[0][0][0]

        assert call == COMBINE_RESPONSES_PAYLOAD

    def test_combine_responses_by_entity(self):
        ds = mock.MagicMock()
        var_url = 'http://test.crunch.io/api/datasets/123/variables/0001/'
        subvar1_url = 'http://test.crunch.io/api/datasets/123/variables/0001/subvariables/00001/'
        subvar2_url = 'http://test.crunch.io/api/datasets/123/variables/0001/subvariables/00002/'
        ds.entity.self = 'http://test.crunch.io/api/datasets/123/'

        # mock subvariables
        subvar_mock = mock.MagicMock()
        subvar_mock.entity.self = subvar1_url
        subvar2_mock = mock.MagicMock()
        subvar2_mock.entity.self = subvar2_url

        # mock parent variable
        entity_mock = mock.MagicMock()
        entity_mock.entity.self = var_url

        # add dictionaries return to by functions
        entity_mock.entity.subvariables.by.return_value = {
            'sub1': subvar_mock,
            'sub2': subvar2_mock
        }

        ds.variables.by.return_value = {
            'test': entity_mock
        }

        # mock response from ds.session.get(variable_url)
        var_response = mock.MagicMock()
        var_response.payload = entity_mock.entity
        ds.session.get.return_value = var_response

        entity = Entity(
            mock.MagicMock(),
            self=var_url,
            body={}
        )

        # make the actual response call
        combine_responses(ds, entity, RESPONSE_MAP, 'name', 'alias')
        call = ds.variables.create.call_args_list[0][0][0]

        assert call == COMBINE_RESPONSES_PAYLOAD
