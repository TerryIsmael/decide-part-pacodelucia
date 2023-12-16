from django import forms
from .models import UserData
from datetime import datetime

class CreationUserDetailsForm(forms.Form):

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

        model = UserData
        fields = (
            'voter_id',
            'born_year', 
            'gender', 
            'civil_state',
            'works',
            'country',
            'religion'
        )

    def save (self, commit = True):

        user_data = super(Creationuser_dataForm, self).save(commit = False)
        user_data.voter_id= self.cleaned_data['voter_id']
        user_data.born_year= self.cleaned_data['born_year']
        user_data.gender= self.cleaned_data['gender']
        user_data.civil_state= self.cleaned_data['civil_state']
        user_data.works= self.cleaned_data['works']
        user_data.country = self.cleaned_data['country']
        user_data.religion = self.cleaned_data['religion']

        if commit:
            user_data.save()
        
        return user_data

 

