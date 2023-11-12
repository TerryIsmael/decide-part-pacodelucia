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

def enviar_correo(email_destino):
    # Configurar los detalles del correo
    asunto = 'Asunto del Correo'
    mensaje = 'Hola, este es un mensaje de prueba.'
    remitente = 'decide.pacodelucia@gmail.com'
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

        try:
            user = User(username=username, email=email)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            enviar_correo(email)
        except IntegrityError:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'user_pk': user.pk, 'token': token.key}, status=status.HTTP_201_CREATED)


