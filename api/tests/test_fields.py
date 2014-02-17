# import django deps
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import translation

# import project deps
from api.fields import TranslationField
from blog.models import Entry


# translatable field test case
class TranslationFieldTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='rob', password='password')
        self.entry = Entry.objects.create(
            author=self.author,
            title='My Blog Entry',
            content='# My Content',
            published=True)
        self.trans = self.entry.translations.create(
            language='es',
            title='My Blog Entry es',
            content='# My Content es')

    def test_field_to_native_no_markdown_no_trans(self):
        """
            Make sure field_to_native()
            returns what we expect
        """
        f = TranslationField(markdown=False)
        result_1 = f.field_to_native(self.entry, 'content')
        self.assertEqual(u'# My Content', result_1)

    def test_field_to_native_markdown_no_trans(self):
        """
            Make sure field_to_native()
            returns what we expect when markdown enabled
        """
        f = TranslationField(markdown=True)
        result_1 = f.field_to_native(self.entry, 'content')
        self.assertEqual(u'<h1>My Content</h1>', result_1)

    def test_field_to_native_no_markdown_with_trans(self):
        """
            Make sure field_to_native()
            returns what we expect when a translation is present
        """
        translation.activate('es')
        f = TranslationField(markdown=False)
        result_1 = f.field_to_native(self.entry, 'content')
        self.assertEqual(u'# My Content es', result_1)
        translation.activate('en')

    def test_field_to_native_markdown_with_trans(self):
        """
            Make sure field_to_native()
            returns what we expect when markdown enabled
            and there is a translation present.
        """
        translation.activate('es')
        f = TranslationField(markdown=True)
        result_1 = f.field_to_native(self.entry, 'content')
        self.assertEqual(u'<h1>My Content es</h1>', result_1)
        translation.activate('en')
