from django.contrib import admin

from .models import Vote, VoteByPreference


admin.site.register(Vote)
admin.site.register(VoteByPreference)
