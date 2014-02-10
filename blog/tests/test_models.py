# import django deps
from django.contrib.auth.models import User
from django.test import TestCase

# import project deps
from blog.models import Entry


# test entry model
class EntryModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='rob', password='password')
        self.entry = Entry.objects.create(
            author=self.user,
            title='Entry Title',
            content='# This is an H1',
            published=True)

    def test_unicode_method(self):
        # check unicode method is what we expect
        self.assertEqual(self.entry.__unicode__(), '%s - %s' % (
            self.entry.title, self.entry.creation_date))

    def test_html_content_property(self):
        # test that markdown content stored in the db is converted
        # into HTML
        expected_content = u"<h1>This is an H1</h1>"
        self.assertEqual(expected_content, self.entry.html_content)
