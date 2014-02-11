# import lib deps
from rest_framework.serializers import ModelSerializer

# import package deps
from blog.models import Entry


# Entry serializer
class EntrySerializer(ModelSerializer):
    class Meta:
        model = Entry
        exclude = ['author']