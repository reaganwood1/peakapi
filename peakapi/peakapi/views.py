from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
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
import json


@csrf_exempt
@api_view(["POST"])
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