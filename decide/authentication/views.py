from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED,
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer
import secrets
import string


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
def generar_clave():
    # define the alphabet
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation

    alphabet = letters + digits + special_chars

    # fix password length
    pwd_length = 8

    # generate a password string
    pwd = ''
    for i in range(pwd_length):
        pwd += ''.join(secrets.choice(alphabet))

    return print(pwd)

def enviar_correo(email_destino, username):
    # Configurar los detalles del correo
    asunto = 'Autenticación de Registro en Decide.pacodelucia'
    mensaje = '¡Hola' + username +'! Gracias por registrarte en Decide.pacodelucia. Para completar el proceso de registro y asegurarnos de que tu dirección de correo electrónico sea válida, necesitamos que verifiques tu cuenta. Por favor, haz clic en el siguiente enlace para activar tu cuenta: ' +'http://localhost:5173/authentication/'+username+ ' Si no has solicitado este registro o crees que esto es un error, puedes ignorar este correo. Tu cuenta no se activará hasta que hayas hecho clic en el enlace de activación. ¡Gracias por unirte a nosotros en Decide.pacodelucia! Estamos emocionados de tenerte como parte de nuestra comunidad. Atentamente, El Equipo de Decide.pacodelucia'
    remitente = 'decide.pacodelucia@outlook.es'
    destinatarios = [email_destino]

    # Enviar el correo
    send_mail(asunto, mensaje, remitente, destinatarios)
    generar_clave()
    return HttpResponse('Correo enviado exitosamente.')

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        pwd = request.data.get('password', '')
        email = request.data.get('email', '')
        
        if not username or not pwd or not email:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username, email=email)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            enviar_correo(email,username)
        except IntegrityError:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'user_pk': user.pk, 'token': token.key}, status=status.HTTP_201_CREATED)


