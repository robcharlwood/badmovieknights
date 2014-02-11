# import python deps
import json

# import django deps
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# import projectr deps
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from core.tests.appengine_base import AppEngineTestCase
from blog.models import Entry


# base API entry test class
class BaseEntryAPITestCase(AppEngineTestCase):
    def setUp(self):
        super(BaseEntryAPITestCase, self).setUp()
        self.client = APIClient()
        self.author = User.objects.create_user(
            username='rob', password='password')
        self.token = Token.objects.get(user__username='rob')
        self.entry_1 = Entry.objects.create(
            author=self.author,
            title='My Blog Entry',
            content='# My Content',
            published=True)
        self.entry_2 = Entry.objects.create(
            author=self.author,
            title='My Blog Entry 2',
            content='# My Content 2',
            published=True)
        self.entry_3 = Entry.objects.create(
            author=self.author,
            title='My Blog Entry 3',
            content='# My Content 3',
            published=False)


# api entry list test case
class APIEntryListTestCase(BaseEntryAPITestCase):
    def test_entry_list_200(self):
        # entry list should return published entries
        resp = self.client.get(reverse('badmovieknights_api:entry_list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned = json.loads(resp.content)
        self.assertEqual(2, len(returned))
        e1 = returned[0]
        e2 = returned[1]
        self.assertEqual(self.entry_1.id, e1['id'])
        self.assertEqual(self.entry_2.id, e2['id'])

    def test_entry_list_authenticated_200(self):
        # entry list should return published and unpublished items
        # for authenticated api calls
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.get(reverse('badmovieknights_api:entry_list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned = json.loads(resp.content)
        self.assertEqual(3, len(returned))
        e1 = returned[0]
        e2 = returned[1]
        e3 = returned[2]
        self.assertEqual(self.entry_1.id, e1['id'])
        self.assertEqual(self.entry_2.id, e2['id'])
        self.assertEqual(self.entry_3.id, e3['id'])

    def test_entry_list_create_401(self):
        # test create not allowed if not authenticated
        resp = self.client.post(
            reverse('badmovieknights_api:entry_list'),
            {'title': 'Entry 4', 'content': '# Content 4'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_entry_list_create_ok(self):
        # test create ok when authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.post(
            reverse('badmovieknights_api:entry_list'),
            {'title': 'Entry 4', 'content': '# Content 4'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        returned = json.loads(resp.content)
        self.assertEqual(returned['title'], 'Entry 4')
        self.assertEqual(returned['content'], '# Content 4')
        self.assertEqual(returned['published'], False)


# entry detail test case
class APIEntryDetailTestCase(BaseEntryAPITestCase):
    def test_entry_detail_200(self):
        # entry detail should return published entries only
        resp = self.client.get(reverse(
            'badmovieknights_api:entry_detail',
            kwargs={'pk': self.entry_1.pk}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned = json.loads(resp.content)
        self.assertEqual(self.entry_1.id, returned['id'])
        self.assertEqual(self.entry_1.title, returned['title'])
        self.assertEqual(self.entry_1.content, returned['content'])
        self.assertEqual(self.entry_1.published, returned['published'])

        # now try and access an unpublished entry
        resp = self.client.get(reverse(
            'badmovieknights_api:entry_detail',
            kwargs={'pk': self.entry_3.pk}))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_entry_detail_authenticated_200(self):
        # entry detail should return published & unpublished entries
        # for authenticated api calls
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.get(reverse(
            'badmovieknights_api:entry_detail',
            kwargs={'pk': self.entry_1.pk}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned = json.loads(resp.content)
        self.assertEqual(self.entry_1.id, returned['id'])
        self.assertEqual(self.entry_1.title, returned['title'])
        self.assertEqual(self.entry_1.content, returned['content'])
        self.assertEqual(self.entry_1.published, returned['published'])

        # try and access an unpublished entry
        resp = self.client.get(reverse(
            'badmovieknights_api:entry_detail',
            kwargs={'pk': self.entry_3.pk}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned = json.loads(resp.content)
        self.assertEqual(self.entry_3.id, returned['id'])
        self.assertEqual(self.entry_3.title, returned['title'])
        self.assertEqual(self.entry_3.content, returned['content'])
        self.assertEqual(self.entry_3.published, returned['published'])

    def test_entry_detail_put_unauthenticated(self):
        # test forbidden update if unauthenticated
        resp = self.client.put(
            reverse('badmovieknights_api:entry_detail', kwargs={
                'pk': self.entry_1.pk
            }), {
                'title': 'Edited', 'content': '# Edited',
                'published': True
            })
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_entry_detail_put_ok(self):
        # test updates ok when authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.put(
            reverse('badmovieknights_api:entry_detail', kwargs={
                'pk': self.entry_1.pk
            }), {
                'title': 'Edited', 'content': '# Edited',
                'published': True
            })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned = json.loads(resp.content)
        self.assertEqual(returned['title'], 'Edited')
        self.assertEqual(returned['content'], '# Edited')
        self.assertEqual(returned['published'], True)

    def test_entry_detail_delete_unauthenticated(self):
        # test forbidden delete if unauthenticated
        resp = self.client.delete(
            reverse('badmovieknights_api:entry_detail', kwargs={
                'pk': self.entry_1.pk
            }))
        # check the response code is a 401 unauthorized and that the
        # object remains
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(3, len(Entry.objects.all()))

    def test_entry_detail_delete_ok(self):
        # test delete ok when authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.delete(
            reverse('badmovieknights_api:entry_detail', kwargs={
                'pk': self.entry_1.pk
            }))
        # check the response code is good and we have one less item
        # in the entry model.
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(2, len(Entry.objects.all()))
