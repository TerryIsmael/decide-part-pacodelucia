from django.db import models
from django.db.models import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from base import mods
from base.models import Auth, Key
from store.models import VoteByPreference,VoteYesNo
from django.db.models import Max


class Question(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc


#Class QuestionByPreference:
class QuestionByPreference(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc

#Modelo para preguntas de tipo si o no    
class QuestionYesNo(models.Model):
    desc = models.TextField()
    optionYes = models.PositiveIntegerField(editable=False)
    optionNo = models.PositiveIntegerField(editable=False)

    def save(self, *args, **kwargs):
        self.optionYes = 1
        self.optionNo = 2
        super().save(*args, **kwargs)

    def __str__(self):
        return self.desc


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()

    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)

#Class QuestionOptionByPreference:
class QuestionOptionByPreference(models.Model):
    question = models.ForeignKey(QuestionByPreference, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    preference = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()

    def save(self):
        
        self.preference = 0
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)


class Voting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(Question, related_name='voting', on_delete=models.CASCADE)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    

    def save(self, *args, **kwargs):
        def max_id():
            max_voting_bp_id = VotingByPreference.objects.all().aggregate(Max('id'))['id__max']
            max_voting_id = Voting.objects.all().aggregate(Max('id'))['id__max']
            max_votingyesno_id = VotingYesNo.objects.all().aggregate(Max('id'))['id__max']
           
            if max_voting_bp_id is None and max_voting_id is None and max_votingyesno_id is None:
                return 0
            else:
                return max(max_voting_bp_id or 0, max_voting_id or 0, max_votingyesno_id or 0)
        if(self.id is None):
            self.id = (max_id() + 1)
        super().save(*args, **kwargs)

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
        }
        try:
            key = mods.post('mixnet', baseurl=auth.url, json=data)
        except Exception as e:
            raise Exception("No se ha podido conectar con el servidor de mezcla") from e
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        
        # anon votes
        votes_format = []
        vote_list = []
        for vote in votes:
            for info in vote:
                if info == 'a':
                    votes_format.append(vote[info])
                if info == 'b':
                    votes_format.append(vote[info])
            vote_list.append(votes_format)
            votes_format = []
        return vote_list

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)
        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        try:
            response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        except Exception as e:
            raise Exception("No se ha podido conectar con el servidor de mezcla") from e
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        try:
            response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)
        except Exception as e:
            raise Exception("No se ha podido conectar con el servidor de mezcla") from e
        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        options = self.question.options.all()

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes
            })

        data = { 'type': 'IDENTITY', 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name

#Class VotingByPreference:
class VotingByPreference(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(QuestionByPreference, related_name='votingbypreference', on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    pub_key = models.OneToOneField(Key, related_name='votingbypreference', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votingsbypreference')
    
    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        def max_id():
            max_voting_bp_id = VotingByPreference.objects.all().aggregate(Max('id'))['id__max']
            max_voting_id = Voting.objects.all().aggregate(Max('id'))['id__max']
            max_votingyesno_id = VotingYesNo.objects.all().aggregate(Max('id'))['id__max']
           
            if max_voting_bp_id is None and max_voting_id is None and max_votingyesno_id is None:
                return 0
            else:
                return max(max_voting_bp_id or 0, max_voting_id or 0, max_votingyesno_id or 0)
        if(self.id is None):
            self.id = (max_id() + 1)
        super().save(*args, **kwargs)
    
    

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
        }
        try:
            key = mods.post('mixnet', baseurl=auth.url, json=data)
        except Exception as e:
            raise Exception("No se ha podido conectar con el servidor de mezcla") from e
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # getting votes from store
        auxvoting = VoteByPreference.objects.filter(voting_by_preference_id=self.id)
        votes = []
        for vote in auxvoting:
            voting_data = {
                "id": vote.id,
                "voting_by_preference_id": vote.voting_by_preference_id,
                "voter_by_preference_id": vote.voter_by_preference_id,
                "a": vote.a,
                "b": vote.b,
            }
            votes.append(voting_data)
        # anon votes
        votes_format = []
        vote_list = []
        for vote in votes:
            for info in vote:
                if info == 'a':
                    votes_format.append(vote[info])
                if info == 'b':
                    votes_format.append(vote[info])
            vote_list.append(votes_format)
            votes_format = []
        return vote_list

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)
        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        try:
            response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        except Exception as e:
            raise Exception("No se ha podido conectar con el servidor de mezcla") from e
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        try:
            response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)
        except Exception as e:
            raise Exception("No se ha podido conectar con el servidor de mezcla") from e
        if response.status_code != 200:
            # TODO: manage error
            pass
        self.tally = response.json()
        self.save()

        self.do_postproc()
        
    def do_postproc(self):
        tally = self.tally 
        opts = []
        dicpreferences={}
        options = self.question.options.all()
        if isinstance(tally, list):
            
            for t in range(len(tally)):
                tally_str = str(tally[t])
                tally_str_with_commas = tally_str.replace("10000", ",")
                tally_list = [int(num) for num in tally_str_with_commas.split(',') if num]
                for opt in options:
                    if isinstance(tally, list):
                        key=opt.number
                        if key in dicpreferences:
                            dicpreferences[key]+=(len(options) - tally_list[opt.number-2])
                        else:
                            dicpreferences[key]=(len(options) - tally_list[opt.number-2])
                        
        for key in dicpreferences:
            votes = dicpreferences[key]
            option=options.get(number=key)
            opts.append({
                'option': option.option,
                'number': key,
                'votes': votes
            })

        data = { 'type': 'IDENTITY', 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name

#Modelo para votaciones de tipo si o no
class VotingYesNo(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(QuestionYesNo, related_name='votingyesno', on_delete=models.CASCADE)


    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    pub_key = models.OneToOneField(Key, related_name='votingyesno', blank=True, null=True, on_delete=models.SET_NULL)
    auths_yesno = models.ManyToManyField(Auth, related_name='votingsyesno')
    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        def max_id():
            max_voting_bp_id = VotingByPreference.objects.all().aggregate(Max('id'))['id__max']
            max_voting_id = Voting.objects.all().aggregate(Max('id'))['id__max']
            max_votingyesno_id = VotingYesNo.objects.all().aggregate(Max('id'))['id__max']
           
            if max_voting_bp_id is None and max_voting_id is None and max_votingyesno_id is None:
                return 0
            else:
                return max(max_voting_bp_id or 0, max_voting_id or 0, max_votingyesno_id or 0)
        if(self.id is None):
            self.id = (max_id() + 1)
        super().save(*args, **kwargs)

    def create_pubkey(self):
        if self.pub_key or not self.auths_yesno.count():
            return

        auth = self.auths_yesno.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths_yesno.all() ],

        }
        try:
            key = mods.post('mixnet', baseurl=auth.url, json=data)
        except Exception as e:
            raise Exception("No se ha podido conectar con el servidor de mezcla") from e
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # gettings votes from store
        votes = []
        votes_yesno = VoteYesNo.objects.filter(voting_yesno_id=self.id)
        for vote in votes_yesno:
            vote_data = {
                'id': vote.id,
                'voting_yesno_id': vote.voting_yesno_id,
                'voter_yesno_id': vote.voter_yesno_id,
                'a': vote.a,
                'b': vote.b,
            }
            votes.append(vote_data)
        votes_format = []
        vote_list = []
        for vote in votes:
            for info in vote:
                if info == 'a':
                    votes_format.append(vote[info])
                if info == 'b':
                    votes_format.append(vote[info])
            vote_list.append(votes_format)
            votes_format = []
        return vote_list

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)
        auth = self.auths_yesno.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)

        # first, we do the shuffle
        data = { "msgs": votes }
        try:
            response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        except Exception as e:
            raise Exception("No se ha podido conectar con el servidor de mezcla") from e
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        try:
            response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)
        except Exception as e:
            raise Exception("No se ha podido conectar con el servidor de mezcla") from e
        if response.status_code != 200:
            # TODO: manage error
            pass
        self.tally = response.json()
        self.save()

        self.do_postproc()
    
    def do_postproc(self):
        tally = self.tally
        options = []
        options.append(self.question.optionYes)
        options.append(self.question.optionNo)
        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(int(opt))
            else:
                votes = 0
            if int(opt) == 1:
                opts.append({
                    'option': 'Si',
                    'votes': votes
                })
            else:
                opts.append({
                    'option': 'No',
                    'votes': votes
                })

        data = { 'type': 'IDENTITY', 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name
