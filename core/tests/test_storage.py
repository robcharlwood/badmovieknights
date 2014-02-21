# -*- coding: utf-8 -*-
# import django deps
from django.core.files.storage import get_storage_class
from django.core.files.base import ContentFile
from django.conf import settings

# import test deps
from core.tests.appengine_base import AppEngineStorageTestCase

# import project deps
from core.storage import GoogleCloudStorage


# test google cloud storage
class GoogleCloudStorageTestCase(AppEngineStorageTestCase):
    def setUp(self):
        super(GoogleCloudStorageTestCase, self).setUp()
        self.storage = GoogleCloudStorage()

    def test_get_blobstorage_storage(self):
        self.assertEqual(
            get_storage_class('core.storage.GoogleCloudStorage'),
            GoogleCloudStorage)

    def test_save(self):
        file_name = 'test_name.txt'
        file_content = b'test_content'
        f_name = self.storage.save(file_name, ContentFile(file_content))
        self.assertEqual(f_name, file_name)

    def test_open(self):
        file_name = 'test_name.txt'
        file_content = b'test_content'
        self.storage.save(file_name, ContentFile(file_content))
        f = self.storage.open(file_name)
        self.assertEqual(f.read(), file_content)

    def test_exists(self):
        file_name = 'test_name.txt'
        file_content = b'test_content'
        self.assertFalse(self.storage.exists(file_name))
        self.storage.save(file_name, ContentFile(file_content))
        self.assertTrue(self.storage.exists(file_name))

    def test_delete(self):
        file_name = 'test_name.txt'
        file_content = b'test_content'
        self.storage.save(file_name, ContentFile(file_content))
        self.assertTrue(self.storage.exists(file_name))
        self.storage.delete(file_name)
        self.assertFalse(self.storage.exists(file_name))

    def test_delete_bad_file(self):
        file_name = 'test_name.txt'
        file_content = b'test_content'
        self.storage.save(file_name, ContentFile(file_content))
        self.assertTrue(self.storage.exists(file_name))
        self.assertRaises(OSError, self.storage.delete, 'foo')

    def test_size(self):
        file_name = 'test_name.txt'
        file_content = b'test_content'
        self.storage.save(file_name, ContentFile(file_content))
        self.assertEqual(12, self.storage.size(file_name))

    def test_url(self):
        file_name = 'test_name.txt'
        file_content = b'test_content'
        self.storage.save(file_name, ContentFile(file_content))
        self.assertEqual(
            u'https://storage.googleapis.com/badmovieknights/test_name.txt',
            self.storage.url(file_name))

    def test_url_development(self):
        settings.DEBUG = True
        file_name = 'test_name.txt'
        file_content = b'test_content'
        self.storage.save(file_name, ContentFile(file_content))
        self.assertEqual(
            u'http://localhost:8000/blobstore/blob/encoded_gs_file:'
            'YmFkbW92aWVrbmlnaHRzL3Rlc3RfbmFtZS50eHQ=?display=inline',
            self.storage.url(file_name))
        settings.DEBUG = False

    def test_list_dir(self):
        file_name = 'test_name.txt'
        file_content = b'test_content'
        self.storage.save(file_name, ContentFile(file_content))
        self.assertEqual((['badmovieknights'], []), self.storage.listdir())

    def test_get_file_info(self):
        file_name = 'test_name.txt'
        file_content = b'test_content'
        self.storage.save(file_name, ContentFile(file_content))
        self.assertTrue(self.storage.size(file_name) is not None)
