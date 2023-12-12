from django.contrib import admin
from .models import Vote, VoteByPreference,VoteYesNo


admin.site.register(Vote)
admin.site.register(VoteByPreference)
admin.site.register(VoteYesNo)

