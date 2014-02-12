# import python deps
import copy

# import django deps
from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# import c3po deps
from c3po.exceptions import AlreadyRegistered


# create registry class
class C3PORegistry(object):
    """
        Registration class used to register models
        for translation
    """
    def __init__(self):
        self._registry = {}
        self._models = {}

    # registration method
    def register(self, model, trans_class):
        """
            Registers the given model for use with c3po translation system.
            The model should be Model classes, not instances.
            If a model is already registered, this will raise
            AlreadyRegistered exception.
        """
        assert hasattr(model, '_meta'), 'Model must derive from Model.'

        # check if model is already registered
        if model in self._registry:
            raise AlreadyRegistered(
                u'The model %s.%s is already registered! Registry dump: %s' % (
                    model.__module__,
                    model.__name__,
                    self.get_registered_models()
                )
            )

        # setup translations model
        opts = trans_class(model)
        trans_model = self._create_translation_model(model, opts)
        models.register_models(model._meta.app_label, trans_model)

        # Clear related object caches so that Django reprocesses objects.
        model._meta._fill_related_objects_cache()
        model._meta.init_name_map()

        # Configured and register the multilingual model and the
        # translation_class.
        model._translation_model = trans_model
        self._registry[model] = opts

    def get_registered_models(self):
        """
            Returns a list of all the models registered
        """
        return self._registry.keys()

    def _create_translation_model(self, model, opts):
        """
            Creates a model for storing `model`'s translations based on
            given registration trans options class.
        """
        attrs = {'__module__': model.__module__}

        # create meta classes for the model
        class Meta:
            app_label = model._meta.app_label
            db_table = opts.db_table
            unique_together = (('model_instance', 'language', 'context'))
        attrs['Meta'] = Meta

        class TranslationMeta:
            translatable_fields = opts.attributes
            related_name = opts.related_name
        attrs['_transmeta'] = TranslationMeta

        # give translation objects some meaning
        def __unicode__(self):
            return (
                u'translation_model:%s master_model:%s '
                'master_model_instance_id:%s language:%s' % (
                    self.__class__,
                    model,
                    self.model_instance.id,
                    self.language
                ))
        attrs['__unicode__'] = __unicode__

        # Common translation model fields
        common_fields = {
            'language': models.CharField(
                db_index=True,
                verbose_name='language',
                max_length=10,
                choices=settings.LANGUAGES[1:]),
            'model_instance': models.ForeignKey(
                model, verbose_name='model', related_name=opts.related_name),
        }
        attrs.update(common_fields)

        # Add translatable fields
        model_name = model.__name__ + 'Translation'
        for field in model._meta.fields:
            if field.name not in opts.attributes:
                continue
            if field.name in common_fields:
                raise ImproperlyConfigured(
                    '%s: %s field name "%s" conflicts with the language or '
                    'model instance foreign key common fields'
                    % (model_name, model.__name__, field.attname))
            newfield = copy.copy(field)

            # first make sure that our newfield is not unique since we may
            # have two languages with the same translation for a particular
            # field. Next we ensure that the field isnt marked as a primary
            # key field.
            if newfield._unique is True:
                newfield._unique = False
            newfield.primary_key = False
            attrs[newfield.name] = newfield

        # return the new model
        return type(model_name, (models.Model,), attrs)

# registry object - only one instance globally
c3po = C3PORegistry()
