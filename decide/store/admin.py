from django.contrib import admin

from .models import VoteYesNo, Vote


admin.site.register(Vote)
admin.site.register(VoteYesNo)
