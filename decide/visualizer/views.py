import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from base import mods
from voting.models import VotingYesNo,VotingByPreference


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

