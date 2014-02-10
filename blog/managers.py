# import django deps
from django.db import models


# entry manager
class EntryManager(models.Manager):
    def get_query_set(self):
        """
            Override get query set and put in some select related optimisations
            on relationships we know we will be traversing regularly. This will
            also only return published entries
        """
        return super(EntryManager, self).get_query_set().select_related(
            'author').filter(published=True).order_by('-creation_date')
