from rest_framework import serializers

from .models import Vote, VoteYesNo


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    a = serializers.IntegerField()
    b = serializers.IntegerField()

    class Meta:
        model = Vote
        fields = ('voting_id', 'voter_id', 'a', 'b')


class VoteYesNoSerializer(serializers.HyperlinkedModelSerializer):
    a = serializers.IntegerField()
    b = serializers.IntegerField()

    class Meta:
        model = VoteYesNo
        fields = ('voting_yesno_id', 'voter_yesno_id', 'a', 'b')