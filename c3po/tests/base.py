# import django deps
from django.db import models
from django.utils.translation import ugettext_lazy as _

# import c3po deps
from c3po.options import ModelTranslationOptions


# create a mock class which will represent something which is not a model
class MockNotAModel(object):
    test_field_1 = 'foobar'


# create a mock class to represent a model
class MockModel(models.Model):
    """
        Mock model with a couple of text fields
    """
    test_field_1 = models.CharField(_('test_field_1'), max_length=200)
    test_field_2 = models.TextField(_('test_field_2'), blank=True)

    def __unicode__(self):
        return u'%s' % self.test_field_1


# create a mock class to represent a model with translation field that
# conflicts with c3po's translation reserved field names
class MockModelReservedFieldName(models.Model):
    """
        Mock model with a couple of text fields
    """
    language = models.CharField(_('language'), max_length=200)

    def __unicode__(self):
        return u'%s' % self.language


# mock model options
class MockModelOptions(ModelTranslationOptions):
    """
        Subclass to define fields for translation
    """
    attributes = ('test_field_1', 'test_field_2')


# mock model options
class MockModelReservedOptions(ModelTranslationOptions):
    """
        options that try to use a reserved field name
    """
    attributes = ('language')


# mock model with unique fields
class MockModelUnique(models.Model):
    """
        We mark ``test_field_1`` as unique. This is so that we can test that
        when a translation model is generated this model, that ``test_field_1``
        is not unique in the translation model. This is because two different
        languages may have the same translation string for an object and so
        we shouldn't be enforcing ``unique`` on any translation fields in
        the translation model except a ``unique_together`` on language and
        model instance.
    """
    test_field_1 = models.CharField(
        _('test_field_1'), max_length=200, unique=True)
    test_field_2 = models.TextField(_('test_field_2'), blank=True)

    def __unicode__(self):
        return u'%s' % self.test_field_1
