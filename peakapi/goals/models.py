from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Goal(models.Model):
	title = models.CharField(max_length=100)
	goalType = models.IntegerField(default=1)

class GoalChallenge(models.Model):
	title = models.CharField(max_length=100)
	attempts_to_complete = models.IntegerField(default=1)
	failure_amount = models.IntegerField(default=0)
	goal = models.ForeignKey(Goal, on_delete=models.PROTECT)

class GoalAttempt(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	current_completed = models.IntegerField(default=0)
	misess_remaining = models.IntegerField(default=0)
	goal_challenge = models.ForeignKey(GoalChallenge, on_delete=models.PROTECT)
	completed = models.BooleanField(default=False)




