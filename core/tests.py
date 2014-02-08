# import python deps
import unittest

# import test deps
from ndbtestcase import NdbTestCase


# simple test case
class ATestCase(NdbTestCase):

    def setUp(self):
        self.param = 1
        super(ATestCase, self).setUp()

    def test_param(self):
        self.assertEqual(self.param, 1)

if __name__ == '__main__':
    unittest.main()
