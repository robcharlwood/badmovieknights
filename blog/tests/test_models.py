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


# test entry translation model
class EntryTranslationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='rob', password='password')
        self.entry = Entry.objects.create(
            author=self.user,
            title='Entry Title',
            content='# This is an H1',
            published=True)
        self.trans = self.entry.translations.create(
            language='es',
            title='Entry Title ES',
            content='# This is an H1 ES')

    def test_unicode_method(self):
        # check unicode is what we expect
        self.assertEqual(
            self.trans.__unicode__(),
            u"translation_model:<class 'blog.models.EntryTranslation'> "
            "master_model:<class 'blog.models.Entry'> "
            "master_model_instance_id:%s language:es" % self.entry.pk)
