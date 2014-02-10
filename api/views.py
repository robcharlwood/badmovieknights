# import lib deps
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# import project deps
from blog.models import Entry
from api.serializers import EntrySerializer


# entry api view mixin
class EntryViewMixin(object):
    """
        Mixin to handle generic functionality
        between EntryList and EntryDetail API views.
    """
    model = Entry
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def pre_save(self, obj):
        """
            Force author to the current user on save
        """
        obj.author = self.request.user
        return super(EntryViewMixin, self).pre_save(obj)


# entry list view
class EntryList(EntryViewMixin, ListCreateAPIView):
    """
        API end point to list all published entries
        and create new entries
    """
    pass


# entry detail view
class EntryDetail(EntryViewMixin, RetrieveUpdateDestroyAPIView):
    """
        API end point to retrieve, update or delete an
        individual entry
    """
    pass
