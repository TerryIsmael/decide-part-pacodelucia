from django.utils import timezone
from django.utils.dateparse import parse_datetime
import django_filters.rest_framework
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from voting.models import VotingByPreference, VotingYesNo
from .models import Vote, VoteByPreference, VoteYesNo
from .serializers import VoteSerializer, VoteByPreferenceSerializer,VoteYesNoSerializer
from base import mods
from base.perms import UserIsStaff, UserIsAdminToken


class StoreView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('voting_id', 'voter_id')

    def get(self, request):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        return super().get(request)

    def post(self, request):
        """
         * voting: id
         * voter: id
         * vote: { "a": int, "b": int }
        """

        vid = request.data.get('voting')
        voting = mods.get('voting', params={'id': vid})
        if not voting or not isinstance(voting, list):
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        start_date = voting[0].get('start_date', None)
        # print ("Start date: "+  start_date)
        end_date = voting[0].get('end_date', None)
        #print ("End date: ", end_date)
        not_started = not start_date or timezone.now() < parse_datetime(start_date)
        #print (not_started)
        is_closed = end_date and parse_datetime(end_date) < timezone.now()
        if not_started or is_closed:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        uid = request.data.get('voter')
        vote = request.data.get('vote')

        if not vid or not uid or not vote:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # validating voter
        if request.auth:
            token = request.auth.key
        else:
            token = "NO-AUTH-VOTE"
        voter = mods.post('authentication', entry_point='/getuser/', json={'token': token})
        voter_id = voter.get('id', None)
        if not voter_id or voter_id != uid:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census
        perms = mods.get('census/{}'.format(vid), params={'voter_id': uid}, response=True)
        if perms.status_code == 401:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        a = vote.get("a")
        b = vote.get("b")
   
        defs = { "a": a, "b": b }
        v, _ = Vote.objects.get_or_create(voting_id=vid, voter_id=uid,
                                          defaults=defs)
        v.a = a
        v.b = b

        v.save()

        return  Response({})

    def delete(self, request):
        voteId = request.data.get('id')
        vote = get_object_or_404(Vote, pk=voteId) 
        vote.delete()
        return Response({"Eliminado correctamente"})

class StoreFrontView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('voting_id', 'voter_id')
    permission_classes = (UserIsAdminToken,)

    def get(self, request):
        self.check_permissions(request)
        return super().get(request)
    
    def delete(self, request):
        voteId = request.data.get('id')
        vote = get_object_or_404(Vote, pk=voteId) 
        vote.delete()
        return Response({"Eliminado correctamente"})

class StoreByPreferenceView(generics.ListAPIView):
    queryset = VoteByPreference.objects.all()
    serializer_class = VoteByPreferenceSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('voting_by_preference_id', 'voter_by_preference_id')
    
    def get(self, request):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        return super().get(request)
      
    def post(self, request):
        """
         * voting: id
         * voter: id
         * vote: { "a": int, "b": int }
        """
        vid = request.data.get('voting')
        voting = mods.get('voting', params={'id': vid})
        auxvoting = VotingByPreference.objects.get(id=vid)
        voting = []
        voting_data = {
                'id': auxvoting.id,
                'name': auxvoting.name,
                'desc': auxvoting.desc,
                'question': {
                    'desc': auxvoting.question.desc,
                    'options': [{'number': o.number, 'option': o.option, 'preference': o.preference} for o in auxvoting.question.options.all()]
                },
                'start_date': auxvoting.start_date.isoformat(),
                'end_date': auxvoting.end_date.isoformat() if auxvoting.end_date else None,
                'pub_key': {
                    'p': auxvoting.pub_key.p,
                    'g': auxvoting.pub_key.g,
                    'y': auxvoting.pub_key.y,
                },
                'auths': [{'name': a.name, 'url': a.url, 'me': a.me} for a in auxvoting.auths.all()],
                'tally': None,
                'postproc': None
            }
        voting.append(voting_data)
        if not voting or not isinstance(voting, list):
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        start_date = voting[0].get('start_date', None)
        # print ("Start date: "+  start_date)
        end_date = voting[0].get('end_date', None)
        #print ("End date: ", end_date)
        not_started = not start_date or timezone.now() < parse_datetime(start_date)
        #print (not_started)
        is_closed = end_date and parse_datetime(end_date) < timezone.now()
        if not_started or is_closed:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        uid = request.data.get('voter')
        vote = request.data.get('vote')

        if not vid or not uid or not vote:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # validating voter
        if request.auth:
            token = request.auth.key
        else:
            token = "NO-AUTH-VOTE"
        voter = mods.post('authentication', entry_point='/getuser/', json={'token': token})
        voter_id = voter.get('id', None)
        if not voter_id or voter_id != uid:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census
        perms = mods.get('custom/census/censuspreference/{}'.format(vid), params={'voter_id': uid}, response=True)
        if perms.status_code == 401:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        a = vote.get("a")
        b = vote.get("b")

        defs = { "a": a, "b": b }
        v, _ = VoteByPreference.objects.get_or_create(voting_by_preference_id=vid, voter_by_preference_id=uid,
                                          defaults=defs)
        v.a = a
        v.b = b

        v.save()

        return  Response({})

    def delete(self, request):
        voteId = request.data.get('id')
        vote = get_object_or_404(Vote, pk=voteId) 
        vote.delete()
        return Response({"Eliminado correctamente"})
    
class StoreYesNoView(generics.ListAPIView):
    queryset = VoteYesNo.objects.all()
    serializer_class = VoteYesNoSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('voting_yesno_id', 'voter_yesno_id')


    def get(self, request):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        return super().get(request)

    def post(self, request):
        """
         * voting: id
         * voter: id
         * vote: { "a": int, "b": int }
        """
        voting = []
        vid = request.data.get('voting')
        voting_yesno = VotingYesNo.objects.get(id=vid)
        voting_data = {
            'id': voting_yesno.id,
            'name': voting_yesno.name,
            'desc': voting_yesno.desc,
            'question': {
                'desc': voting_yesno.question.desc,
                'optionYes': voting_yesno.question.optionYes,
                'optionNo': voting_yesno.question.optionNo,
            },
            'start_date': voting_yesno.start_date.isoformat(),
            'end_date': voting_yesno.end_date.isoformat() if voting_yesno.end_date else None,
            'pub_key': {
                'p': voting_yesno.pub_key.p,
                'g': voting_yesno.pub_key.g,
                'y': voting_yesno.pub_key.y,
            },
            'auths': [{'name': a.name, 'url': a.url, 'me': a.me} for a in voting_yesno.auths_yesno.all()],
            'tally': voting_yesno.tally,
            'postproc': voting_yesno.postproc,
        }
        voting.append(voting_data)

        if not voting or not isinstance(voting, list):
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        start_date = voting[0].get('start_date', None)
        # print ("Start date: "+  start_date)
        end_date = voting[0].get('end_date', None)
        #print ("End date: ", end_date)
        not_started = not start_date or timezone.now() < parse_datetime(start_date)
        #print (not_started)
        is_closed = end_date and parse_datetime(end_date) < timezone.now()
        if not_started or is_closed:

            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        uid = request.data.get('voter')
        vote = request.data.get('vote')

        if not vid or not uid or not vote:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # validating voter
        if request.auth:
            token = request.auth.key
        else:
            token = "NO-AUTH-VOTE"
        voter = mods.post('authentication', entry_point='/getuser/', json={'token': token})
        voter_id = voter.get('id', None)
        if not voter_id or voter_id != uid:

            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census
        #perms = mods.get('census/yesno/', params={'voter_id': uid}, response=True)
        perms = mods.get('custom/census/censusyesno/{}'.format(vid), params={'voter_id': uid}, response=True)
        if perms.status_code == 401:

            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        a = vote.get("a")
        b = vote.get("b")

        defs = { "a": a, "b": b }
        v, _ = VoteYesNo.objects.get_or_create(voting_yesno_id=vid, voter_yesno_id=uid,

                                          defaults=defs)
        v.a = a
        v.b = b

        v.save()

        return  Response({})
