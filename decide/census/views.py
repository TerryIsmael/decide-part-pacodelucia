from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

from base.perms import UserIsStaff
from .models import Census


class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})

    def list_votings(self, request, *args, **kwargs):
        voter_id = request.GET.get('voter_id')
        votings = Census.objects.filter(voter_id=voter.id).values_list('voting_id', flat=True)
        return Response ({'votings': votings})

class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')

def createCensus(request):
    if request.method == 'GET':
        return render (request, 'census_create.html',{'form': CreationCensusForm})
    else:
        if request.method == 'POST':
            try:
                census = Census.objects.create(

                    voting_id = request.POST['voting_id'],
                    voter_id = request.POST['voter_id'],
                    born_date = request.POST['born_date'],
                    gender = request.POST['gender'],
                    civil_state = request.POST['civil_state'],
                    works = request.POST['works']

                )
                census.save()
                return render(request, 'census_suceed.html', {'census':census})

            except:
                return render(request,'census_create.html',{'form': CreationCensusForm, "error": 'Census already exist'})
        return render(request,'census_create.html',{'form':CreationCensusForm})

def  voitingIdSet():
    conjunto_voting=set()
    for census in census.objects.all():
        conjunto_voting.add(census.voting_id)
    return conjunto_voting


def filter(request):
    censo =census.objects.all()
    votingsIds = votingIdSet()
    return  render(request, 'filterCensus.html', {'census': censo, 'votingsIds':votingsIds})

class filterGender(self, request, *args, **kwargsView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    gender = request.GET.get('gender')
    census = Census.objects.filter(=gender)
    return Response ({'census': census})


class filterWork(self, request,*args, **kwargsView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    works = request.GET.get('works')
    census = Census.objects.filter(=works)
    return Response ({'census': census})

class filterCivilState(self, request,*args, **kwargsView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    civil_state = request.GET.get('civil_state')
    census = Census.objects.filter(=civil_state)
    return Response ({'census': census})



    
