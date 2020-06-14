#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Author:AkulaKirov
@Blog: akulak.top
@License: MPL 2.0
@Version 0.1_pre_alpha
'''
import requests
import json
import os
import hashlib
import random

url = 'http://www.xszongping.com/Health/EpidemicHealthRecord/postHealth'
checkToken = 'http://www.xszongping.com/School/PatriarchEpidemic/checkToken'
checkTokenT = 'http://www.xszongping.com/School/User/checkToken'
surveyT = 'animal_heat=TEMP&city=350100&city_name=福州市&county=350105&county_name=马尾区&epidemic_health_id=EIDS&is_case=1&is_family_health=2&is_fever=2&is_health=1&is_hoose=2&is_leave=2&is_other_case_history=2&is_touch_abroad=2&is_touch_area=2&province=350000&province_name=福建省&student_id=SIDS&user_type=2'

class Account :
    acc = ''
    pwd = ''
    isTeacher = True
    token = ''

    def __init__(self, acc, pwd, isTeacher):
      self.acc = acc
      self.pwd = pwd
      self.isTeacher = isTeacher

def login(a) :
    u = 'http://www.xszongping.com/School/PatriarchEpidemic/login'
    u2 = 'http://www.xszongping.com/School/User/loginMobile'
    headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8"}
    info = 'password=pwd&phone=PHONE'
    PHONE = a.acc
    pwd = a.pwd
    if (a.isTeacher == True) :
        pwd = hashlib.md5(pwd.encode(encoding='UTF-8')).hexdigest()
    info = info.replace("pwd",pwd)
    info = info.replace("PHONE",PHONE)
    print ('Trying...')
    if (a.isTeacher == True) :
        response = requests.post(u2, data = info.encode('utf-8'), headers = headers)
    else :
        response = requests.post(u, data = info.encode('utf-8'), headers = headers)
    status = json.loads(response.text)
    data = status["data"]
    print ('状态:',status["message"])
    #print (status)
    #print (data)
    a.token = data["token"]
    print ('token updated:',data["token"])
    

def fastFill (a, token, isTeacher) :
    token
    survey = 'animal_heat=TEMP&city=350000&city_name=福州市&county=350105&county_name=马尾区&grade_id=75&is_case=1&is_family_health=2&is_fever=2&is_health=1&is_hoose=2&is_leave=2&is_other_case_history=2&is_touch_abroad=2&is_touch_area=2&patriarch_id=6938&province=350000&province_name=福建省&record_phone=PHONE&school_id=27&student_id=IDS'
    if (a.isTeacher == True) :
        survey = surveyT
    headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8", 'token': token}
    TEMP = str(float(random.randint(360, 367))/10.0)  #要是用random.uniform会生成精度太高的float 先这样写了
    survey = survey.replace("TEMP",TEMP)
    if (a.isTeacher == True) :
        survey = survey.replace("EIDS",str(a["epidemic_health_id"]))
        survey = survey.replace("SIDS",str(a["student_id"]))
    else :
        survey = survey.replace("PHONE",a["phone"])
        survey = survey.replace("IDS",str(a["student_id"]))
    response = requests.post(url, data = survey.encode('utf-8'), headers = headers)
    # 返回信息
    status = json.loads(response.text)
    print ('状态：',status["message"])







liubin = Account('13405928271', '111111', True)

s = set()
s.add(liubin)

for a in s :
    login(a)




