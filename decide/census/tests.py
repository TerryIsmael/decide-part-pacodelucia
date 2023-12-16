import random
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from .models import Census, UserData
from base import mods
from base.tests import BaseTestCase

class CreateCensusTest(BaseTestCase):
    
    def setUp(self):
        self.user1 = User(username='user1', is_staff=True)
        self.user1.set_password('qwerty')
        self.user1.save()

        self.user2 = User(username='user2', is_staff=True)
        self.user2.set_password('qwerty')
        self.user2.save()

        self.user_data = UserData.objects.create(
            voter_id= 1,
            born_year = 2002,
            gender = "MA",
            civil_state = "SI",
            works = "ST",
            country = "Spain",
            religion = "CH"
        )
        self.user_data.save()
        super().setUp()

    def tearDown(self):
        self.user_data = None
        super().tearDown()

    def test_censo_create(self):
        created_user_data = UserData.objects.filter(id = self.user_data.id)

        self.assertNotEqual(created_user_data, None)
        self.assertEqual(self.user_data.voter_id,1)
        self.assertEqual(self.user_data.born_year,2002)
        self.assertEqual(self.user_data.gender,"MA")
        self.assertEqual(self.user_data.civil_state,"SI")
        self.assertEqual(self.user_data.works,"ST")

    def test_post_fail_year(self):
        data = {'voter_id': 2, 'born_year': 1000, 'gender': 'MA', 'civil_state': 'SI', 'works': 'ST', 'country': 'Spain', 'religion': 'CH'}
        response = self.client.post('/census/user-details/', data, format='json', follow = True)
        self.assertEqual(response.status_code, 400)

    def test_post_success(self):
        data = {'voter_id': 2, 'born_year': 2000, 'gender': 'MA', 'civil_state': 'SI', 'works': 'ST', 'country': 'Spain', 'religion': 'CH'}
        response = self.client.post('/census/user-details/', data, format='json', follow = True)
        self.assertEqual(response.status_code, 201)

    def test_update_success(self):
        data = {'voter_id': 2, 'born_year': 2000, 'gender': 'MA', 'civil_state': 'SI', 'works': 'ST', 'country': 'Spain', 'religion': 'CH'}
        response = self.client.post('/census/user-details/', data, format='json', follow = True)
        data = {'voter_id': 2, 'born_year': 2002, 'gender': 'MA', 'civil_state': 'SI', 'works': 'ST', 'country': 'Spain', 'religion': 'CH'}
        response = self.client.post('/census/user-details/', data, format='json', follow = True)
        self.assertEqual(response.status_code, 201)

class CensusFilter(BaseTestCase):
    def setUp(self):
        self.user1 = User(username='user1', is_staff=True)
        self.user1.set_password('qwerty')
        self.user1.save()

        self.user2 = User(username='user2', is_staff=True)
        self.user2.set_password('qwerty')
        self.user2.save()

        self.user_data1 = UserData.objects.create(
        voter_id= self.user1.id,
        born_year = 2002,
        gender = "MA",
        civil_state = "SI",
        works = "ST",
        country = "Spain",
        religion = "CH"
        )
        self.user_data1.save()

        self.user_data2 = UserData.objects.create(
        voter_id= self.user2.id,
        born_year = 2000,
        gender = "FE",
        civil_state = "MA",
        works = "WO",
        country = "China",
        religion = "BU"
        )
        self.user_data2.save()
        super().setUp()

    def tearDown(self):
        self.user_data1 = None
        self.user_data2 = None
        super().tearDown()

    def test_filter_works(self):
        response = self.client.get('/census/get-filtered-census?filter=works&filter_value=ST', format='json', follow = True)
        self.assertEqual(response.status_code, 200)
        users = response.json()

        self.assertEqual(len(users['users']), 1)
        self.assertEqual(users['users'][0]['id'], self.user1.id)

    def test_filter_gender(self):
        response = self.client.get('/census/get-filtered-census?filter=gender&filter_value=FE', format='json', follow = True)
        self.assertEqual(response.status_code, 200)
        users = response.json()

        self.assertEqual(len(users['users']), 1)
        self.assertEqual(users['users'][0]['id'], self.user2.id)

    def test_filter_civil_state(self):
        response = self.client.get('/census/get-filtered-census?filter=civil_state&filter_value=SI', format='json', follow = True)
        self.assertEqual(response.status_code, 200)
        users = response.json()

        self.assertEqual(len(users['users']), 1)
        self.assertEqual(users['users'][0]['id'], self.user1.id)

    def test_filter_born_year(self):
        response = self.client.get('/census/get-filtered-census?filter=born_year&filter_value=2002', format='json', follow = True)
        self.assertEqual(response.status_code, 200)
        users = response.json()

        self.assertEqual(len(users['users']), 1)
        self.assertEqual(users['users'][0]['id'], self.user1.id)

    def test_filter_country(self):
        response = self.client.get('/census/get-filtered-census?filter=country&filter_value=China', format='json', follow = True)
        self.assertEqual(response.status_code, 200)
        users = response.json()

        self.assertEqual(len(users['users']), 1)
        self.assertEqual(users['users'][0]['id'], self.user2.id)

    def test_religion(self):
        response = self.client.get('/census/get-filtered-census?filter=religion&filter_value=BU', format='json', follow = True)
        self.assertEqual(response.status_code, 200)
        users = response.json()

        self.assertEqual(len(users['users']), 1)
        self.assertEqual(users['users'][0]['id'], self.user2.id)

    def test_no_one_was_found(self):
        response = self.client.get('/census/get-filtered-census?filter=religion&filter_value=AT', format='json', follow = True)
        self.assertEqual(response.status_code, 200)
        users = response.json()

        self.assertEqual(len(users['users']), 0)

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

    def test_add_new_voters_conflict(self):
        data = {'voting_id': 1, 'voters': [1]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 409)

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

class CensusFrontTestCase(BaseTestCase):
    
    def setUp(self):
        super().setUp()
        self.census = Census(voting_id=1, voter_id=1)
        self.census.save()
    
    def tearDown(self):
        super().tearDown()
        self.census = None

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

    def test_list_census(self):
        self.login()
        response = self.client.get('/census/front/', format='json')
        self.assertEqual(response.status_code, 200)
            
    def test_list_census_400(self):
        response = self.client.get('/census/front/', format='json')
        self.assertEqual(response.status_code, 401)
            
        self.login(user='noadmin')
        response = self.client.get('/census/front/', format='json')
        self.assertEqual(response.status_code, 403)
    
    def test_create_census(self):
        self.login()
        data = {'voting_id': 2, 'voters': [1,2,3,4]}
            
        response = self.client.post('/census/front/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_census_400(self):
        data = {'voting_id': 2, 'voters': [1,2,3,4]}
            
        response = self.client.post('/census/front/', data, format='json')
        self.assertEqual(response.status_code, 401)
            
        self.login(user='noadmin')
        response = self.client.post('/census/front/', {}, format='json')
        self.assertEqual(response.status_code, 403)
        
    def test_delete_census(self):
        self.login()
        data = {'voting_id':1, 'voters': [1]}
        response = self.client.delete('/census/front/',data, format='json')
        self.assertEqual(response.status_code, 204)
        
    def test_delete_census_400(self):
        data = {'voting_id':1, 'voters': [1]}
            
        response = self.client.delete('/census/front/', data, format='json')
        self.assertEqual(response.status_code, 401)
            
        self.login(user='noadmin')
        response = self.client.delete('/census/front/', data, format='json')
        self.assertEqual(response.status_code, 403)