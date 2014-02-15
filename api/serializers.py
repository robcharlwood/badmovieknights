# import lib deps
from rest_framework import serializers

# import package deps
from blog.models import Entry


# entry translations serializer
class EntryTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry._translation_model
        exclude = ['model_instance']


# Entry serializer
class EntrySerializer(serializers.ModelSerializer):
    translations = EntryTranslationSerializer(
        source='translations', read_only=True)
    creation_date = serializers.DateTimeField(read_only=True)
    last_update = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Entry
        exclude = ['author']
