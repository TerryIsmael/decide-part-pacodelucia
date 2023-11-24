from django import forms
from .models import Census

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
        ("UN", "Unemployed")
    ] 

    born_date = forms.DateField(required=False)
    gender = forms.ChoiceField(choices=GENDER, required=False)
    civil_state = forms.ChoiceField(choices=CIVIL_STATE, required=False)
    works = forms.ChoiceField(choices=WORKS, required=False)
    
    class Meta:

        model = Census 
        fields = (
            'voting_id', 
            'voter_id',
            'born_date', 
            'gender', 
            'civil_state',
            'works'
        )

    def save (self, commit = True):

        census = super(CreationCensusForm, self).save(commit = False)
        census.voting_id= self.cleaned_data['voting_id']
        census.voter_id= self.cleaned_data['voter_id']
        census.born_date= self.cleaned_data['born_date']
        census.gender= self.cleaned_data['gender']
        census.civil_state= self.cleaned_data['civil_state']
        census.works= self.cleaned_data['works']

        if commit:
            census.save()
        
        return census

 

