from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



from base.tests import BaseTestCase
from base import mods


class AuthTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='voter1')
        u.set_password('123')
        u.save()

        u2 = User(username='admin')
        u2.set_password('admin')
        u2.is_superuser = True
        u2.is_staff = True
        u2.save()
    def tearDown(self):
        self.client = None

    def test_login(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('token'))

    def test_login_fail(self):
        data = {'username': 'voter1', 'password': '321'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_getuser(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertEqual(user['username'], 'voter1')

    def test_getuser_invented_token(self):
        token = {'token': 'invented'}
        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_getuser_invalid_token(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 0)

    def test_register_bad_permissions(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 401)

    def test_register_bad_request(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register_user_already_exist(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update(data)
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1', 'password': 'pwd1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            sorted(list(response.json().keys())),
            ['token', 'user_pk']
        )

    def test_admin_login(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login-auth/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('message') == 'Login exitoso')
        self.assertTrue(token.get('sessionid') != '' and token.get('sessionid') != None)

    def test_admin_login_bad_credentials(self):
        data = {'username': 'admin', 'password': '123'}
        response = self.client.post('/authentication/login-auth/', data, format='json')
        self.assertEqual(response.status_code, 401)

        token = response.json()
        self.assertTrue(token.get('message') == 'Credenciales incorrectas')
        self.assertTrue(token.get('sessionid') == '' or token.get('sessionid') == None)

    def test_admin_login_bad_request(self):
        data = {'username': 'admin'}
        response = self.client.get('/authentication/login-auth/', data, format='json')
        self.assertEqual(response.status_code, 405)

        token = response.json()
        self.assertTrue(token.get('message') == 'Método no permitido')
        self.assertTrue(token.get('sessionid') == '' or token.get('sessionid') == None)

    def test_admin_login_bad_json(self):
        response = self.client.post('/authentication/login-auth/', format='json')
        self.assertEqual(response.status_code, 400)

        token = response.json()
        self.assertTrue(token.get('message') == 'Formato JSON incorrecto en la petición')
        self.assertTrue(token.get('sessionid') == '' or token.get('sessionid') == None)

    def test_is_admin(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login-auth/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('message') == 'Login exitoso')
        self.assertTrue(token.get('sessionid') != '' and token.get('sessionid') != None)

        response = self.client.get('/authentication/admin-auth/', format='json')
        credentials = response.json()
        self.assertTrue(credentials.get('user_data').get('is_authenticated') == True)
        self.assertTrue(credentials.get('user_data').get('is_staff') == True)
        self.assertTrue(credentials.get('user_data').get('username') != '' and credentials.get('user_data').get('username') != None)

    def test_is_admin_not_logged(self):
        response = self.client.get('/authentication/admin-auth/', format='json')
        credentials = response.json()
        self.assertTrue(credentials.get('user_data').get('is_authenticated') == False)
        self.assertTrue(credentials.get('user_data').get('is_staff') == False)
        self.assertTrue(credentials.get('user_data').get('username') == '' or credentials.get('user_data').get('username') == None)

    def test_get_tokens(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login-auth/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('message') == 'Login exitoso')
        self.assertTrue(token.get('sessionid') != '' and token.get('sessionid') != None)

        response = self.client.get('/authentication/get-auth/', format='json')
        self.assertEqual(response.status_code, 200)

        tokens = response.json()
        self.assertTrue(len(tokens.get('tokens')) == 2)

