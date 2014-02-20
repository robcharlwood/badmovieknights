# import lib deps
from rest_framework import serializers

# import django deps
from django.utils.translation import ugettext_lazy as _

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

    def validate_language(self, attrs, source):
        """
            Check we dont already have a translation for this entry.
            This would normally be handled by rest framework standard
            serializer validation. However, I didn't want to have to
            pass model instance in my API calls from Angular and wanted
            the API to auto-detect entry using the nested router urls.
        """
        view = self.context.get('view')
        entry_pk = view.kwargs.get('entry_pk')
        trans_pk = view.kwargs.get('pk', None)

        # this check should only be done for new translation objects. :-)
        if not trans_pk:
            try:
                Entry._translation_model.objects.get(
                    language=attrs[source], model_instance__pk=entry_pk)
            except Entry._translation_model.DoesNotExist:
                return attrs
            raise serializers.ValidationError(
                _(u"%s translation already exists for this entry" % (
                    attrs[source])))
        return attrs


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
        exclude = [
            'author', 'creation_date', 'last_update', 'image']


# entry image serializer
class EntryImageSerializer(serializers.ModelSerializer):
    """
        We need to handle image upload with a different serializer
        due to angularjs being a bit naff with file uploads.
        TODO: Contribute to angularjs docs on file upload!
    """
    class Meta:
        model = Entry
        fields = ['image']


# Entry read only serializer
class EntryReadOnlySerializer(serializers.ModelSerializer):
    """
        Serializer for standard read-only API calls to entry.
        Formats dates accordingly.
    """
    title = TranslationField()
    content = TranslationField(markdown=True)
    creation_date = serializers.DateTimeField(
        format="%d %b %Y", read_only=True)
    last_update = serializers.DateTimeField(
        format="%d %b %Y", read_only=True)
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
