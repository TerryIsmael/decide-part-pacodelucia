from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED,
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED,
        HTTP_404_NOT_FOUND
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponse
from rest_framework import status
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import authenticate, login
import json
from django.middleware.csrf import get_token
from .serializers import UserSerializer
from base.perms import UserIsStaff, UserIsAdminToken
import django_filters.rest_framework

class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)

class LogoutView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})
    
def es_correo_valido(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def encriptar(cadena):
    # Cambia el orden de los caracteres en la cadena
    cadena_encriptada = cadena.translate(str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA"))
    return cadena_encriptada

def desencriptar(cadena_encriptada):
    # Invierte la operación para obtener la cadena original
    cadena_original = cadena_encriptada.translate(str.maketrans("zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    return cadena_original

def enviar_correo(email_destino, username,password):
    # Configurar los detalles del correo
    asunto = 'Autenticación de Registro en Decide.pacodelucia'
    clave= str(encriptar(password))
    mensaje = '¡Hola ' + username +'! Gracias por registrarte en Decide.pacodelucia. Para completar el proceso de registro y asegurarnos de que tu dirección de correo electrónico sea válida, necesitamos que verifiques tu cuenta. Por favor, introduzca el siguiente codigo: '+clave+ ' Si no has solicitado este registro o crees que esto es un error, puedes ignorar este correo. Tu cuenta no se activará hasta que hayas introducido la clave de activación. ¡Gracias por unirte a nosotros en Decide.pacodelucia! Estamos emocionados de tenerte como parte de nuestra comunidad. Atentamente, El Equipo de Decide.pacodelucia'
    remitente = 'decide.pacodelucia@outlook.es'
    destinatarios = [email_destino]

    # Enviar el correo
    send_mail(asunto, mensaje, remitente, destinatarios)
    return HttpResponse('Correo enviado exitosamente.')

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        pwd = request.data.get('password', '')
        email = request.data.get('email', '')
        
        if not username or not pwd or not email:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        if not es_correo_valido(email):
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username, email=email)
            user.set_password(pwd)
            user.is_active=False
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            enviar_correo(email,username,pwd)
        except IntegrityError:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'user_pk': user.pk, 'token': token.key}, status=status.HTTP_201_CREATED)

class AuthView(APIView):
    def post(self, request):
        name = request.data.get('username', '')
        clave = request.data.get('clave', '')        
        if not name or not clave :
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_object_or_404(User, username=name)
            if user.check_password(desencriptar(clave)):
                user.is_active = True
                user.save()
            
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        return Response({'user_pk': user.pk, 'token': token.key}, HTTP_201_CREATED)

def getTokens(request):
    sessionid = request.COOKIES.get('sessionid', '')
    if sessionid == '':
        response = JsonResponse({}, status=HTTP_401_UNAUTHORIZED)
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    tokensList = []
    users = User.objects.all()
    for user in users:
        try:
            token = Token.objects.get(user=user)
            tokensList.append({'user': user.username, 'token': token.key, 'date': token.created.strftime("%b. %d, %Y, %I:%M %p"), 'id': user.id})
        except (ObjectDoesNotExist):
            tokensList.append({'user': user.username, 'token': '', 'date': '', 'id': user.id})        
    response = JsonResponse({'tokens': tokensList})
    response['Access-Control-Allow-Credentials'] = 'true'
    return response

def deleteToken(request, **kwargs):
    sessionid = request.COOKIES.get('sessionid', '')
    if sessionid == '':
        response = JsonResponse({}, status=HTTP_401_UNAUTHORIZED)
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    userId = kwargs.get('userId', '')
    if userId == '':
        response = JsonResponse({}, status=HTTP_400_BAD_REQUEST)
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    try:
        user = User.objects.get(id=userId)
        
        token = Token.objects.get(user=user)
        token.delete()
        response = JsonResponse({})
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    except (ObjectDoesNotExist):
        response = JsonResponse({}, status=HTTP_404_NOT_FOUND)
        response['Access-Control-Allow-Credentials'] = 'true'
        return response

def addToken(request, **kwargs):
    sessionid = request.COOKIES.get('sessionid', '')
    if sessionid == '':
        response = JsonResponse({}, status=HTTP_401_UNAUTHORIZED)
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    userId = kwargs.get('userId', '')
    if userId == '':
        response = JsonResponse({}, status=HTTP_400_BAD_REQUEST)
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    try:
        user = User.objects.get(id=userId)
        token, _ = Token.objects.get_or_create(user=user)
        response = JsonResponse({'user': user.username, 'token': token.key, 'date': token.created.strftime("%b. %d, %Y, %I:%M %p"), 'id': user.id})
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    except (ObjectDoesNotExist):
        response = JsonResponse({}, status=HTTP_404_NOT_FOUND)
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    
@csrf_exempt
def adminLogin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.is_staff:
                login(request, user)
                csrf_token = get_token(request)
                tk=Token.objects.get_or_create(user=user)
                response = JsonResponse({'message': 'Login exitoso', 'sessionid': request.session.session_key})
                response.set_cookie('csrftoken', csrf_token, samesite='Lax')
                response.set_cookie('auth-token', tk[0].key, samesite='Lax')
                
                return response
            else:
                return JsonResponse({'message': 'Credenciales incorrectas'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Formato JSON incorrecto en la petición'}, status=400)
    return JsonResponse({'message': 'Método no permitido'}, status=405)      

@ensure_csrf_cookie
def isAdmin(request):
    sessionid = request.COOKIES.get('sessionid', '')
    try:
        session = Session.objects.get(session_key=sessionid)
        user_id = session.get_decoded().get('_auth_user_id')

        user = User.objects.get(id=user_id)

        user_data = {
            'is_authenticated': user.is_authenticated,
            'is_staff': user.is_staff if user.is_authenticated else False,
            'username': user.username if user.is_authenticated else None,
        }
        return JsonResponse({'user_data': user_data})
    except Exception as _:
        return JsonResponse({'user_data': {'is_authenticated': False, 'is_staff': False, 'username': None}})

class UserView(APIView):

    permission_classes = (UserIsStaff,)
    serializer_class = UserSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(User.objects.all(), many=True).data)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('id', None)
        username = request.data.get('username', '')
        pword = request.data.get('password', '')

        if not username or (not user_id and not pword):
            return Response({}, status=HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email', '')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        is_staff = request.data.get('is_staff', '')
        is_active = request.data.get('is_active', '')
        is_superuser = request.data.get('is_superuser', '')

        try:
            user = User(id=user_id,username=username, email=email, first_name=first_name, last_name=last_name, is_staff=is_staff, is_active=is_active, is_superuser=is_superuser)
            if(pword is None or pword != ''):
                user.set_password(pword)
            elif user_id != '':
                user.password = User.objects.get(id=user_id).password
            else:
                return Response({}, status=HTTP_400_BAD_REQUEST)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        
        return Response({'user_pk': user.pk, 'token': token.key}, HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user_id = request.data.get('id', '')
        
        if not user_id:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            user.delete()
        
        except ObjectDoesNotExist:
            return Response({}, status=HTTP_404_NOT_FOUND)
        return Response({})

class UserFrontView(APIView):

    permission_classes = (UserIsAdminToken,)
    serializer_class = UserSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(User.objects.all(), many=True).data)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('id', None)
        username = request.data.get('username', '')
        pword = request.data.get('password', '')

        if not username or (not user_id and not pword):
            return Response({}, status=HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email', '')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        is_staff = request.data.get('is_staff', '')
        is_active = request.data.get('is_active', '')
        is_superuser = request.data.get('is_superuser', '')

        try:
            user = User(id=user_id,username=username, email=email, first_name=first_name, last_name=last_name, is_staff=is_staff, is_active=is_active, is_superuser=is_superuser)
            if(pword is None or pword != ''):
                user.set_password(pword)
            elif user_id != '':
                user.password = User.objects.get(id=user_id).password
            else:
                return Response({}, status=HTTP_400_BAD_REQUEST)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        
        return Response({'user_pk': user.pk, 'token': token.key}, HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user_id = request.data.get('id', '')
        
        if not user_id:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            user.delete()
        
        except ObjectDoesNotExist:
            return Response({}, status=HTTP_404_NOT_FOUND)
        return Response({})
