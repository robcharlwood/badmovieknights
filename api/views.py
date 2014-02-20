# import lib deps
from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated)

# import project deps
from blog.models import Entry
from api.serializers import (
    EntrySerializer, EntryImageSerializer,
    EntryReadOnlySerializer, EntryTranslationSerializer)


# entry api view mixin
class EntryViewSet(viewsets.ModelViewSet):
    """
        API end point to list/retieve/create/put/delete
        entries. Allows read only when not logged in.
        Will return unpublished entries to logged in user
    """
    model = Entry
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """
            Use a different serializer depending on
            whether we are getting or creating/updating/deleting
        """
        if self.request.method == u'GET' \
                and not self.request.user.is_authenticated():
            return EntryReadOnlySerializer
        if self.request.method == u'PUT' and len(self.request.FILES) > 0:
            return EntryImageSerializer
        return EntrySerializer

    def get_queryset(self):
        """
            Return published and unpublished entries
            for authenticated api calls
        """
        if self.request.user.is_authenticated():
            return Entry.objects.all()
        return Entry.objects.get_published()

    def pre_save(self, obj):
        """
            Force author to the current user on save
        """
        obj.author = self.request.user
        return super(EntryViewSet, self).pre_save(obj)


# entry translation list view
class EntryTranslationViewSet(viewsets.ModelViewSet):
    """
        API end point to list/retieve/create/put/delete
        translations for an entry
    """
    model = Entry._translation_model
    serializer_class = EntryTranslationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(
            model_instance=self.kwargs['entry_pk'])

    def pre_save(self, obj):
        """
            Force model_instance to point to the correct
            model instance
        """
        obj.model_instance = Entry.objects.get(pk=self.kwargs['entry_pk'])
        return super(EntryTranslationViewSet, self).pre_save(obj)
