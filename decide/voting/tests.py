import json
import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, Client
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base import mods
from base.tests import BaseTestCase
from census.models import Census,CensusPreference, CensusYesNo
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from voting.models import Voting, Question, QuestionOption, Auth, QuestionByPreference, QuestionOptionByPreference,VotingByPreference, QuestionYesNo, VotingYesNo
from datetime import datetime
from rest_framework.authtoken.models import Token



class VotingModelTestCase(BaseTestCase):
    def setUp(self):
        q = Question(desc='Descripcion')
        q.save()
        
        opt1 = QuestionOption(question=q, option='opcion 1')
        opt1.save()
        opt1 = QuestionOption(question=q, option='opcion 2')
        opt1.save()

        self.v = Voting(name='Votacion', question=q)
        self.v.save()

        a = Auth.objects.create(url=settings.BASEURL, me=True, name='test auth')
        a.save()

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.v = None

    def testExist(self):
        v=Voting.objects.get(name='Votacion')
        self.assertEquals(len(v.question.options.all()), 2)

class VotingByPreferenceModelTestCase(BaseTestCase):
    def setUp(self):
        q=QuestionByPreference(desc='Descripcion')
        q.save()

        opt1 = QuestionOptionByPreference(question=q, option='Opción ejemplo 1')
        opt1.save()
        opt1 = QuestionOptionByPreference(question=q, option='Opción ejemplo 2')
        opt1.save()

        self.v = VotingByPreference(name='VotacionPorPreferencia', question=q)
        self.v.save()
        super().setUp()
    
    def tearDown(self):
        super().tearDown()
        self.v = None

    def testExist(self):
        v=VotingByPreference.objects.get(name='VotacionPorPreferencia')
        self.assertEquals(len(v.question.options.all()), 2)

class VotingByPreferenceTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_to_string(self):
        v = self.create_voting_by_preference()
        self.assertEqual(str(v), "test voting by preference")
        self.assertEqual(str(v.question), "test by preference question")
        q=v.question.options.filter(option="option 1").first()
        self.assertEqual(str(q), "option 1 (2)")

    def create_voting_by_preference(self):
        q = QuestionByPreference(desc='test by preference question')
        q.save()
        for i in range(5):
            opt = QuestionOptionByPreference(question=q, option='option {}'.format(i+1))
            opt.save()
        v = VotingByPreference(name='test voting by preference', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
    
    def create_voters_by_preference(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = CensusPreference(voter_id=u.id, voting_preference_id=v.id)
            c.save()
    
    def encrypt_msg_by_preference(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)
    
    def get_or_create_user_by_preference(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user
    
    def store_votes(self, v):
        voters = list(CensusPreference.objects.filter(voting_preference_id=v.id))
        voter = voters.pop()

        clear = {}
        for i in range(random.randint(0, 5)):
                cont=0
                for opt in v.question.options.all():
                    if cont==0:
                        clear[opt.number] = 0
                    opt.number=opt.number+1
                    cont=cont+1
                
                a, b = self.encrypt_msg_by_preference(opt.number, v)
                data = {
                        'votingbypreference': v.id,
                        'voter': voter.voter_id,
                        'vote': { 'a': a, 'b': b },
                }
                    
                user = self.get_or_create_user_by_preference(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear
    
    def test_complete_voting_by_preference(self):
        v = self.create_voting_by_preference()
        self.create_voters_by_preference(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    
    def test_create_voting_by_preference_API(self):
        self.login()
        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'Your preferences ',
            'question_opt': ['cat', 'dog', 'horse']
        }
        response = self.client.post('/custom/votingbypreference', data, format='json')
        self.assertEqual(response.status_code, 201)

        voting = VotingByPreference.objects.get(name='Example')
        self.assertEqual(voting.desc, 'Description example')
        
    def test_create_voting_from_api_by_preference(self):
        data = {'name': 'Example'}
        response = self.client.post('/custom/votingbypreference', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'Your preferences ',
            'question_opt': ['cat', 'dog', 'horse']
        }

        response = self.client.post('/custom/votingbypreference', data, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_update_voting_by_preference(self):
        voting = self.create_voting_by_preference()

        data = {'action': 'start'}

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/custom/votingbypreference/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/custom/votingbypreference/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/custom/votingbypreference/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/custom/votingbypreference/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/custom/votingbypreference/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/custom/votingbypreference/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/custom/votingbypreference/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/custom/votingbypreference/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/custom/votingbypreference/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/custom/votingbypreference/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/custom/votingbypreference/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/custom/votingbypreference/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/custom/votingbypreference/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')    
        
  


class VotingTestCase(BaseTestCase):

    def setUp(self):
        self.q = Question(desc='Descripcion')
        self.q.save()
        
        opt1 = QuestionOption(question=self.q, option='opcion 1')
        opt1.save()
        opt1 = QuestionOption(question=self.q, option='opcion 2')
        opt1.save()

        self.a = Auth.objects.create(url=settings.BASEURL, me=True, name='test auth')
        self.a.save()

        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_to_string(self):
        v = self.create_voting()
        self.assertEqual(str(v), "test voting")
        self.assertEqual(str(v.question), "test question")
        self.assertEqual(str(v.question.options.all()[0]), "option 1 (2)")

    def test_create_voting_API(self):
        self.login()
        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

        voting = Voting.objects.get(name='Example')
        self.assertEqual(voting.desc, 'Description example')
    
    
    def test_check_name_length_limit(self):
        name_over_200_chars = 'a' * 201  
        voting = Voting(name=name_over_200_chars)
        with self.assertRaises(ValidationError):
            voting.full_clean()
       
    def test_check_name_length_limit_on_edit(self):
        # Crear una votación con un nombre válido
        voting = self.create_voting()
        voting.name = 'a' * 200 # Cambiar el nombre a uno válido
        voting.save()
        voting.name = 'a' * 201
        with self.assertRaises(ValidationError):
            voting.full_clean()
    
    def test_voting_without_question(self):
        # Intentar crear una votación sin una pregunta asociada
        with self.assertRaises(IntegrityError):
            voting = Voting(name='Test voting')
            voting.save()  # Esto debería lanzar un IntegrityError porque no se ha establecido question_id


    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
  
    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_voting(self):
        voting = self.create_voting()

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')

    def test_update_voting_405(self):
        v = self.create_voting()
        data = {} #El campo action es requerido en la request
        self.login()
        response = self.client.post('/voting/{}/'.format(v.pk), data, format= 'json')
        self.assertEquals(response.status_code, 405) 
    
    def test_get_voting_string_keys(self):
        v = self.create_voting()
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()
        response = self.client.get('/voting/{}/stringkeys'.format(v.pk))
        voting = json.loads(response.json()['voting'])
        keybits = response.json()['KEYBITS']
        self.assertEquals(response.status_code, 200)
        self.assertEquals(voting['name'], 'test voting')
        self.assertEquals(keybits, settings.KEYBITS)
        for _, val in voting['pub_key'].items():
            self.assertIsInstance(val, str)
        self.assertEquals(voting['pub_key']['p'], str(v.pub_key.p))
        self.assertEquals(voting['pub_key']['g'], str(v.pub_key.g))
        self.assertEquals(voting['pub_key']['y'], str(v.pub_key.y))
    
    def test_get_voting_string_keys_404(self):
        response = self.client.get('/voting/12345/stringkeys')
        self.assertEquals(response.status_code, 404)
    
class GetVotingsByUserTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=user)

        q = Question(desc='Descripcion')
        q.save()
        
        opt1 = QuestionOption(question=q, option='opcion 1')
        opt1.save()
        opt1 = QuestionOption(question=q, option='opcion 2')
        opt1.save()

        self.voting1 = Voting.objects.create(name='test voting 1', question=q)
        self.voting2 = Voting.objects.create(name='test voting 2', question=q)

        Census.objects.create(voter_id=user.pk, voting_id=self.voting1.pk)
        Census.objects.create(voter_id=user.pk, voting_id=self.voting2.pk)
    
    def tearDown(self):
        self.client = None
        super().tearDown()

    def test_get_votings_by_user(self):
        self.client.cookies['decide'] = self.token.key
        response = self.client.get('/voting/getbyuser')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['votings'][0]['name'], 'test voting 1')
        self.assertEqual(response.json()['votings'][1]['name'], 'test voting 2')
    
    def test_get_votings_by_user_401(self):
        response = self.client.get('/voting/getbyuser')
        self.assertEqual(response.status_code, 401)

class VotingFrontTestCase(BaseTestCase):

    def setUp(self):
        self.q = Question(desc='Descripcion')
        self.q.save()
        opt1 = QuestionOption(question=self.q, option='opcion 1')
        opt1.save()
        opt1 = QuestionOption(question=self.q, option='opcion 2')
        opt1.save()

        self.a = Auth.objects.create(url=settings.BASEURL, me=True, name='test auth')
        self.a.save()

        super().setUp()

    def tearDown(self):
        super().tearDown()

    def login(self, user='admin', password='qwerty'):
        data = {'username': user, 'password': password}
        response = mods.post('authentication/login', json=data, response=True)
        response2 = mods.post('authentication/login-auth', json=data, response=True)
        self.assertEqual(response.status_code, 200)
        self.token = response.json().get('token')
        self.assertTrue(self.token)
        csrf_token = response2.cookies.get('csrftoken')
        auth_token = response2.cookies.get('auth_token')
        self.client.cookies['csrftoken'] = csrf_token
        self.client.cookies['auth-token'] = auth_token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        
    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
  
    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear
    
    def test_update_voting_front(self):

        voting = self.create_voting()

        # login with user admin
        self.login()
        data = {'id': voting.pk,'action': 'bad'}
        response = self.client.put('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'id': voting.pk,'action': action}
            response = self.client.put('/voting/voting/', data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'id': voting.pk,'action': 'start'}
        response = self.client.put('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'id': voting.pk,'action': 'start'}
        response = self.client.put('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'id': voting.pk,'action': 'tally'}
        response = self.client.put('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'id': voting.pk,'action': 'stop'}
        response = self.client.put('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'id': voting.pk,'action': 'start'}
        response = self.client.put('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'id': voting.pk,'action': 'stop'}
        response = self.client.put('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'id': voting.pk,'action': 'tally'}
        response = self.client.put('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'No votes to tally')

        # STATUS VOTING: tallied
        data = {'id': voting.pk,'action': 'start'}
        response = self.client.put('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'id': voting.pk,'action': 'stop'}
        response = self.client.put('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'id': voting.pk,'action': 'tally'}
        response = self.client.put('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')
        
    def test_update_voting_front_with_votes(self):
        voting = self.create_voting()
        self.create_voters(voting)

        voting.create_pubkey()
        voting.start_date = timezone.now()
        voting.save()

        self.store_votes(voting)

        self.login()

        data = {'id': voting.pk,'action': 'stop'}
        response = self.client.put('/voting/voting/', data, format='json')

        data = {'id': voting.pk,'action': 'tally'}
        response = self.client.put('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

    def test_create_voting_front(self):
        
        data = {
            'name': 'example name',
            'desc': 'example description',
            'question': self.q.id,
            'auths': [self.a.id],
        }
        
        self.login()
        response = self.client.post('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_voting_front_400(self):
        data = {'name': 'Example'}
        
        data_good = {
            'name': 'example name',
            'desc': 'example description',
            'question': self.q.id,
            'auths': [self.a.id],
        }
        
        response = self.client.post('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.post('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 403)

        response = self.client.post('/voting/voting/', data_good, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = self.client.post('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_voting_front(self):
        
        voting = self.create_voting()
        data = {'id': voting.pk}
        self.login()
        response = self.client.delete('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_voting_front_400(self):
        
        voting = self.create_voting()
        data = {'id': voting.pk}

        response = self.client.delete('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)
        
        self.login(user='noadmin')
        response = self.client.delete('/voting/voting/', data, format='json')
        self.assertEqual(response.status_code, 403)

        #Post without data
        self.login()
        response = self.client.delete('/voting/voting/')
        self.assertEqual(response.status_code, 404)

class QuestionFrontTestCase(BaseTestCase):
    
    def setUp(self):
        self.q = Question(desc='Descripcion')
        self.q.save()
        
        opt1 = QuestionOption(question=self.q, option='opcion 1')
        opt1.save()
        opt1 = QuestionOption(question=self.q, option='opcion 2')
        opt1.save()

        self.a = Auth.objects.create(url=settings.BASEURL, me=True, name='test auth')
        self.a.save()

        super().setUp()

    def tearDown(self):
        super().tearDown()

    def login(self, user='admin', password='qwerty'):
        data = {'username': user, 'password': password}
        response = mods.post('authentication/login', json=data, response=True)
        response2 = mods.post('authentication/login-auth', json=data, response=True)
        self.assertEqual(response.status_code, 200)
        self.token = response.json().get('token')
        self.assertTrue(self.token)
        csrf_token = response2.cookies.get('csrftoken')
        auth_token = response2.cookies.get('auth_token')
        self.client.cookies['csrftoken'] = csrf_token
        self.client.cookies['auth-token'] = auth_token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_all_questions(self):
        self.login()
        response = self.client.get('/voting/all-questions/')
        self.assertEqual(response.status_code, 200)

    def test_get_all_questions_400(self):
        response = self.client.get('/voting/all-questions/')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.get('/voting/all-questions/')
        self.assertEqual(response.status_code, 403)
        
    def test_create_question_front(self):  
        self.login()
        data = {
            "desc": "example description",
            "options": [
                {
                    "number": 1,
                    "option": "Option 1"
                },
                {
                    "number": 2,
                    "option": "Option 2"
                }
            ]
        }
        
        response = self.client.post('/voting/all-questions/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_question_front_400(self):
        data = {"desc": "example description"}
        
        response = self.client.post('/voting/all-questions/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.post('/voting/all-questions/', data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = self.client.post('/voting/all-questions/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_update_question_front(self):
        self.login()
        
        data = {
            "id": self.q.id,
            "desc": "example description edited",
            "options": [
                {
                    "number": 1,
                    "option": "Option 1 edited"
                },
                {
                    "number": 2,
                    "option": "Option 2 edited"
                }
            ]
        }
        
        response = self.client.post('/voting/all-questions/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_question_front_400(self):
        data = {"desc": "example description"}
        
        response = self.client.post('/voting/all-questions/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.post('/voting/all-questions/', data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = self.client.post('/voting/all-questions/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_question_front(self):
        self.login()
        data = {"id": self.q.id}
        response = self.client.delete('/voting/all-questions/', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_question_front_400(self):
        data = {"id": self.q.id}
        response = self.client.delete('/voting/all-questions/', data, format='json')
        self.assertEqual(response.status_code, 401)
        
        self.login(user='noadmin')
        response = self.client.delete('/voting/all-questions/', data, format='json')
        self.assertEqual(response.status_code, 403)

        #Post without data
        self.login()
        response = self.client.delete('/voting/all-questions/')
        self.assertEqual(response.status_code, 404)

class LogInSuccessTests(StaticLiveServerTestCase):

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def successLogIn(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")
        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/")


class LogInErrorTests(StaticLiveServerTestCase):

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def usernameWrongLogIn(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)
        
        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("usuarioNoExistente")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("usuarioNoExistente")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.assertTrue(self.cleaner.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/p').text == 'Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.')

    def passwordWrongLogIn(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("wrongPassword")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.assertTrue(self.cleaner.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/p').text == 'Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.')

class QuestionsTests(StaticLiveServerTestCase):

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def createQuestionSuccess(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.cleaner.get(self.live_server_url+"/admin/voting/question/add/")
        
        self.cleaner.find_element(By.ID, "id_desc").click()
        self.cleaner.find_element(By.ID, "id_desc").send_keys('Test')
        self.cleaner.find_element(By.ID, "id_options-0-number").click()
        self.cleaner.find_element(By.ID, "id_options-0-number").send_keys('1')
        self.cleaner.find_element(By.ID, "id_options-0-option").click()
        self.cleaner.find_element(By.ID, "id_options-0-option").send_keys('test1')
        self.cleaner.find_element(By.ID, "id_options-1-number").click()
        self.cleaner.find_element(By.ID, "id_options-1-number").send_keys('2')
        self.cleaner.find_element(By.ID, "id_options-1-option").click()
        self.cleaner.find_element(By.ID, "id_options-1-option").send_keys('test2')
        self.cleaner.find_element(By.NAME, "_save").click()

        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/voting/question/")

    def createCensusEmptyError(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.cleaner.get(self.live_server_url+"/admin/voting/question/add/")

        self.cleaner.find_element(By.NAME, "_save").click()

        self.assertTrue(self.cleaner.find_element_by_xpath('/html/body/div/div[3]/div/div[1]/div/form/div/p').text == 'Please correct the errors below.')
        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/voting/question/add/")

class VotingYesNoModelTestCase(BaseTestCase):
    def setUp(self):
        q = QuestionYesNo(desc='Descripcion')
        q.save()

        self.v = VotingYesNo(name='Votacion Yes/No', question=q)
        self.v.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.v = None

    def testExist(self):
        v=VotingYesNo.objects.get(name='Votacion Yes/No')
        self.assertEquals(v.question.optionYes, 1)
        self.assertEquals(v.question.optionNo, 2)

class VotingYesNoTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_to_string(self):
        v = self.create_voting()
        self.assertEqual(str(v), "test votingYesNo")
        self.assertEqual(str(v.question), "test question yesno")
        self.assertEqual(str(v.question.optionYes), '1')
        self.assertEqual(str(v.question.optionNo), '2')
    
    def create_voting(self):
        q = QuestionYesNo(desc='test question yesno')
        q.save()
        v = VotingYesNo(name='test votingYesNo', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths_yesno.add(a)

        return v
    
    def test_create_voting_yesno_API(self):
        self.login()
        data = {
            'name': 'Example Yes/No',
            'desc': 'Description example Yes/No',
            'question': 'Do you like cats?',
            'question_opt': ['Yes', 'No']
        }
        response = self.client.post('/custom/votingyesno/', data, format='json')
        self.assertEqual(response.status_code, 201)

        voting = VotingYesNo.objects.get(name='Example Yes/No')
        self.assertEqual(voting.desc, 'Description example Yes/No')
    
    
    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)



    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = CensusYesNo(voter_id=u.id, voting_yesno_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(CensusYesNo.objects.filter(voting_yesno_id=v.id))
        voter = voters.pop()

        clear = {}
        clear[v.question.optionYes] = 0
        for i in range(random.randint(0, 5)):
            a, b = self.encrypt_msg(v.question.optionYes, v)
            data = {
                'voting': v.id,
                'voter': voter.voter_id,
                'vote': { 'a': a, 'b': b },
            }
            clear[v.question.optionYes] += 1
            user = self.get_or_create_user(voter.voter_id)
            self.login(user=user.username)
            voter = voters.pop()
            mods.post('custom/store/yesno', json=data)
        clear[v.question.optionNo] = 0
        for i in range(random.randint(0, 5)):
            a, b = self.encrypt_msg(v.question.optionNo, v)
            data = {
                'voting': v.id,
                'voter': voter.voter_id,
                'vote': { 'a': a, 'b': b },
            }
            clear[v.question.optionNo] += 1
            user = self.get_or_create_user(voter.voter_id)
            self.login(user=user.username)
            voter = voters.pop()
            mods.post('custom/store/yesno', json=data)
        
        return clear

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}


        self.assertEqual(tally.get(v.question.optionYes, 0), clear.get(v.question.optionYes, 0))
        self.assertEqual(tally.get(v.question.optionNo, 0), clear.get(v.question.optionNo, 0))

        for q in v.postproc:
            if q["option"] == 'Si':
                self.assertEqual(tally.get(v.question.optionYes, 0), q["votes"])
            else:
                self.assertEqual(tally.get(v.question.optionNo, 0), q["votes"])

    def test_create_voting_yesno_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/custom/votingyesno/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example Yes/No',
            'desc': 'Description example Yes/No',
            'question': 'Do you like cats?',
            'question_opt': ['Yes', 'No']
        }
        response = self.client.post('/custom/votingyesno/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_voting_yesno(self):
        voting = self.create_voting()

        data = {'action': 'start'}

        self.login(user='noadmin')
        response = self.client.put('/custom/votingyesno/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/custom/votingyesno/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/custom/votingyesno/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/custom/votingyesno/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/custom/votingyesno/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/custom/votingyesno/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/custom/votingyesno/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/custom/votingyesno/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/custom/votingyesno/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/custom/votingyesno/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/custom/votingyesno/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/custom/votingyesno/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/custom/votingyesno/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')
