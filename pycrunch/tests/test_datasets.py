import json

from unittest import TestCase
from unittest import mock

from pycrunch.datasets import exclusion


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
