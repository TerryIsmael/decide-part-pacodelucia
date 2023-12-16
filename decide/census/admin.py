from django.contrib import admin

from .models import Census, CensusPreference, CensusYesNo



class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id')
    list_filter = ('voting_id', )

    search_fields = ('voter_id', )


class CensusPreferenceAdmin(admin.ModelAdmin):
    list_display = ('voting_preference_id', 'voter_id')
    list_filter = ('voting_preference_id', )

    search_fields = ('voter_id', )


class CensusYesNoAdmin(admin.ModelAdmin):
    list_display = ('voting_yesno_id', 'voter_id')
    list_filter = ('voting_yesno_id', )

    search_fields = ('voter_id', )

admin.site.register(Census, CensusAdmin)
admin.site.register(CensusPreference, CensusPreferenceAdmin)
admin.site.register(CensusYesNo, CensusYesNoAdmin)
