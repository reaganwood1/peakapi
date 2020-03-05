from django.shortcuts import render
from goals.models import Goal, GoalChallenge, GoalAttempt

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
from django.http import HttpResponse
import json

@csrf_exempt
@api_view(["GET"])
def get_goals(request):
	goals = Goal.objects.all()
	response = serializers.serialize("json", goals)
	return HttpResponse(response, content_type='application/json')

@csrf_exempt
@api_view(["POST"])
def post_goal(request):
   	title = request.data.get("title")
   	if title is None:
   		return Response({'error': 'Please provide a title'},
                        status=HTTP_400_BAD_REQUEST)
   	# check if the title already exists
   	matching_results = Goal.objects.filter(title=title)
   	if matching_results.exists():
   		return Response({'error': 'This goal already exists'},
                        status=HTTP_400_BAD_REQUEST)

   	goal = Goal(title=title, goalType=1)
   	goal.save()

   	values = []
   	values.append(goal)

   	response = serializers.serialize("json", values)

   	return HttpResponse(response, content_type='application/json')

@csrf_exempt
@api_view(["POST"])
def post_goal_challenge(request):
   	title = request.data.get("title")
   	attempts_to_complete = request.data.get("attempts_to_complete")
   	failure_amount = request.data.get("failure_amount")
   	goal_id = request.data.get("goal_id")

   	if title is None or attempts_to_complete is None or failure_amount is None or goal_id is None:
   		return Response({'error': 'Please provide a title, attempts to complete, and a failure amount'},
                        status=HTTP_400_BAD_REQUEST)
   	# check if the title already exists
   	#TODO: check for identical ones

   	matching_goal = Goal.objects.get(pk=goal_id)
   	if matching_goal is None:
   		return Response({'error': 'Goal not found'},
                        status=HTTP_400_BAD_REQUEST)


   	goal_attempt = GoalChallenge(title=title,
   		attempts_to_complete=attempts_to_complete, failure_amount=failure_amount, goal=matching_goal)
   	goal_attempt.save()

   	values = []
   	values.append(goal_attempt)

   	response = serializers.serialize("json", values)

   	return HttpResponse(response, content_type='application/json')

@csrf_exempt
@api_view(["GET"])
def get_goal_challenges(request):
	challenges = GoalChallenge.objects.all()

	response = serializers.serialize("json", challenges)
	return HttpResponse(response, content_type='application/json')

@csrf_exempt
@api_view(["POST"])
def post_user_goal_attempt(request, id):
   	user = request.user
   	#TODO: check for identical ones

   	matching_goal_challenge = GoalChallenge.objects.get(pk=id)
   	if matching_goal_challenge is None:
   		return Response({'error': 'Goal challenge not found'},
                        status=HTTP_400_BAD_REQUEST)


   	goal_attempt = GoalAttempt(user=user,
   		misess_remaining=matching_goal_challenge.failure_amount, goal_challenge=matching_goal_challenge)
   	goal_attempt.save()

   	values = []
   	values.append(goal_attempt)

   	response = serializers.serialize("json", values)

   	return HttpResponse(response, content_type='application/json')
