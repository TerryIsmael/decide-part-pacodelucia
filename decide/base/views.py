from django.shortcuts import render
from django.db.utils import IntegrityError
from base.perms import UserIsAdminToken
from base.models import Auth
from voting.models import VotingByPreference, VotingYesNo
from base.serializers import AuthSerializer
from rest_framework import generics
import django_filters.rest_framework
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_409_CONFLICT as ST_409
)

class AllAuthsAPIView(generics.ListAPIView):

    permission_classes = (UserIsAdminToken,)
    serializer_class = AuthSerializer
    queryset = Auth.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def post(self, request, *args, **kwargs):

        auth_id = None
        name = request.data.get('name')
        url = request.data.get('url')
        me = request.data.get('me')

        try:
            if (request.data.get('id') is not None):
                auth_id = request.data.get('id')
                auth = Auth(id=auth_id, name=name, url=url, me=me)
            else:
                auth = Auth(name=name, url=url, me=me)
            auth.save()

        except IntegrityError:
            return Response('Error trying to create Auth', status=ST_409)
        
        return Response('Auths created', status=ST_201)

    def delete(self, request, *args, **kwargs):

        auth_id = request.data.get('id')

        try:
            auth = Auth.objects.get(id=auth_id)
            votings = VotingByPreference.objects.filter(auths=auth)
            for voting in votings:
                voting.auths.remove(auth)
                voting.save()
            votings = VotingYesNo.objects.filter(auths_yesno=auth)
            for voting in votings:
                voting.auths_yesno.remove(auth)
                voting.save()
            auth.delete()
        except Auth.DoesNotExist:
            return Response('Auth does not exist', status=ST_400)

        return Response('Auth deleted', status=ST_204)