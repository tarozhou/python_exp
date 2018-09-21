import time
import datetime

def is_int(s):
	try:
		int(s)
		return True
	except (ValueError,TypeError):
		pass
	return False

def get_hours_before(hours,itime=None):
	itime=itime or int(time.time())
	return itime-hours*3600

def from_unixtime(itime):
	return datetime.datetime.fromtimestamp(itime).strftime('%Y-%m-%d %H:%M:%S')

def getlingchentime(itime=None):
	itime = itime or int(time.time())
	return itime-itime%86400-8*3600

def to_unixtime(itime,format='%Y-%m-%d %H:%M:%S'):
	return int(time.mktime(time.strptime(itime,format)))



