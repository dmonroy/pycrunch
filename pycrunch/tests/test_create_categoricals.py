from unittest import TestCase
from unittest import mock

from pycrunch.create_categorical import create_categorical


categories = [
    {"id": 3, "name": "Hipsters", "numeric_value": None, "missing": False},
    {"id": 1, "name": "Techies", "numeric_value": None, "missing": False},
    {"id": 2, "name": "Yuppies", "numeric_value": None, "missing": False}]

rules = ['gender == 1', 'gender == 2']


class TestCreateCategorical(TestCase):

    def test_create_categorical(self):
        ds = mock.MagicMock()
        var_url = 'http://test.crunch.io/api/datasets/123/variables/0001/'
        ds.entity.self = 'http://test.crunch.io/api/datasets/123/'
        entity_mock = mock.MagicMock()
        entity_mock.entity.self = var_url
        ds.variables.by.return_value = {
            'gender': entity_mock
        }

        test = create_categorical(ds, 'alias', 'name',
                                  categories, rules, 'description')
        call = ds.variables.create.call_args_list[0][0][0]
        payload = {
          "body": {
            "name": "name",
            "alias": "alias",
            "description": "description",
            "expr": {
              "function": "case",
              "args": [
                {
                  "column": [
                    3,
                    1,
                    2
                  ],
                  "type": {
                    "value": {
                      "categories": [
                        {
                          "name": "Hipsters",
                          "id": 3,
                          "numeric_value": None,
                          "missing": False
                        },
                        {
                          "name": "Techies",
                          "id": 1,
                          "numeric_value": None,
                          "missing": False
                        },
                        {
                          "name": "Yuppies",
                          "id": 2,
                          "numeric_value": None,
                          "missing": False
                        }
                      ],
                      "class": "categorical"
                    }
                  }
                },
                {
                  "function": "==",
                  "args": [
                    {
                      "variable": "http://test.crunch.io/api/datasets/123/variables/0001/"
                    },
                    {
                      "value": 1
                    }
                  ]
                },
                {
                  "function": "==",
                  "args": [
                    {
                      "variable": "http://test.crunch.io/api/datasets/123/variables/0001/"
                    },
                    {
                      "value": 2
                    }
                  ]
                }
              ]
            }
          },
          "element": "shoji:entity"
        }
        assert call == payload
