import random
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from .models import Census
from base import mods
from base.tests import BaseTestCase
from .views import filterClass
#from .views import CreateCensus
#from .forms import CreationCensusForm
from django.http import HttpRequest

class CreateCensusTest(TestCase):
    
    def setUp(self):
        self.censo1 = Census.objects.create(
            voting_id= 1,
            voter_id= 1,
            born_year = 2002,
            gender = "MA",
            civil_state = "SI",
            works = "ST",
            country = "Spain",
            religion = "CH"
        )
    def test_censo_create(self):
        self.assertEqual(self.censo1.voting_id,1)
        self.assertEqual(self.censo1.voter_id,1)
        self.assertEqual(self.censo1.born_year,2002)
        self.assertEqual(self.censo1.gender,"MA")
        self.assertEqual(self.censo1.civil_state,"SI")
        self.assertEqual(self.censo1.works,"ST")

#LOS TESTS COMENTADOS AQUÍ DEBAJO SON PARA CUANDO YA SE HAYA HECHO EL HTML

    # def test_get(self):
    #     view = CreateCensus()
    #     request = HttpRequest()
    #     response = view.get(request)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.context['form'], CreationCensusForm)

    # def test_post_success(self):
    #     view = CreateCensus()
    #     request = HttpRequest()
    #     request.POST = {
    #         'voting_id': '1',
    #         'voter_id': '1',
    #         'born_year': '2000',
    #         'gender': 'MA',
    #         'civil_state': 'SI',
    #         'works': 'ST',
    #         'country' = 'Spain',
    #         'religion' = 'CH',
    #     }

    #     response = view.post(request)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.context['census'], Census)
    #     self.assertEqual(Census.objects.count(), 1)

    # def test_post_duplicate(self):
    #     view = CreateCensus()
    #     request = HttpRequest()
    #     request.POST = {
    #         'voting_id': '1',
    #         'voter_id': '1',
    #         'born_year': '2000',
    #         'gender': 'MA',
    #         'civil_state': 'SI',
    #         'works': 'ST',
    #         'country' = 'Spain',
    #         'religion' = 'CH',
    #     }

    #     Census.objects.create(
    #         voting_id='1',
    #         voter_id='1',
    #         born_year='2000',
    #         gender='MA',
    #         civil_state='SI',
    #         works='ST'
    #         country = 'Spain',
    #         religion = 'CH',
    #     )

    #     response = view.post(request)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('error', response.context)

    # def test_invalid_method(self):
    #     view = CreateCensus()
    #     request = HttpRequest()
    #     request.method = 'PUT'
    #     response = view.post(request)
    #     self.assertEqual(response.status_code, 405)


class CensusFilter(TestCase):
    def setUp(self):
        self.censo1 = Census.objects.create(
        voting_id= 1,
        voter_id= 1,
        born_year = 2002,
        gender = "MA",
        civil_state = "SI",
        works = "ST",
        country = "Spain",
        religion = "CH"
        )
        self.censo2= Census.objects.create(
        voting_id= 1,
        voter_id= 1,
        born_year = 2000,
        gender = "FE",
        civil_state = "MA",
        works = "WO",
        country = "China",
        religion = "BU"
        )

    def test_filter_works(self):
        view = filterClass()
        request = HttpRequest()
        request.GET = {'works': 'ST'}
        response = view.filterWorks(request)
        self.assertEqual(list(response.data['census'].values('id')),[{'id':self.censo1.id}])

    def test_filter_gender(self):
        view = filterClass()
        request = HttpRequest()
        request.GET = {'gender': 'FE'}
        response = view.filterGender(request)
        self.assertEqual(list(response.data['census'].values('id')),[{'id':self.censo2.id}])

    def test_filter_civil_state(self):
        view = filterClass()
        request = HttpRequest()
        request.GET = {'civil_state': 'MA'}
        response = view.filterCivilState(request)
        self.assertEqual(list(response.data['census'].values('id')),[{'id':self.censo2.id}])

    def test_filter_born_year(self):
        view = filterClass()
        request = HttpRequest()
        request.GET = {'born_year': '2002'}
        response = view.filterBornYear(request)
        self.assertEqual(list(response.data['census'].values('id')),[{'id':self.censo1.id}])

    def test_filter_country(self):
        view = filterClass()
        request = HttpRequest()
        request.GET = {'country': 'Spain'}
        response = view.filterCountry(request)
        self.assertEqual(list(response.data['census'].values('id')),[{'id':self.censo1.id}])

    def test_filter_religion(self):
        view = filterClass()
        request = HttpRequest()
        request.GET = {'religion': 'BU'}
        response = view.filterReligion(request)
        self.assertEqual(list(response.data['census'].values('id')),[{'id':self.censo2.id}])

class CensusTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.census = Census(voting_id=1, voter_id=1)
        self.census.save()

    def tearDown(self):
        super().tearDown()
        self.census = None

    def test_check_vote_permissions(self):
        response = self.client.get('/census/{}/?voter_id={}'.format(1, 2), format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 'Invalid voter')

        response = self.client.get('/census/{}/?voter_id={}'.format(1, 1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Valid voter')

    def test_list_voting(self):
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'voters': [1]})

    # def test_add_new_voters_conflict(self):
    #     data = {'voting_id': 1, 'voters': [1]}
    #     response = self.client.post('/census/', data, format='json')
    #     self.assertEqual(response.status_code, 401)

    #     self.login(user='noadmin')
    #     response = self.client.post('/census/', data, format='json')
    #     self.assertEqual(response.status_code, 403)

    #     self.login()
    #     response = self.client.post('/census/', data, format='json')
    #     self.assertEqual(response.status_code, 409)

    def test_add_new_voters(self):
        data = {'voting_id': 2, 'voters': [1,2,3,4]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data.get('voters')), Census.objects.count() - 1)

    def test_destroy_voter(self):
        data = {'voters': [1]}
        response = self.client.delete('/census/{}/'.format(1), data, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, Census.objects.count())


class CensusTest(StaticLiveServerTestCase):
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
    
    def createCensusSuccess(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.cleaner.get(self.live_server_url+"/admin/census/census/add")
        now = datetime.now()
        self.cleaner.find_element(By.ID, "id_voting_id").click()
        self.cleaner.find_element(By.ID, "id_voting_id").send_keys(now.strftime("%m%d%M%S"))
        self.cleaner.find_element(By.ID, "id_voter_id").click()
        self.cleaner.find_element(By.ID, "id_voter_id").send_keys(now.strftime("%m%d%M%S"))
        self.cleaner.find_element(By.NAME, "_save").click()

        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/census/census")

    def createCensusEmptyError(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.cleaner.get(self.live_server_url+"/admin/census/census/add")

        self.cleaner.find_element(By.NAME, "_save").click()

        self.assertTrue(self.cleaner.find_element_by_xpath('/html/body/div/div[3]/div/div[1]/div/form/div/p').text == 'Please correct the errors below.')
        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/census/census/add")

    def createCensusValueError(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.cleaner.get(self.live_server_url+"/admin/census/census/add")
        now = datetime.now()
        self.cleaner.find_element(By.ID, "id_voting_id").click()
        self.cleaner.find_element(By.ID, "id_voting_id").send_keys('64654654654654')
        self.cleaner.find_element(By.ID, "id_voter_id").click()
        self.cleaner.find_element(By.ID, "id_voter_id").send_keys('64654654654654')
        self.cleaner.find_element(By.NAME, "_save").click()

        self.assertTrue(self.cleaner.find_element_by_xpath('/html/body/div/div[3]/div/div[1]/div/form/div/p').text == 'Please correct the errors below.')
        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/census/census/add")