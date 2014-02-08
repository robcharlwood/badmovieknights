# import django deps
from django.conf.urls import patterns, include

# set up urls
urlpatterns = patterns(
    '',
    (r'', include('core.urls')),
)
