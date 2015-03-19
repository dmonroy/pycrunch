# -*- coding: utf-8 -*-

import six

from pycrunch import csvlib

class TestCSV:
	def test_unicode_values(self):
		"CSV rendering should handle simple unicode"
		rows = [[u'☃']]
		csvlib.rows_as_csv_file(rows)

	def test_result_is_binary(self):
		"Result should be a stream with a binary type"
		res = csvlib.rows_as_csv_file([['foo']])
		assert isinstance(res.getvalue(), six.binary_type)