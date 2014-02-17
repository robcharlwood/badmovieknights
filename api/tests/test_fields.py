# import django deps
from django.test import TestCase
from django.contrib.auth.models import User

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

    def test_field_to_native_no_markdown(self):
        """
            Make sure field_to_native()
            returns what we expect
        """
        f = TranslationField(markdown=False)
        result_1 = f.field_to_native(self.entry, 'content')
        self.assertEqual(u'# My Content', result_1)

    def test_field_to_native_markdown(self):
        """
            Make sure field_to_native()
            returns what we expect when markdown enabled
        """
        f = TranslationField(markdown=True)
        result_1 = f.field_to_native(self.entry, 'content')
        self.assertEqual(u'<h1>My Content</h1>', result_1)
