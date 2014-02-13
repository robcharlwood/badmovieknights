# import django deps
from django.conf.urls import patterns, url, include

# import lib deps
from rest_framework_nested import routers

# import project deps
from api.views import EntryViewSet, EntryTranslationViewSet

# create api routers
router = routers.SimpleRouter()
router.register(r'entry', EntryViewSet)
translation_router = routers.NestedSimpleRouter(
    router, r'entry', lookup='entry')
translation_router.register(
    r'translations', EntryTranslationViewSet)

# setup the urls
urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^', include(translation_router.urls)),
)
