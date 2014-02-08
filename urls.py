# import django deps
from django.conf.urls import patterns, include, url

# set up urls
urlpatterns = patterns(
    '',
    (r'', include('core.urls')),
    url(r'^api/auth/', include(
        'rest_framework.urls', namespace='rest_framework'))
)
