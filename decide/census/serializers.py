from rest_framework import serializers


from .models import UserData
from base.serializers import KeySerializer, AuthSerializer


class UserDataSerializer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = UserData
        fields = ('id', 'voter_id', 'born_year', 'country', 'religion',
                  'gender', 'civil_state', 'works')