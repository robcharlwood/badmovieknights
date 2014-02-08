# import django deps
from django.conf.urls import url, patterns
from django.conf import settings

# urls
urlpatterns = patterns('')

# handle 404s and 500s in development mode
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^500/$', 'django.views.generic.simple.direct_to_template', {
            'template': '500.html'}),
        url(r'^404/$', 'django.views.generic.simple.direct_to_template', {
            'template': '404.html'}),
    )
