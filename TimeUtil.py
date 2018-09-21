#-*- coding: utf-8 -*-

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


#时间基本操作
def datetime_tool():

	#获取当前时间
    dtime = datetime.datetime.now()

	#将unix时间转换成datetime对象
    time = datetime.datetime.fromtimestamp(1534777341)


#获取unix时间和当前时间的时间差
def _gethourdiff_():

	dtime = datetime.datetime.now()
	time = datetime.datetime.fromtimestamp(1534777341)

	daydiff = (dtime - time).days
	secdiff = (dtime - time).seconds

	hourdiff = (daydiff*86400 + secdiff)/3600

	return hourdiff

