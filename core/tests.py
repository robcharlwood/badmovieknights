# import python deps
import unittest

# import test deps
from django.test import TestCase


# simple test case
class ATestCase(TestCase):

    def setUp(self):
        self.param = 1
        super(ATestCase, self).setUp()

    def test_param(self):
        self.assertEqual(self.param, 1)

if __name__ == '__main__':
    unittest.main()
