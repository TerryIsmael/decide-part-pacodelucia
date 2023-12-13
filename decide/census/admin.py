from django.contrib import admin

from .models import Census


class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id',"census_group")
    list_filter = ('voting_id', "census_group")
    list_filter = ('voter_id', )

    search_fields = ('voter_id', )


admin.site.register(Census, CensusAdmin)
