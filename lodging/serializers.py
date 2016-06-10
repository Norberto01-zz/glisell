from rest_framework import serializers
from lodging.models import Lodging


class LodgingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lodging
        fields = ('id', 'title')
