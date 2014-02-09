# import google deps
from google.appengine.ext import testbed

# import django deps
from django.test import TestCase


# test the auth api views
class AppEngineTestCase(TestCase):
    def setUp(self):
        """
            Base TestCase class that uses app engines's
            test bed to stub out any services that we
            may need to test.
        """
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        """
            Deactivate testbed so that tests don't
            interfere with one another
        """
        self.testbed.deactivate()
