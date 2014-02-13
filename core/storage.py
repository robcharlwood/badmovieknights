# import python deps
import mimetypes
import os

# import django deps
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage

# import google deps
from google.appengine.api.blobstore import create_gs_key

# import lib deps
import cloudstorage as gcs


# storage backend for Google cloud storage
class GoogleCloudStorage(Storage):
    """
        A file storage backend for django appengine projects
        that uses google's cloud storage
    """
    def __init__(self, location=None, base_url=None):
        """
            Grab settings
        """
        if location is None:
            location = settings.GCS_BUCKET
        self.location = location
        if base_url is None:
            base_url = settings.GCS_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        """
            Method to open files on google cloud storage
        """
        filename = self.location + "/" + name
        gcs_file = gcs.open(filename, mode='r')
        f = ContentFile(gcs_file.read())
        gcs_file.close()
        return f

    def _save(self, name, content):
        """
            Method to save files to google cloud storage.
            This writes uploaded files with public-read permissions
        """
        filename = os.path.normpath(self.location + "/" + name)
        file_type, encoding = mimetypes.guess_type(name)
        gss_file = gcs.open(
            filename, mode='w',
            content_type=file_type,
            options={
                'x-goog-acl': 'public-read',
                'cache-control': settings.GCS_DEFAULT_CACHE_CONTROL
            })
        content.open()
        gss_file.write(content.read())
        content.close()
        gss_file.close()
        return name

    def delete(self, name):
        """
            Removes file from google cloud storage
        """
        filename = self.location + "/" + name
        try:
            gcs.delete(filename)
        except gcs.NotFoundError:
            pass

    def exists(self, name):
        """
            Method to check if a file exists on
            google cloud storage
        """
        try:
            self.get_file_info(name)
            return True
        except gcs.NotFoundError:
            return False

    def listdir(self, path=''):
        """
            Method to list contents of bucket based
            on the passed path.
        """
        directories, files = [], []
        bucket_contents = gcs.listbucket(self.location, prefix=path)
        for entry in bucket_contents:
            filePath = entry.filename
            head, tail = os.path.split(filePath)
            subPath = os.path.join(self.location, path)
            head = head.replace(subPath, '', 1)
            if head == "":
                head = None
            if not head and tail:
                files.append(tail)
            if head:
                if not head.startswith("/"):
                    head = "/" + head
                dir = head.split("/")[1]
                if not dir in directories:
                    directories.append(dir)
        return directories, files

    def size(self, name):
        """
            Method to get size of a file.
        """
        stats = self.get_file_info(name)
        return stats.st_size

    def url(self, name):
        """
            Returns the publically accessible URL for the file
            If in DEBUG mode then we server it via the google sdk
            blobstore using the google storage key
        """
        if settings.DEBUG:
            filename = "/gs" + self.location + "/" + name
            key = create_gs_key(filename)
            return "http://localhost:8000/blobstore/blob/" + \
                key + "?display=inline"
        return self.base_url + "/" + name

    def get_file_info(self, name):
        filename = self.location + "/" + name
        return gcs.stat(filename)
