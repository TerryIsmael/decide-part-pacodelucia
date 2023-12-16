from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

from base.perms import UserIsStaff
from .models import Census, UserData
from .forms import CreationUserDetailsForm
from .serializers import UserDataSerializer
from authentication.serializers import UserSerializer

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

class UserDataCreate(generics.CreateAPIView):
    serializer_class = UserDataSerializer

    def post(self, request, *args, **kwargs):
        form = CreationUserDetailsForm(request.POST)
        if not form["country"].data:
            form = CreationUserDetailsForm(request.data)

        if form.is_valid():
            user_data = UserData.objects.filter(voter_id = form["voter_id"].data)
            if not user_data.exists():
                user_data = UserData.objects.create(
                    voter_id=form.cleaned_data['voter_id'],
                    born_year=form.cleaned_data['born_year'],
                    gender=form.cleaned_data['gender'],
                    civil_state=form.cleaned_data['civil_state'],
                    works=form.cleaned_data['works'],
                    country = form.cleaned_data['country'],
                    religion = form.cleaned_data['religion']
                )
                user_data.save()
                return Response({}, status=status.HTTP_201_CREATED)
            else:
                user_data = user_data[0]
                user_data.born_year=form.cleaned_data['born_year']
                user_data.gender=form.cleaned_data['gender']
                user_data.civil_state=form.cleaned_data['civil_state']
                user_data.works=form.cleaned_data['works']
                user_data.country = form.cleaned_data['country']
                user_data.religion = form.cleaned_data['religion']
               
                user_data.save()
                return Response({}, status=status.HTTP_201_CREATED)
        return Response({"errors": str(form.errors.as_data)}, status=status.HTTP_400_BAD_REQUEST)


class CensusFilter(generics.ListAPIView):
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        filter_type = request.GET["filter"]
        filter_value = request.GET["filter_value"]
        filter_class = FilterClass()
        return filter_class.get_users_filtered(filter_type, filter_value)


class FilterClass():

    def get_users_filtered(self, filter, filter_value):
        user_ids = None
        if filter == 'gender':
            user_ids = self.filterGender(filter_value)
        elif filter == 'works':
            user_ids = self.filterWorks(filter_value)
        elif filter == 'civil_state':
            user_ids = self.filterCivilState(filter_value)
        elif filter == 'born_year':
            user_ids = self.filterBornYear(filter_value)
        elif filter == 'country':
            user_ids = self.filterCountry(filter_value)
        elif filter == 'religion':
            user_ids = self.filterReligion(filter_value)

        if not user_ids:
            user_ids = []
       
        users = []
        for voter_id in user_ids:
            user = User.objects.filter(id = voter_id)
            if user.exists():
                users.append(user[0])

        users = UserSerializer(users, many = True)
        return Response ({'users': users.data})


    def filterGender(self, filter_value):
        user_ids = UserData.objects.filter(gender = filter_value).values_list('voter_id', flat=True)
        return user_ids


    def filterWorks(self, filter_value):
        user_ids = UserData.objects.filter(works = filter_value).values_list('voter_id', flat=True)
        return user_ids

    def filterCivilState(self, filter_value):
        user_ids = UserData.objects.filter(civil_state = filter_value).values_list('voter_id', flat=True)
        return user_ids

    def filterBornYear(self, filter_value):
        user_ids = UserData.objects.filter(born_year = filter_value).values_list('voter_id', flat=True)
        return user_ids

    def filterCountry(self, filter_value):
        user_ids = UserData.objects.filter(country = filter_value).values_list('voter_id', flat=True)
        return user_ids

    def filterReligion(self, filter_value):
        user_ids = UserData.objects.filter(religion = filter_value).values_list('voter_id', flat=True)
        return user_ids
