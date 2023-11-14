from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED,
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED,
        HTTP_404_NOT_FOUND
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

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


class RegisterView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        if not tk.user.is_superuser:
            return Response({}, status=HTTP_401_UNAUTHORIZED)

        username = request.data.get('username', '')
        pwd = request.data.get('password', '')
        if not username or not pwd:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
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
