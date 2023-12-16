from django.contrib import admin
from django.contrib import messages
from .models import Census, CensusPreference, CensusYesNo, UserData
from .forms import ReuseCensusForm

class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id')
    list_filter = ('voting_id', 'voter_id')

    search_fields = ('voter_id', )

    def reuse_census(modeladmin, request, queryset):
        selected_voting_id = request.POST.get("selected_voting_id")
        if selected_voting_id and selected_voting_id.strip():
            modeladmin.message_user(request, f"ID provided: {selected_voting_id}")

            for census in queryset.all():
                existing_census = Census.objects.filter(
                    voting_id=selected_voting_id, voter_id=census.voter_id
                )
                if existing_census.exists():
                    messages.error(
                        request,
                        f"Census with voter_id {census.voter_id} and voting_id {selected_voting_id} already exists in the database.",
                    )
                    continue
                new_census = Census(voter_id=census.voter_id, voting_id=selected_voting_id)
                new_census.save()
        else:
            messages.error(
                request,
                "Error: Invalid form. Make sure to enter a valid ID.",
            )

    reuse_census.short_description = "Reuse Census"

    actions = [reuse_census]
    action_form = ReuseCensusForm  


class CensusPreferenceAdmin(admin.ModelAdmin):
    list_display = ('voting_preference_id', 'voter_id')
    list_filter = ('voting_preference_id', )

    search_fields = ('voter_id', )


class CensusYesNoAdmin(admin.ModelAdmin):
    list_display = ('voting_yesno_id', 'voter_id')
    list_filter = ('voting_yesno_id', )

    search_fields = ('voter_id', )


class UserDataAdmin(admin.ModelAdmin):
    list_display = ('voter_id', 'gender', 'works', 'civil_state', 'born_year', 'country', 'religion')
    list_filter = ('voter_id', 'gender', 'works', 'civil_state', 'born_year', 'country', 'religion')


    search_fields = ('voter_id', )

admin.site.register(Census, CensusAdmin)
admin.site.register(CensusPreference, CensusPreferenceAdmin)
admin.site.register(CensusYesNo, CensusYesNoAdmin)
admin.site.register(UserData, UserDataAdmin)