# import django deps
from django.conf.urls import url, patterns

# import app deps
from core.views import home_view

# setup urls
urlpatterns = patterns(
    '',
    url(r'^$', home_view, name='home'),
)
