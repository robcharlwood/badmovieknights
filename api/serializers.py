# import lib deps
from rest_framework.serializers import ModelSerializer

# import package deps
from blog.models import Entry


# entry translations serializer
class EntryTranslationSerializer(ModelSerializer):
    class Meta:
        model = Entry._translation_model
        exclude = ['model_instance']


# Entry serializer
class EntrySerializer(ModelSerializer):
    translations = EntryTranslationSerializer(
        source='translations', read_only=True)

    class Meta:
        model = Entry
        exclude = ['author']
