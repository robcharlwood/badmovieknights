# import django deps
from django.utils import translation

# import rest framework deps
from rest_framework import serializers
from markdown import markdown


# read only translation field
class TranslationField(serializers.Field):
    """
        Translation serializer field checks current language,
        looks for the relevant translation for the object and
        returns it if found. If there is no translation for the
        requested entry then english is returned.

        Optionally you can pass a method into this for post
        processing on a translated field
    """
    def __init__(self, markdown=False):
        self.markdown = markdown
        super(TranslationField, self).__init__()

    def field_to_native(self, obj, field_name):
        lang = translation.get_language()
        trans_fields = \
            obj._translation_model._transmeta.translatable_fields
        trans = None
        data = getattr(obj, field_name)
        if field_name in trans_fields:
            try:
                trans = obj.translations.get(language=lang)
            except obj._translation_model.DoesNotExist:
                pass
        if trans:
            data = getattr(trans, field_name)
        if self.markdown:
            data = markdown(data)
        return self.to_native(data)
