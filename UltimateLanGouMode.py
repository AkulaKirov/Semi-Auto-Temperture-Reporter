#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Author:AkulaKirov
@Blog: akulak.top
@License: MPL 2.0
@Version 1.0
'''

import requests
import json
import hashlib
import random

url = 'http://www.xszongping.com/Health/EpidemicHealthRecord/postHealth'
checkTokenT = 'http://www.xszongping.com/School/User/checkToken'
userName = ''
token = ''
acc = '114514'
pwd = '114514'

def wooHoo() :
    global token
    total = 0
    #gradeId = '75' #2017级高三 暂时用不到
    classId = '809' #9班/809
    get = 'http://www.xszongping.com/Health/EpidemicHealthRecord/getRecordListByTypeFromSchool'
    headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8", 'token': token}
    post = 'class_ids%5B%5D=CLASSID&no_record=1&page=1&size=60'
    post = post.replace('CLASSID', classId)
    #post = 'no_record=1&page=1&size1=60'    #测试用 实际情况用上一个
    print ('准备开始获取学生名单')
    response = requests.post(get, data = post.encode('utf-8'), headers = headers)
    data = json.loads(response.text)
    print ('状态：',data["message"])
    data = data["data"]
    studentList = data["list"]
    print ('获取了', data["total"], '名学生 准备开始填写...')
    for stu in studentList :
        fastFill(stu)
        total = total + 1
    print ('结束 填写了 ', data["total"], '中的', total, '人')

def fastFill (stu) :
    global token
    survey = 'animal_heat=TEMP&city=350000&city_name=福州市&county=350105&county_name=马尾区&grade_id=75&is_case=1&is_family_health=2&is_fever=2&is_health=1&is_hoose=2&is_leave=2&is_other_case_history=2&is_touch_abroad=2&is_touch_area=2&patriarch_id=6938&province=350000&province_name=福建省&record_phone=PHONE&school_id=27&student_id=IDS'
    headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8", 'token': token}
    TEMP = str(float(random.randint(360, 367))/10.0)  #要是用random.uniform会生成精度太高的float 先这样写了
    survey = survey.replace("TEMP",TEMP)
    survey = survey.replace("PHONE",stu["phone"])
    survey = survey.replace("IDS",str(stu["student_id"]))
    response = requests.post(url, data = survey.encode('utf-8'), headers = headers)
    # 返回信息
    status = json.loads(response.text)
    print (stu["student_name"],'  状态：',status["message"])

def loginTec() :
    u = 'http://www.xszongping.com/School/User/loginMobile'
    headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8"}
    info = 'account=ACT&password=PWD&school_id=27'
    global pwd, acc
    pwdmd5 = hashlib.md5(pwd.encode(encoding='UTF-8')).hexdigest()
    info = info.replace('ACT',acc)
    info = info.replace('PWD',pwdmd5)
    response = requests.post(u, data = info.encode('utf-8'), headers = headers)
    status = json.loads(response.text)
    data = status["data"]
    print ('状态:',status["message"])
    print (status)
    #print (data)
    global token 
    token = data["token"]
    print ('token updated:',data["token"])
    body = 'token=' + token
    response = requests.post(checkTokenT, data = body.encode('utf-8'), headers = headers)
    status = json.loads(response.text)
    #print (status)
    data = status["data"]
    global userName 
    userName = data["user_name"]
    #print (userName)
    return token

print ('===================================')
print ('=          福建师大二附中         =')
print ('========    究极懒狗模式    =======')
print ('Made by AkulaKirov')
print ('Lisence: MPL 2.0')
print ('2017级9班专供')
print ('===================================')
print ('尝试登录...')
try :
    token = loginTec()
except :
    print('登录时遇到错误,即将退出...')
    quit()
else :
    print('登录成功,欢迎您:', userName)
print('开始尝试填写所有学生体温...')
wooHoo()
print('已完成,按任意键退出')
input()
quit()
