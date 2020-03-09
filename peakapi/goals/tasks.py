from background_task import background
from django.contrib.auth.models import User
from goals.models import Goal, GoalChallenge, GoalAttempt, GoalAttemptEntry

# TODO: fix task scheduler
@background(schedule=30)
def add_failure_at_start_of_day():
    goal_attempts = GoalAttempt.objects.filter(misess_remaining >= 0, completed=False)

    for goal_attempt in goal_attempts:
    	clear_goal_attempt(goal_attempt)
    


def clear_goal_attempt(goalAttempt: GoalAttempt):
	print("BOOM")
	print("RUNNING THIS")
	#chech if there is an entry sooner than today
	todayMinusOneDayDateTime = datetime.today() - timedelta(days=1)
	today = todayMinusOneDayDateTime.date()

	entrys = GoalAttemptEntry.objects.filter(goal_attempt=goalAttempt)

	for entry in entrys:
		if entry.created_at.date() >= today:
			return


	print("SUBTRACTING")
	goalAttempt.misess_remaining -= 1
	goalAttempt.save()