
from rest_framework import serializers

class StringListSerializer(serializers.Serializer):
    voters = serializers.ListSerializer(child=serializers.CharField())
    