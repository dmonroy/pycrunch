from unittest import TestCase
from unittest import mock

from pycrunch.recodes import validate_category_map
from pycrunch.recodes import combine_categories


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
        new_variable = combine_categories(ds, 'test', CATEGORY_MAP, 'name', 'alias')
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
