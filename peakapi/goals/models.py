from django.db import models

# Create your models here.
class Goal(models.Model):
	title = models.CharField(max_length=100)
	goalType = models.IntegerField(default=1)

# class DailyGoal(models.Model):
# 	title = models.CharField(max_length=100)
# 	attempts_to_complete = models.IntegerField(default=1)
# 	failure_amount = models.IntegerField(default=0)
	



