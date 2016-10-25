import json

from unittest import TestCase
from unittest import mock

import pytest
from pycrunch.datasets import Dataset
from pycrunch.shoji import Tuple, Entity


class TestExclusionFilters(TestCase):

    ds_url = 'http://test.crunch.io/api/datasets/123/'

    def test_apply_exclusion(self):
        """
        Tests that the proper PATCH request is sent to Crunch in order to
        apply an exclusion filter to a dataset.
        """
        var_id = '0001'
        var_alias = 'disposition'
        var_type = 'numeric'
        var_url = '%svariables/%s/' % (self.ds_url, var_id)

        # Mocking setup.
        def _get(*args):
            if args[0] == 'id':
                return var_id
            if args[0] == 'alias':
                return var_alias
            if args[0] == 'type':
                return var_type
            if args[0] == 'is_subvar':
                return False
            return args[0]

        _var_mock = mock.MagicMock()
        _var_mock.entity.self = var_url
        _var_mock.__getitem__.side_effect = _get
        _var_mock.get.side_effect = _get

        class CrunchPayload(dict):
            def __getattr__(self, item):
                if item == 'payload':
                    return self
                else:
                    return self[item]

        def _session_get(*args, **kwargs):
            if args[0] == '%stable/' % self.ds_url:
                return CrunchPayload({
                    'metadata': {
                        var_alias: _var_mock
                    }
                })
            return CrunchPayload()

        ds = mock.MagicMock()
        ds.self = self.ds_url
        ds.fragments.exclusion = '%sexclusion/' % self.ds_url
        ds.fragments.table = '%stable/' % self.ds_url
        ds.__class__ = Dataset
        ds.exclusion = Dataset.exclusion
        ds.session.get.side_effect = _session_get

        # Action!
        exclusion_filter = 'disposition != 0'
        ds.exclusion(ds, exclusion_filter)

        # Ensure .patch was called the right way.
        assert len(ds.session.patch.call_args_list) == 1

        call = ds.session.patch.call_args_list[0]
        assert call[0][0] == ds.fragments.exclusion

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
        ds.fragments.exclusion = '%sexclusion/' % self.ds_url
        ds.__class__ = Dataset
        ds.exclusion = Dataset.exclusion
        ds.exclusion(ds)

        ds.session.patch.assert_called_once_with(
            ds.fragments.exclusion,
            data=json.dumps({'expression': {}})
        )


class TestVariables(TestCase):
    def test_variable_as_attribute(self):
        session = mock.MagicMock()

        test_variable = mock.MagicMock()
        test_variable.entity = Entity(session=session)

        variables = {
            'test_variable': test_variable
        }
        dataset = Dataset({})
        dataset.variables = mock.MagicMock()
        dataset.variables.by.return_value = variables

        assert isinstance(dataset.test_variable, Entity)
        with pytest.raises(AttributeError) as err:
            dataset.another_variable

        assert str(err.value) == 'Dataset has no attribute another_variable'
