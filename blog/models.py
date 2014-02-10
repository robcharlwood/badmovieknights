# import django deps
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User

# import lib deps
from markdown import markdown

# import project deps
from blog.managers import EntryManager


# entry model
class Entry(models.Model):
    """
        Blog Entry model
    """
    author = models.ForeignKey(User)
    title = models.CharField(_('Title'), max_length=255)
    creation_date = models.DateTimeField(
        _('Creation date'), default=timezone.now,
        help_text=_("Used to build the entry's URL."))
    last_update = models.DateTimeField(
        _('Last update'), default=timezone.now)
    content = models.TextField(_('Content'))
    published = models.BooleanField(
        default=False, verbose_name=_('Published'),
        help_text=_(u'Mark entry as published'))
    objects = EntryManager()

    def __unicode__(self):
        return u'%s - %s' % (self.title, self.creation_date)

    @property
    def html_content(self):
        """
            Returns the "content" field as HTML.
            using the markdown library
        """
        return markdown(self.content)

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
