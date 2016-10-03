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
        exclusion_filter = {
            'function': '!=',
            'args': [
                {'variable': 'disposition.id'},
                {'value': 0}
            ]
        }

        ds = mock.MagicMock()
        ds.fragments.exclusion = self.exclusion_url

        exclusion(ds, exclusion_filter)
        ds.session.patch.assert_called_once_with(
            self.exclusion_url,
            data=json.dumps({'expression': exclusion_filter})
        )

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
