from datetime import datetime, timedelta

def getStartOfAttemptCycleDate():
	return getStartOfAttemptCycle().date();

def getStartOfAttemptCycle():
	pub_date = datetime.today()
	min_pub_date_time = datetime.combine(pub_date, datetime.min.time())
	min_pub_date_time -= timedelta(hours=5) # UTC minus 5 is central
	return min_pub_date_time

def getEndOfAttemptCycleDate():
	return getEndOfAttemptCycle.date()

def getEndOfAttemptCycle():

	pub_date = datetime.today()
	max_pub_date_time = datetime.combine(pub_date, datetime.max.time())
	max_pub_date_time -= timedelta(hours=5) # UTC minus 5 is central
	return max_pub_date_time

	# from goals.time import getStartOfAttemptCycle
	# from goals.time import getEndOfAttemptCycle