# !/usr/bin/env python
# -*- coding: utf-8 -*-

import threading,time

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
