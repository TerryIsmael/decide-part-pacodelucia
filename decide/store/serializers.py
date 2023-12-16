from rest_framework import serializers
from .models import Vote, VoteByPreference, VoteYesNo



class VoteSerializer(serializers.HyperlinkedModelSerializer):
    a = serializers.IntegerField()
    b = serializers.IntegerField()

    class Meta:
        model = Vote
        fields = ('voting_id', 'voter_id', 'a', 'b')


class VoteByPreferenceSerializer(serializers.HyperlinkedModelSerializer):
      a = serializers.IntegerField()
      b = serializers.IntegerField()
      
      class Meta:
        model = VoteByPreference
        fields = ('voting_by_preference_id', 'voter_by_preference_id', 'a', 'b')


class VoteYesNoSerializer(serializers.HyperlinkedModelSerializer):

    a = serializers.IntegerField()
    b = serializers.IntegerField()

    class Meta:
        model = VoteYesNo
        fields = ('voting_yesno_id', 'voter_yesno_id', 'a', 'b')

