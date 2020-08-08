from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.core import serializers
from django.http import HttpResponse, JsonResponse

from django.forms.models import model_to_dict
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from requests.exceptions import HTTPError

from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from peakapi.socialserializer import SocialSerializer
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User

from peakapi.throttles import BurstRateThrottle

import json

@csrf_exempt
@api_view(["POST"])
@throttle_classes([AnonRateThrottle])
@permission_classes((AllowAny,))
def signup(request):
    username = request.data.get("user_name")
    password = request.data.get("password")
    email = request.data.get("email")
    if username is None or password is None or email is None:
        return Response({'error': 'Please provide a username, password, and email'},
                        status=HTTP_400_BAD_REQUEST)

    matching_users = User.objects.filter(username=username)
    if matching_users.exists():
        return Response({'error': 'Username already taken'},
                        status=HTTP_400_BAD_REQUEST)

    matching_users = User.objects.filter(email=email)
    if matching_users.exists():
        return Response({'error': 'Email already taken'},
                        status=HTTP_400_BAD_REQUEST)

    try:
        validate_email(email)
    except ValidationError as e:
        return Response({'error': 'Email invalid'},
                        status=HTTP_400_BAD_REQUEST)
    else:
        user = User.objects.create_user(username, email, password)
        token, _ = Token.objects.get_or_create(user=user)
        user_dic = model_to_dict(user)
        token_dic = model_to_dict(token)
        return JsonResponse({"user": user_dic, "token": token.key})

@csrf_exempt
@api_view(["POST"])
@throttle_classes([AnonRateThrottle])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("user_name")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)

    user_dic = model_to_dict(user)
    token_dic = model_to_dict(token)
    
    return JsonResponse({"user": user_dic, "token": token.key})

@csrf_exempt
@api_view(["POST"])
@throttle_classes([BurstRateThrottle])
@permission_classes((AllowAny,))
def loginFromAccessToken(request):
    access_token = request.data.get("access_token")
    user_id = request.data.get("user_id")

    if access_token is None or user_id is None:
        return Response({'error': 'error logging in.'},
                        status=HTTP_400_BAD_REQUEST)
    fullToken = Token.objects.select_related('user').get(pk=access_token)
    if fullToken is None:
        return Response({'error': 'error logging in.'},
                        status=HTTP_400_BAD_REQUEST)

    user = fullToken.user

    if int(user.pk) != int(user_id):
        return Response({'error': 'cannot log in.'},
                        status=HTTP_400_BAD_REQUEST)

    user_dic = model_to_dict(user)

    return JsonResponse({"user": user_dic, "token": access_token})


@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    data = {'sample_data': 123}
    return Response(data, status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
def logout(request):
        request.user.auth_token.delete()
        return JsonResponse({"success": "successfully logged out"})

@csrf_exempt
@api_view(["POST"])
@throttle_classes([AnonRateThrottle])
@permission_classes((AllowAny,))
def postFacebookLogin(request):
            """Authenticate user through the provider and access_token"""
            serializer = SocialSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            provider = serializer.data.get('provider', None)
            strategy = load_strategy(request)

            try:
                backend = load_backend(strategy=strategy, name=provider,
                redirect_uri=None)

            except MissingBackend:
                return Response({'error': 'Please provide a valid provider'},
                status=status.HTTP_400_BAD_REQUEST)
            try:
                if isinstance(backend, BaseOAuth2):
                    access_token = request.data.get('access_token')
                    if access_token is None:
                        return Response({'error': 'Please provide a valid provider'},
                            status=status.HTTP_400_BAD_REQUEST)
                user = backend.do_auth(access_token)
            except HTTPError as error:
                return Response({
                    "error": {
                        "access_token": "Invalid token",
                        "details": str(error)
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
            except AuthTokenError as error:
                return Response({
                    "error": "Invalid credentials",
                    "details": str(error)
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                authenticated_user = backend.do_auth(access_token, user=user) 
            except HTTPError as error:
                return Response({
                    "error":"invalid token",
                    "details": str(error)
                }, status=status.HTTP_400_BAD_REQUEST)
        
            except AuthForbidden as error:
                return Response({
                    "error":"invalid token",
                    "details": str(error)
                }, status=status.HTTP_400_BAD_REQUEST)

            if authenticated_user and authenticated_user.is_active:
                token, _ = Token.objects.get_or_create(user=authenticated_user)

                user_dic = model_to_dict(authenticated_user)

                token_dic = model_to_dict(token)

                return JsonResponse({"user": user_dic, "token": token.key})
            else:
                return Response({
                    "error": "Unexpected error",
                    "details": "User could not be authorized"
                }, status=status.HTTP_400_BAD_REQUEST)

