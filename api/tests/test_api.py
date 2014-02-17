# import python deps
import json
import datetime

# import django deps
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.timezone import utc

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
        creation_date_1 = datetime.datetime.utcnow().replace(tzinfo=utc)
        creation_date_2 = datetime.datetime.utcnow().replace(
            tzinfo=utc) - datetime.timedelta(hours=13)
        creation_date_3 = datetime.datetime.utcnow().replace(
            tzinfo=utc) - datetime.timedelta(hours=15)
        self.client = APIClient()
        self.author = User.objects.create_user(
            username='rob', password='password')
        self.token = Token.objects.get(user__username='rob')
        self.entry_1 = Entry.objects.create(
            author=self.author,
            title='My Blog Entry',
            content='# My Content',
            published=True,
            creation_date=creation_date_1)
        self.entry_2 = Entry.objects.create(
            author=self.author,
            title='My Blog Entry 2',
            content='# My Content 2',
            published=True,
            creation_date=creation_date_2)
        self.entry_3 = Entry.objects.create(
            author=self.author,
            title='My Blog Entry 3',
            content='# My Content 3',
            published=False,
            creation_date=creation_date_3)

        # add translations for entry 1
        self.trans_1 = self.entry_1.translations.create(
            language='es',
            title='My Blog Entry es',
            content='# My Content es')
        self.trans_2 = self.entry_1.translations.create(
            language='fr',
            title='My Blog Entry fr',
            content='# My Content fr')


# api entry list test case
class APIEntryListTestCase(BaseEntryAPITestCase):
    def test_entry_list_200(self):
        # entry list should return published entries
        resp = self.client.get(reverse('badmovieknights_api:entry-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned = json.loads(resp.content)
        self.assertEqual(2, len(returned))
        e1 = returned[0]
        e2 = returned[1]

        # check ids
        self.assertEqual(self.entry_1.id, e1['id'])
        self.assertEqual(self.entry_2.id, e2['id'])

        # test mark down fields are rendered into html
        self.assertEqual('<h1>My Content</h1>', e1['content'])
        self.assertEqual('<h1>My Content 2</h1>', e2['content'])

        # test author field
        self.assertEqual('rob', e1['author'])
        self.assertEqual('rob', e2['author'])

    def test_entry_list_authenticated_200(self):
        # entry list should return published and unpublished items
        # for authenticated api calls
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.get(reverse('badmovieknights_api:entry-list'))
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
            reverse('badmovieknights_api:entry-list'),
            {'title': 'Entry 4', 'content': '# Content 4'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_entry_list_create_ok(self):
        # test create ok when authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.post(
            reverse('badmovieknights_api:entry-list'),
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
            'badmovieknights_api:entry-detail',
            kwargs={'pk': self.entry_1.pk}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned = json.loads(resp.content)
        self.assertEqual(self.entry_1.id, returned['id'])
        self.assertEqual(self.entry_1.title, returned['title'])
        self.assertEqual('<h1>My Content</h1>', returned['content'])
        self.assertEqual('rob', returned['author'])

        # now try and access an unpublished entry
        resp = self.client.get(reverse(
            'badmovieknights_api:entry-detail',
            kwargs={'pk': self.entry_3.pk}))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_entry_detail_authenticated_200(self):
        # entry detail should return published & unpublished entries
        # for authenticated api calls
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.get(reverse(
            'badmovieknights_api:entry-detail',
            kwargs={'pk': self.entry_1.pk}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned = json.loads(resp.content)
        self.assertEqual(self.entry_1.id, returned['id'])
        self.assertEqual(self.entry_1.title, returned['title'])
        self.assertEqual(self.entry_1.content, returned['content'])
        self.assertEqual('# My Content', returned['content'])
        self.assertEqual(self.entry_1.published, returned['published'])

        # try and access an unpublished entry
        resp = self.client.get(reverse(
            'badmovieknights_api:entry-detail',
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
            reverse('badmovieknights_api:entry-detail', kwargs={
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
            reverse('badmovieknights_api:entry-detail', kwargs={
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
            reverse('badmovieknights_api:entry-detail', kwargs={
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
            reverse('badmovieknights_api:entry-detail', kwargs={
                'pk': self.entry_1.pk
            }))
        # check the response code is good and we have one less item
        # in the entry model.
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(2, len(Entry.objects.all()))


# api entry translation list test case
class APIEntryTranslationListTestCase(BaseEntryAPITestCase):

    def test_entry_translation_list_unauthenticated(self):
        # translations should not be listed if not authenticated
        resp = self.client.get(
            reverse(
                'badmovieknights_api:entrytranslation-list',
                kwargs={'entry_pk': self.entry_1.pk}))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_entry_translation_list_create_401(self):
        # test create translation not allowed if not authenticated
        resp = self.client.post(
            reverse(
                'badmovieknights_api:entrytranslation-list',
                kwargs={'entry_pk': self.entry_2.pk}), {
                    'title': 'My Blog Entry 2 es',
                    'content': '# My Content 2 es',
                    'language': 'es',
                })
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_entry_translation_list_ok(self):
        # translations should be returned when logged in
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.get(
            reverse(
                'badmovieknights_api:entrytranslation-list',
                kwargs={'entry_pk': self.entry_1.pk}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned = json.loads(resp.content)
        self.assertEqual(2, len(returned))
        t1 = returned[0]
        t2 = returned[1]
        self.assertEqual(self.trans_1.id, t1['id'])
        self.assertEqual(self.trans_2.id, t2['id'])

    def test_entry_translation_list_create_ok(self):
        # test create translation ok when authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.post(
            reverse(
                'badmovieknights_api:entrytranslation-list',
                kwargs={'entry_pk': self.entry_2.pk}), {
                    'title': 'My Blog Entry 2 es',
                    'content': '# My Content 2 es',
                    'language': 'es',
                })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        returned = json.loads(resp.content)
        self.assertEqual(returned['language'], 'es')
        self.assertEqual(returned['title'], 'My Blog Entry 2 es')
        self.assertEqual(returned['content'], '# My Content 2 es')


# entry detail test case
class APIEntryTranslationDetailTestCase(BaseEntryAPITestCase):
    def test_entry_translation_detail_200(self):
        # entry translation detail should return when logged in
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.get(reverse(
            'badmovieknights_api:entrytranslation-detail',
            kwargs={'entry_pk': self.entry_1.pk, 'pk': self.trans_1.pk}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned = json.loads(resp.content)
        self.assertEqual(self.trans_1.id, returned['id'])
        self.assertEqual(self.trans_1.title, returned['title'])
        self.assertEqual(self.trans_1.content, returned['content'])

    def test_entry_translation_detail_unauthenticated_401(self):
        # translation detail should not be returned to unauthenticated users
        resp = self.client.get(reverse(
            'badmovieknights_api:entrytranslation-detail',
            kwargs={'entry_pk': self.entry_1.pk, 'pk': self.trans_1.pk}))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_entry_translation_detail_put_unauthenticated_401(self):
        # test forbidden update if unauthenticated
        resp = self.client.put(
            reverse('badmovieknights_api:entrytranslation-detail', kwargs={
                'entry_pk': self.entry_1.pk,
                'pk': self.trans_1.pk
            }), {
                'title': 'Edited', 'content': '# Edited',
                'language': self.trans_1.language
            })
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_entry_translation_detail_put_ok(self):
        # test updates ok when authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.put(
            reverse('badmovieknights_api:entrytranslation-detail', kwargs={
                'entry_pk': self.entry_1.pk,
                'pk': self.trans_1.pk,
            }), {
                'title': 'Edited', 'content': '# Edited',
                'language': self.trans_1.language
            })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned = json.loads(resp.content)
        self.assertEqual(returned['title'], 'Edited')
        self.assertEqual(returned['content'], '# Edited')

    def test_entry_translation_detail_delete_unauthenticated_401(self):
        # test forbidden delete if unauthenticated
        resp = self.client.delete(
            reverse('badmovieknights_api:entrytranslation-detail', kwargs={
                'entry_pk': self.entry_1.pk,
                'pk': self.trans_1.pk
            }))
        # check the response code is a 401 unauthorized and that the
        # object remains
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(2, len(self.entry_1.translations.all()))

    def test_entry_translation_detail_delete_ok(self):
        # test delete ok when authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        resp = self.client.delete(
            reverse('badmovieknights_api:entrytranslation-detail', kwargs={
                'entry_pk': self.entry_1.pk,
                'pk': self.trans_1.pk,
            }))
        # check the response code is good and we have one less item
        # in the entry model.
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, len(self.entry_1.translations.all()))
