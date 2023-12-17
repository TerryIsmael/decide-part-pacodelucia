
from rest_framework import serializers
from .models import Census, UserData


class StringListSerializer(serializers.Serializer):
    voters = serializers.ListSerializer(child=serializers.CharField())

class CensusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Census
        fields = ('id','voting_id', 'voter_id')

class UserDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserData
        fields = ('id', 'voter_id', 'born_year', 'country', 'religion',
                  'gender', 'civil_state', 'works')


class CensusReuseSerializer(serializers.Serializer):
    source_voting_id = serializers.IntegerField()
    destination_voting_id = serializers.IntegerField()
