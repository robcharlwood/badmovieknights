# import django deps
from django.conf.urls import patterns, include, url
from django.conf import settings

# set up urls
urlpatterns = patterns(
    '',

    # enable the bad movie knights api
    url(r'^api/', include('api.urls', namespace='badmovieknights_api')),

    # enable session and token auth urls
    url(r'^api/auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^api/auth/token/',
        'rest_framework.authtoken.views.obtain_auth_token')
)

# handle 404s and 500s in development mode
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^500/$', 'django.views.generic.simple.direct_to_template', {
            'template': '500.html'}, name='error-404'),
        url(r'^404/$', 'django.views.generic.simple.direct_to_template', {
            'template': '404.html'}, name='error-500'),
    )
