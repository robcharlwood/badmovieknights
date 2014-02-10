# import django deps
from django.contrib.auth.models import User
from django.test import TestCase

# import project deps
from blog.models import Entry


# test entry manager
class EntryManagerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='rob', password='password')
        self.entry = Entry.objects.create(
            author=self.user,
            title='Entry Title',
            content='Content field',
            published=True)
        self.entry_2 = Entry.objects.create(
            author=self.user,
            title='Entry Title 2',
            content='Content field 2',
            published=False)

    def test_get_query_set(self):
        # should only return published entry by default
        self.assertEqual(1, len(Entry.objects.all()))

        # due to the optimisations made, this should only
        # execute one query as we select related on user
        with self.assertNumQueries(1):
            e = Entry.objects.all()[0]
            self.assertEqual(self.entry, e)
            self.assertEqual(e.author.username, 'rob')
