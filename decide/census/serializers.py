
from rest_framework import serializers

from .models import Census, UserData

class StringListSerializer(serializers.Serializer):
    voters = serializers.ListSerializer(child=serializers.CharField())

class CensusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Census
        fields = '__all__'    


class UserDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserData
        fields = ('id', 'voter_id', 'born_year', 'country', 'religion',
                  'gender', 'civil_state', 'works')

