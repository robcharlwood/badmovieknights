# import django deps
from django.conf.urls import patterns, url
from appengine_sessions.views import session_clean_up

# setup urls
urlpatterns = patterns(
    '',
    url(r'^clean-up/$', session_clean_up, name='session-clean-up'),
)
