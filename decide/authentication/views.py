from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED,
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponse
from rest_framework import status
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .serializers import UserSerializer


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
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'user_pk': user.pk}, status=status.HTTP_201_CREATED)
