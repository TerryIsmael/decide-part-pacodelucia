from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

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
        self.assertEqual(user['id'], 1)
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

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        u = User(username='yaexiste')
        u.set_password('yaexiste')
        u.save()

    def tearDown(self):
        self.client = None

    def test_registration_successful(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
        }

        response = self.client.post('/authentication/register/', data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_registration_missing_data(self):
        # Caso de test donde faltan datos requeridos
        data = {
            # Falta 'username'
            'password': 'testpassword',
            'email': 'test@example.com',
        }

        response = self.client.post('/authentication/register/', data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_registration_duplication_error(self):
        # Caso de test donde ocurre un IntegrityError (e.g., username duplicado)
        data = {
            'username': 'yaexiste',
            'password': 'testpassword',
            'email': 'new@example.com',
        }

        response = self.client.post('/authentication/register/', data, format='json')

        self.assertEqual(response.status_code, 400)

    def test_registration_not_mail(self):
        # Caso de test donde ocurre un IntegrityError (e.g., no se introduce un correo electrónico válido)
        data = {
            'username': 'testuser2',
            'password': 'testpassword2',
            'email': 'notanemail',
        }

        response = self.client.post('/authentication/register/', data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username='testuser').exists())
