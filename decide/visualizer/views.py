import json
from django.views.generic import TemplateView
from django.http import Http404
from base import mods
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from voting.models import Voting, VotingYesNo,VotingByPreference
from census.models import Census, CensusYesNo
from store.models import Vote, VoteYesNo, VoteByPreference

# views.py

def stats(request,voting_id):

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

def statsYesNo(request,voting_id):

     # Obtener la votación específica
    voting = get_object_or_404(VotingYesNo, id=voting_id)
    question= voting.question.desc

     # Obtener el número de votos para la votación
    votes_count = VoteYesNo.objects.filter(voting_id=voting_id).count()

    # Obtener el censo para la votación
    census_count = CensusYesNo.objects.filter(voting_id=voting_id).count()

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


class VisualizerBPView(TemplateView):
    template_name = 'visualizer/visualizerBP.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
          
            voting = VotingByPreference.objects.get(id=vid)
        
            # Convert the data into the desired JSON format
            voting_data = {
                'id': voting.id,
                'name': voting.name,
                'desc': voting.desc,
                'question': {
                    'desc': voting.question.desc,
                    'options': [{'number': o.number, 'option': o.option, 'preference': o.preference} for o in voting.question.options.all()]
                },
                'start_date': voting.start_date.isoformat(),
                'end_date': voting.end_date.isoformat() if voting.end_date else None,
                'pub_key': {
                    'p': voting.pub_key.p,
                    'g': voting.pub_key.g,
                    'y': voting.pub_key.y,
                },
                'auths': [{'name': a.name, 'url': a.url, 'me': a.me} for a in voting.auths.all()],
                'tally': voting.tally,
                'postproc': voting.postproc,
            }
            context['voting'] = json.dumps(voting_data)
        except:
            raise Http404

        return context
    

class VisualizerYesNoView(TemplateView):
    template_name = 'visualizer/visualizerYesNo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
          
            voting_yesno = VotingYesNo.objects.get(id=vid)
            voting_data = {
                'id': voting_yesno.id,
                'name': voting_yesno.name,
                'desc': voting_yesno.desc,
                'question': {
                    'desc': voting_yesno.question.desc,
                    'optionYes': voting_yesno.question.optionYes,
                    'optionNo': voting_yesno.question.optionNo,
                },
                'start_date': voting_yesno.start_date.isoformat(),
                'end_date': voting_yesno.end_date.isoformat() if voting_yesno.end_date else None,
                'pub_key': {
                    'p': voting_yesno.pub_key.p,
                    'g': voting_yesno.pub_key.g,
                    'y': voting_yesno.pub_key.y,
                },
                'auths': [{'name': a.name, 'url': a.url, 'me': a.me} for a in voting_yesno.auths_yesno.all()],
                'tally': voting_yesno.tally,
                'postproc': voting_yesno.postproc,
            }
            context['voting'] = json.dumps(voting_data)
            print(context['voting'])
        except:
            raise Http404

        return context

