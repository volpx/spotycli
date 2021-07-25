# -*- coding: utf-8 -*-

# Run with python -m tests.test_advanced

from .context import spotycli

import unittest


class AdvancedTestSuite(unittest.TestCase):
	"""Advanced test cases."""

	def test_init(self):
		self.assertIsNone(spotycli.test())


if __name__ == '__main__':
	unittest.main()
