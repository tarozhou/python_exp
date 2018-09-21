# !/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import random
from numpy import random,mat
import threading,time
import json
import urllib,urllib2


'''
a = [1,2,3,4,5,6,7]

print a[-2::-1]

for i in range(3):
    print i


name=u'测试'
print name
print type(name)
print len(name)
name=name.encode('utf-8')
print name
print type(name)
print len(name)
'''
#print np.random.uniform(-0.1, 0.1,(3, 3))

'''
a=np.array([0,1,2,3,4,5,6])

d = mat([0,1,2,3,4,5,6])


b = np.zeros(7)


c = np.zeros((7,1))


print c

print c*(1-c)

'''

'''
def sub():

    global fp_write
    global res_list
    global id_list
    global cnt

    idx = 0
    if lockb.acquire(True):
        idx = id_list[0]
        id_list.pop(0)
        lockb.release()

    print idx,threading.current_thread().name

    while(cnt>0):
        if lock.acquire(True):
            arr = res_list[cnt].replace("\n","").split("|")
            if len(arr)==3:
                uin = arr[0]+"\n"
                fp_write.writelines(uin)
            cnt=cnt-1
            lock.release()


start = time.time()
fp_read = open("idex_1536824241749.csv", "r")
res_list = fp_read.readlines()
fp_write = open("4.txt","a")
l = []
id_list=range(1,101)
cnt=len(res_list)-1
lock = threading.Lock()
lockb = threading.Lock()
for i in range(100):
    t = threading.Thread(target=sub,args=())
    t.start()
    l.append(t)

for t in l:
    t.join()
end = time.time()

fp_write.close()
print "cost time:",(end-start)
'''

'''
start = time.time()
fp_read = open("idex_1536824241749.csv", "r")

for one_line in fp_read.readlines():
    arr = one_line.replace("\n", "").split("|")
    if len(arr) == 3:
        uin = int(arr[0])
end = time.time()
print "cost time:",(end-start)
'''

post_url="http://100.109.224.116:8900/lolrecallpost/"

postData  = {}
postData['credid'] = 'qq.ad.app_zm'
postData['flowid'] = '1'
postData['reqtype'] = '3'
postData['sceneid'] = '90002'
postData['userid'] = '305407878'
postData['version'] = '1'

data={}
data['channel']='1'
data['reset']='1'
data['slidetype']='0'
data['version']='1.1'
postData['data']=data

json_data = json.dumps(postData)

req = urllib2.Request(post_url)

rsp = urllib2.urlopen(post_url,urllib.urlencode({"param":json_data}))

print rsp.read()








