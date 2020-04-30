from goals.models import Goal, GoalChallenge, GoalAttempt, GoalAttemptEntry
from rest_framework import serializers

class GoalChallengeSerializer(serializers.ModelSerializer):
	class Meta:
            model = GoalChallenge
            fields = '__all__'

class GoalAttemptSerializer(serializers.ModelSerializer):
	goal_challenge = GoalChallengeSerializer(many=False)

	class Meta:
            model = GoalAttempt
            fields = '__all__'
            extra_fields = ['goal_challenge']
