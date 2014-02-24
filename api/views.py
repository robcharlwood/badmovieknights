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
            If not authenticated return read only serializer regardless
            of request method.

            If authenticated GET call is made that is not
            in edit mode then we render the read only serializer
            (admin preview mode).

            if authenticated PUT call is made with a file upload then
            we return the entry image serializer

            In all other authenticated calls that haven't been covered
            above then the standard entry serializer is returned
        """
        if self.request.user.is_authenticated():

            # authenticated and previewing an entry
            if self.request.method == u'GET' and \
                    self.request.GET.get('edit_mode', None) is None:
                return EntryReadOnlySerializer

            # authenticated and uploading image file
            if self.request.method == u'PUT' and len(self.request.FILES) > 0:
                return EntryImageSerializer

            # if we make it here, then we are either POST, DELETE or PUT
            # (with no image)
            return EntrySerializer

        # if we get this far we are unauthenticated
        return EntryReadOnlySerializer

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
