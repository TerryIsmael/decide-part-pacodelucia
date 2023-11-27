import django_filters.rest_framework
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from store.models import Vote 
from .models import Question, QuestionOption, Voting
from .serializers import SimpleVotingSerializer, VotingSerializer, QuestionSerializer
from base.serializers import AuthSerializer
from base.perms import UserIsStaffOrAdmin, UserIsStaff
from base.models import Auth


class VotingView(generics.ListCreateAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('id', )

    def get(self, request, *args, **kwargs):
        idpath = kwargs.get('voting_id')
        self.queryset = Voting.objects.all()
        version = request.version
        if version not in settings.ALLOWED_VERSIONS:
            version = settings.DEFAULT_VERSION
        if version == 'v2':
            self.serializer_class = SimpleVotingSerializer

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        for data in ['name', 'desc', 'question', 'question_opt']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        question = Question(desc=request.data.get('question'))
        question.save()
        for idx, q_opt in enumerate(request.data.get('question_opt')):
            opt = QuestionOption(question=question, option=q_opt, number=idx)
            opt.save()
        voting = Voting(name=request.data.get('name'), desc=request.data.get('desc'),
                question=question)
        voting.save()

        auth, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        auth.save()
        voting.auths.add(auth)
        return Response({}, status=status.HTTP_201_CREATED)


class VotingUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (UserIsStaff,)

    def put(self, request, voting_id, *args, **kwars):
        action = request.data.get('action')
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting = get_object_or_404(Voting, pk=voting_id)
        msg = ''
        st = status.HTTP_200_OK
        if action == 'start':
            if voting.start_date:
                msg = 'Voting already started'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.start_date = timezone.now()
                voting.save()
                msg = 'Voting started'
        elif action == 'stop':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.end_date:
                msg = 'Voting already stopped'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.end_date = timezone.now()
                voting.save()
                msg = 'Voting stopped'
        elif action == 'tally':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = 'Voting is not stopped'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.tally:
                msg = 'Voting already tallied'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.tally_votes(request.auth.key)
                msg = 'Voting tallied'
        else:
            msg = 'Action not found, try with start, stop or tally'
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)
    
class AllQuestionsView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer 
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        self.queryset = Question.objects.all()
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaffOrAdmin,)
        self.check_permissions(request)
        for data in ['desc', 'options']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('id'):
            question = Question(desc=request.data.get('desc'))
        else:
            question = Question.objects.filter(id=request.data.get('id')).first()
        question.desc = request.data.get('desc')
        question.save()
        newOpts=[]
        for opt in request.data.get('options'):
            if not 'id' in opt:
                option = QuestionOption(question=question, option=opt['option'], number=opt['number'])   
            else:
                option = QuestionOption.objects.filter(id=opt['id']).first()
                option.option = opt['option']
                option.number = opt['number']
            option.save()  
            newOpts.append(option)
        QuestionOption.objects.filter(question=question).exclude(id__in=[o.id for o in newOpts]).delete()
        
        return Response({}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=request.data.get('id'))
        question.delete()
        return Response({}, status=status.HTTP_200_OK)

class AllAuthsAPIView(generics.ListAPIView):
    queryset = Auth.objects.all()
    serializer_class = AuthSerializer
    permission_classes = [permissions.IsAdminUser]

class VotingFrontView(generics.ListCreateAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('id', )

    def get(self, request, *args, **kwargs):
        
        idpath = kwargs.get('voting_id')
        self.queryset = Voting.objects.all()
        version = request.version
        if version not in settings.ALLOWED_VERSIONS:
            version = settings.DEFAULT_VERSION
        if version == 'v2':
            self.serializer_class = SimpleVotingSerializer

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        self.permission_classes = (UserIsStaffOrAdmin,)
        self.check_permissions(request)
        for data in ['name', 'desc', 'question', 'auths']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            
        question = Question.objects.get(id=request.data.get('question'))
        if not request.data.get("id"):
            voting = Voting(name=request.data.get('name'), desc=request.data.get('desc'),
                    question=question)
        else:
            voting = Voting.objects.get(id=request.data.get('id'))
            voting.name = request.data.get('name')
            voting.desc = request.data.get('desc')
            voting.question = question
        voting.save()
        authsIds = request.data.get('auths')
        auths = Auth.objects.filter(id__in=authsIds)

        voting.auths.set(auths)

        return Response({}, status=status.HTTP_201_CREATED)
    
    def put(self, request, *args, **kwars):

        action = request.data.get('action')
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting = get_object_or_404(Voting, pk=request.data.get('id'))
        msg = ''
        st = status.HTTP_200_OK

        if action == 'start':
            if voting.start_date:
                msg = 'Voting already started'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.create_pubkey()
                voting.start_date = timezone.now()
                voting.save()
                msg = 'Voting started'

        elif action == 'stop':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.end_date:
                msg = 'Voting already stopped'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.end_date = timezone.now()
                voting.save()
                msg = 'Voting stopped'
        
        elif action == 'tally':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = 'Voting is not stopped'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.tally:
                msg = 'Voting already tallied'
                st = status.HTTP_400_BAD_REQUEST
            else:   
                token = request.session.get('auth-token', '')
                if Vote.objects.filter(voting_id=voting.id).exists():
                    voting.tally_votes(token)
                    msg = 'Voting tallied'
                else:
                    voting.postproc = []
                    for option in voting.question.options.all():
                        votes = 0
                        voting.postproc.append({
                            'option': option.option,
                            'number': option.number,
                            'votes': votes,
                            'postproc': 0
                        })
                    voting.tally = []
                    voting.save()
                    msg = 'No votes to tally'
        else:
            msg = 'Action not found, try with start, stop or tally'
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)
    
    def delete(self, request, *args, **kwars):
        voting = get_object_or_404(Voting, pk=request.data.get('id'))
        voting.delete()
        return Response({}, status=status.HTTP_200_OK)