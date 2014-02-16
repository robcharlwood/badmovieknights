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
    html_content = serializers.SerializerMethodField('convert_markdown')
    author = serializers.SerializerMethodField('get_author')
    image_full_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Entry

    def convert_markdown(self, obj):
        """
            Convert content markdown field to html
        """
        return obj.html_content

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
