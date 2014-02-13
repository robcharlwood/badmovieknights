# import google deps
from google.appengine.ext import testbed
from google.appengine.api.blobstore import blobstore_stub, file_blob_storage
from google.appengine.api.files import file_service_stub

# import django deps
from django.test import TestCase


# a cloud storage test bed based on Google's testbed
class CloudStorageTestbed(testbed.Testbed):
    """
        Test bed that sets up files for use in test cases
    """
    def init_blobstore_stub(self):
        blob_storage = file_blob_storage.FileBlobStorage(
            '/tmp/testbed.blobstore',
            testbed.DEFAULT_APP_ID
        )
        blob_stub = blobstore_stub.BlobstoreServiceStub(blob_storage)
        file_stub = file_service_stub.FileServiceStub(blob_storage)
        self._register_stub('blobstore', blob_stub)
        self._register_stub('file', file_stub)


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


# appengine storage base test case
class AppEngineStorageTestCase(TestCase):
    """
        Base test case for running appengine tests
        with google cloud storage files
    """
    def setUp(self):
        self.testbed = CloudStorageTestbed()
        self.testbed.activate()
        self.testbed.init_app_identity_stub()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_blobstore_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_urlfetch_stub()

    def tearDown(self):
        """
            Deactivate testbed so that tests don't
            interfere with one another
        """
        self.testbed.deactivate()
