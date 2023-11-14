import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from voting.models import VotingByPreference

from base import mods


# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
        print("Entré a get_context_data")
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)
        
            context['voting'] = json.dumps(r[0])
           
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context

class BoothByPreferenceView(TemplateView):
    template_name = 'booth/boothBP.html'

    

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
                'tally': None,
                'postproc': None
            }
            for k, v in voting_data['pub_key'].items():
                voting_data['pub_key'][k] = str(v)
        
            context['voting'] = json.dumps(voting_data)
        except VotingByPreference.DoesNotExist:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context
