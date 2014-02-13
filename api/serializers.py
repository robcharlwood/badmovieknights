# import lib deps
from rest_framework.serializers import ModelSerializer

# import package deps
from blog.models import Entry


# Entry serializer
class EntrySerializer(ModelSerializer):
    class Meta:
        model = Entry
        exclude = ['author']


# entry translations serializer
class EntryTranslationSerializer(ModelSerializer):
    class Meta:
        model = Entry._translation_model
        exclude = ['model_instance']
