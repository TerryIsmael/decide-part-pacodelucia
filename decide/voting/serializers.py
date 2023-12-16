from rest_framework import serializers
from .models import Question, QuestionOption,QuestionByPreference, QuestionOptionByPreference, VotingByPreference, Voting, VotingYesNo,QuestionYesNo
from base.serializers import KeySerializer, AuthSerializer


class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ('number', 'option')

class QuestionOptionByPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionOptionByPreference
        fields = ('number', 'option','preference')

class QuestionByPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    options = QuestionOptionByPreferenceSerializer(many=True)
    class Meta:
        model = QuestionByPreference
        fields = ('desc', 'options')

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = QuestionOptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ('desc', 'options')

class QuestionYesNoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = QuestionYesNo
        fields = ('desc', 'optionYes', 'optionNo')


class VotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = Voting
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc')

class VotingByPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionByPreferenceSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = VotingByPreference
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc')


class SimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = Voting
        fields = ('name', 'desc', 'question', 'start_date', 'end_date')

class SimpleVotingByPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionByPreferenceSerializer(many=False)

    class Meta:
        model = VotingByPreference
        fields = ('name', 'desc', 'question', 'start_date', 'end_date')        

class SimpleVotingYesNoSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionYesNoSerializer(many=False)

    class Meta:
        model = VotingYesNo
        fields = ('name', 'desc', 'question', 'start_date', 'end_date')

class VotingYesNoSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionYesNoSerializer(many=False)
    pub_key = KeySerializer()
    auths_yesno = AuthSerializer(many=True)
    class Meta:
        model = VotingYesNo
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths_yesno', 'tally', 'postproc')

