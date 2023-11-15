
from rest_framework import serializers

from .models import Census

class StringListSerializer(serializers.Serializer):
    voters = serializers.ListSerializer(child=serializers.CharField())

class CensusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Census
        fields = '__all__'    