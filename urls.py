# import django deps
from django.conf.urls import patterns, include

# set up urls
urlpatterns = patterns(
    '',
    (r'^appengine_sessions/', include('appengine_sessions.urls')),
    (r'', include('core.urls')),
)
