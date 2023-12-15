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

        

    def test_register_view(self):
        # Realizar una solicitud POST a la vista de registro y comprubar si el usuario isActive
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
        }

        self.client.post('/authentication/register/', data)
        user = User.objects.get(username=data['username'])       
        self.assertFalse(user.is_active)

    def test_register_view_code_201(self):
        # Realizar una solicitud POST a la vista de registro y comprubar si el usuario isActive
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
        }

        response = self.client.post('/authentication/register/', data)

        self.assertEqual(response.status_code, 201)

    def test_auth_view_successful(self):
        # Realizar una solicitud POST a la vista de autenticación

        data_register = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
        }

        self.client.post('/authentication/register/', data_register)

        data = {
                'username': 'testuser', 
                'clave': 'gvhgkzhhdliw'
                }

        url = ('/authentication/authEmail/')  
        self.client.post(url, data)
        user = User.objects.get(username='testuser')

        self.assertTrue(user.is_active)


    def test_auth_view_successful_code_201(self):
        # Realizar una solicitud POST a la vista de autenticación

        data_register = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
        }

        self.client.post('/authentication/register/', data_register)

        data = {
                'username': 'testuser', 
                'clave': 'gvhgkzhhdliw'
                }

        url = ('/authentication/authEmail/')  
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)

    def test_auth_view_invalid_data(self):
        # Realizar una solicitud POST a la vista de autenticación con datos incompletos

        data_register = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
        }

        self.client.post('/authentication/register/', data_register)

        data = {'username': 'testuser'}

        url = ('/authentication/authEmail/')  
        self.client.post(url, data)
        user = User.objects.get(username='testuser')
        self.assertFalse(user.is_active)

    def test_auth_view_invalid_data_code_400(self):
        # Realizar una solicitud POST a la vista de autenticación con datos incompletos

        data_register = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
        }

        self.client.post('/authentication/register/', data_register)

        data = {'username': 'testuser'}

        url = ('/authentication/authEmail/')  
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)

    def test_auth_view_invalid_credentials(self):
        # Realizar una solicitud POST a la vista de autenticación con credenciales incorrectas

        data_register = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
        }

        self.client.post('/authentication/register/', data_register)
        data = {'username': 'testuser', 'clave': 'incorrect_password'}

        url = ('/authentication/authEmail/')  
        self.client.post(url, data)
        user = User.objects.get(username='testuser')
        self.assertFalse(user.is_active)

    def test_auth_view_invalid_credentials_code_201(self):
        # Realizar una solicitud POST a la vista de autenticación con credenciales incorrectas

        data_register = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
        }

        response = self.client.post('/authentication/register/', data_register)
        data = {'username': 'testuser', 'clave': 'incorrect_password'}

        url = ('/authentication/authEmail/')  
        response = self.client.post(url, data)

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

    def test_get_tokens_not_logged(self):
        response = self.client.get('/authentication/get-auth/', format='json')
        self.assertEqual(response.status_code, 401)

        tokens = response.json()
        self.assertTrue(tokens.get('tokens') == None)
