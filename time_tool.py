#-*- coding: utf-8 -*-
import datetime

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








