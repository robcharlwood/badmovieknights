# import lib deps
import mock

# import django deps
from django.db.models.signals import post_save
from django.test import TestCase
from django.contrib.auth.models import User

# import lib deps
from rest_framework.authtoken.models import Token


# test signal receivers
class CreateAuthTokenReceiverTestCase(TestCase):
    def test_create_auth_token_signal_receiver(self):
        # check that a token is created for a newly created user
        with mock.patch(
                'core.models.create_auth_token', autospec=True) as \
                mocked_handler:
            post_save.connect(
                mocked_handler,
                sender=User,
                dispatch_uid='test_create_auth_token')
            user = User.objects.create_user(
                username='rob', password='foobar')
            self.assertEqual(mocked_handler.call_count, 1)
            self.assertEqual(1, len(Token.objects.filter(user=user)))
