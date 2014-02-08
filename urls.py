# import django deps
from django.conf.urls import patterns, include, url
from django.conf import settings

# set up urls
urlpatterns = patterns(
    '',
    (r'', include('core.urls')),
    url(r'^api/auth/', include(
        'rest_framework.urls', namespace='rest_framework'))
)

# handle 404s and 500s in development mode
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^500/$', 'django.views.generic.simple.direct_to_template', {
            'template': '500.html'}),
        url(r'^404/$', 'django.views.generic.simple.direct_to_template', {
            'template': '404.html'}),
    )
