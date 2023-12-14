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
from django.shortcuts import render
from .models import Census
from django.views import View
from .forms import CreationCensusForm

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
        votings = Census.objects.filter(voter_id=voter_id).values_list('voting_id', flat=True)
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

class CreateCensus(View):
    def get(self, request):
        form = CreationCensusForm()
        return render(request, 'census_create.html', {'form': form})

    def post(self, request):
        form = CreationCensusForm(request.POST)
        if form.is_valid():
            try:
                census = Census.objects.create(
                    voting_id=form.cleaned_data['voting_id'],
                    voter_id=form.cleaned_data['voter_id'],
                    born_year=form.cleaned_data['born_year'],
                    gender=form.cleaned_data['gender'],
                    civil_state=form.cleaned_data['civil_state'],
                    works=form.cleaned_data['works'],
                    country = form.cleaned_data['country'],
                    religion = form.cleaned_data['religion']
                )
                census.save()
                return render(request, 'census_suceed.html', {'census': census})
            except IntegrityError:
                return render(request, 'census_create.html', {'form': form, "error": 'Census already exist'})
        return render(request, 'census_create.html', {'form': form})


class filterClass():

    def filterGender(self, request, *args, **kwargsView):

        gender = request.GET.get('gender')
        census = Census.objects.filter(gender=gender)
        return Response ({'census': census})

    def filterWorks(self, request,*args, **kwargsView):

        works = request.GET.get('works')
        census = Census.objects.filter(works =works)
        return Response ({'census': census})

    def filterCivilState(self, request,*args, **kwargsView):

        civil_state = request.GET.get('civil_state')
        census = Census.objects.filter(civil_state=civil_state)
        return Response ({'census': census})

    def filterBornYear(sef,request,*args,**kwargsView):

        born_year = request.GET.get('born_year')
        census = Census.objects.filter(born_year=born_year)
        return Response ({'census': census})

    def filterCountry(sef,request,*args,**kwargsView):

        country = request.GET.get('country')
        census = Census.objects.filter(country=country)
        return Response ({'census': census})

    def filterReligion(sef,request,*args,**kwargsView):

        religion = request.GET.get('religion')
        census = Census.objects.filter(religion=religion)
        return Response ({'census': census})

            
