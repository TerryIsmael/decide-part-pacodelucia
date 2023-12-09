from django import forms
from .models import Census
from datetime import datetime

class CreationCensusForm(forms.Form):

    voting_id = forms.IntegerField()
    voter_id = forms.IntegerField()

    GENDER = [
        ("MA", "Male"),
        ("FE", "Female"),
        ("NB", "Non binary"),
        ("NP", "No response")
    ]

    CIVIL_STATE = [   
        ("SI","Single"),
        ("MA", "Married"),
        ("DI", "Divorced"),
        ("WI", "Widower")
    ]

    WORKS = [
        ("ST", "Student"),
        ("WO", "Worker"),
        ("UN", "Unemployed"),
        ("RE", "Retiree"),
        ("PE", "Pensioner")
    ] 

    RELIGION = [
        ("CH", "Christianity"),
        ("IS", "Islamism"),
        ("HI", "Hinduism"),
        ("BU", "Buddhism"),
        ("AG", "Agnosticism"),
        ("AT", "Atheism"),
        ("OT", "Other")
    ]


    country = forms.CharField(max_length=50)
    religion = forms.ChoiceField(choices=RELIGION)
    born_year = forms.IntegerField(min_value=datetime.now().year-100, max_value=datetime.now().year)
    gender = forms.ChoiceField(choices=GENDER)
    civil_state = forms.ChoiceField(choices=CIVIL_STATE)
    works = forms.ChoiceField(choices=WORKS)
    
    class Meta:

        model = Census 
        fields = (
            'voting_id', 
            'voter_id',
            'born_year', 
            'gender', 
            'civil_state',
            'works',
            'country',
            'religion'
        )

    def save (self, commit = True):

        census = super(CreationCensusForm, self).save(commit = False)
        census.voting_id= self.cleaned_data['voting_id']
        census.voter_id= self.cleaned_data['voter_id']
        census.born_year= self.cleaned_data['born_year']
        census.gender= self.cleaned_data['gender']
        census.civil_state= self.cleaned_data['civil_state']
        census.works= self.cleaned_data['works']
        census.country = self.cleaned_data['country']
        census.religion = self.cleaned_data['religion']

        if commit:
            census.save()
        
        return census

 

