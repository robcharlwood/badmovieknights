# import django deps
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User

# import lib deps
from markdown import markdown

# import project deps
from blog.managers import EntryManager
from c3po.options import ModelTranslationOptions
from c3po.registry import c3po


# entry model
class Entry(models.Model):
    """
        Blog Entry model
    """
    author = models.ForeignKey(User)
    title = models.CharField(_('Title'), max_length=255)
    image = models.ImageField(
        _('Image'), max_length=255, blank=True, upload_to='images')
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

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')


# define translation options for Entry
class EntryTranslationOptions(ModelTranslationOptions):
    """
        Let's make title and content translatable
    """
    attributes = ['title', 'content']

# now we register our model and trans option with c3po
# c3po is human cyborg relations and is fluent in over
# 6 million... er 2 languages. :)
c3po.register(Entry, EntryTranslationOptions)
