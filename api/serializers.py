# import lib deps
from rest_framework import serializers

# import package deps
from blog.models import Entry
from api.fields import TranslationField


# entry translations serializer
class EntryTranslationSerializer(serializers.ModelSerializer):
    """
        entry translations serializer
    """
    class Meta:
        model = Entry._translation_model
        exclude = ['model_instance']


# entry CRUD serializer
class EntrySerializer(serializers.ModelSerializer):
    """
        This serializer is rendered for POST/PUT/DELETE
        requests. The reason for having a seperate admin
        and read-only serializers is because we need to
        format and process data differently for admins
    """
    class Meta:
        model = Entry
        exclude = ['author', 'creation_date', 'last_update']


# Entry read only serializer
class EntryReadOnlySerializer(serializers.ModelSerializer):
    """
        Serializer for standard read-only API calls to entry.
    """
    title = TranslationField()
    content = TranslationField(markdown=True)
    creation_date = serializers.DateTimeField(read_only=True)
    last_update = serializers.DateTimeField(read_only=True)
    author = serializers.SerializerMethodField('get_author')
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Entry
        exclude = ['published']

    def get_author(self, obj):
        """
            Return the author of the blog
        """
        return obj.author.username

    def get_image_url(self, obj):
        """
            Returns a full qualified url for angularjs app
        """
        if obj.image:
            return obj.image.url
        return ''
