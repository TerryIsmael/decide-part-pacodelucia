import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from voting.models import VotingYesNo


from base import mods


# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
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

class BoothYesNoView(TemplateView):
    template_name = 'booth/boothYesNo.html'


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
                'tally': None,
                'postproc': None
            }

            for k, v in voting_data['pub_key'].items():
                voting_data['pub_key'][k] = str(v)

            context['voting'] = json.dumps(voting_data)


        except VotingYesNo.DoesNotExist:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context

