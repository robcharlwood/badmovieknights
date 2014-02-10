# import django deps
from django.conf.urls import patterns, url

# import project deps
from api.views import EntryDetail, EntryList

# set up api urls
urlpatterns = patterns(
    '',
    url(r'^entry/(?P<pk>\d+)/$', EntryDetail.as_view(), name='entry_detail'),
    url(r'^entry/$', EntryList.as_view(), name='entry_list')
)
