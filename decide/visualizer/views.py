from datetime import timedelta
import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.db.models.functions import ExtractHour
from base import mods
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from voting.models import Voting
from census.models import Census
from store.models import Vote
from .models import Stats
from django.db.models import Sum, Count,Avg

# views.py

from django.http import JsonResponse

def stats(request,voting_id):
    stats = Stats.objects.first()

     # Obtener la votación específica
    voting = get_object_or_404(Voting, id=voting_id)
    question= voting.question.desc

     # Obtener el número de votos para la votación
    votes_count = Vote.objects.filter(voting_id=voting_id).count()

    # Obtener el censo para la votación
    census_count = Census.objects.filter(voting_id=voting_id).count()

    # Calcular el porcentaje de votantes
    percentage_voters = (votes_count / census_count) * 100 if census_count > 0 else 0
    percentage_voters=round(percentage_voters,2)


    data = {
        'voting': voting.id,
        'votes': votes_count,
        'census':percentage_voters,
        'question':question,
    }

    return JsonResponse(data)



class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        return context
