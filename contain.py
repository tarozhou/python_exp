#-*- coding: utf-8 -*-

#本文主要提供python中list  dict  string等各种列表容器的各类操作

import random

#列表去重的方法
def duplicate_removal():
    mylist=[1,2,2,3,4,5,5,6,7,8,9,9]
    new_list=[]

    for i in mylist:
        if i not in new_list:
            new_list.append(i)
    print new_list

    #转换成set
    new_list = list(set(mylist))
    print new_list


#字符串子串查找
def findstr():

    sub_str = "abc"
    mystr = "1111abcdefg"

    print mystr.find(sub_str)


#list 合并
def list_merge():

    list1=[1,2,3]
    list2=[2,3,4]

    list1.extend(list2)
    print list(set(list1))

    print list(set(list1+list2))


#合并2个dict
def merge_dict():

    dict1={1:[1,2],2:[3,4]}
    dict2={1:[4,5],2:[4,5],3:[6,7]}

    for key in dict2.keys():
        if dict1.has_key(key):
            dict1[key] = list(set(dict1[key]+dict2[key]))
        else:
            dict1[key] = dict2[key]

    print dict1

#生成一个随机不重复列表
def get_random_list():
    list = range(2,8)
    random.shuffle(list)
    print list[0:2]


#测试一下lamda
def lamda_test():

    print reduce(lambda a,b:a*b,[1,2,1,1,1])



lamda_test()



