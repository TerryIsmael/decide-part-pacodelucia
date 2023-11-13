from django.utils import timezone
from django.utils.dateparse import parse_datetime
import django_filters.rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from .models import Vote, VoteYesNo
from voting.models import VotingYesNo
from .serializers import VoteSerializer,VoteYesNoSerializer
from base import mods
from base.perms import UserIsStaff


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
            # print("por aqui 35")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        start_date = voting[0].get('start_date', None)
        # print ("Start date: "+  start_date)
        end_date = voting[0].get('end_date', None)
        #print ("End date: ", end_date)
        not_started = not start_date or timezone.now() < parse_datetime(start_date)
        #print (not_started)
        is_closed = end_date and parse_datetime(end_date) < timezone.now()
        if not_started or is_closed:
            #print("por aqui 42")
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
            # print("por aqui 59")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census
        perms = mods.get('census/{}'.format(vid), params={'voter_id': uid}, response=True)
        if perms.status_code == 401:
            # print("por aqui 65")
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
            'tally': None,
            'postproc': None
        }
        voting.append(voting_data)

        if not voting or not isinstance(voting, list):
            # print("por aqui 35")
            print("PUEDE SER LA LINEA 131")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        start_date = voting[0].get('start_date', None)
        # print ("Start date: "+  start_date)
        end_date = voting[0].get('end_date', None)
        #print ("End date: ", end_date)
        not_started = not start_date or timezone.now() < parse_datetime(start_date)
        #print (not_started)
        is_closed = end_date and parse_datetime(end_date) < timezone.now()
        if not_started or is_closed:
            #print("por aqui 42")
            print("PUEDE SER LA LINEA 142")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        uid = request.data.get('voter')
        vote = request.data.get('vote')

        if not vid or not uid or not vote:
            print("PUEDE SER LA LINEA 149")
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # validating voter
        if request.auth:
            token = request.auth.key
        else:
            token = "NO-AUTH-VOTE"
        voter = mods.post('authentication', entry_point='/getuser/', json={'token': token})
        voter_id = voter.get('id', None)
        if not voter_id or voter_id != uid:
            # print("por aqui 59")
            print("PUEDE SER LA LINEA 160")
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census
        perms = mods.get('census/{}'.format(vid), params={'voter_id': uid}, response=True)
        if perms.status_code == 401:
            # print("por aqui 65")
            print("PUEDE SER LA LINEA 167")
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
