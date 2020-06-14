#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Author:AkulaKirov
@Blog: akulak.top
@License: MPL 2.0
@Version 1.1
'''

import requests
import json
import os
import hashlib
import random

url = 'http://www.xszongping.com/Health/EpidemicHealthRecord/postHealth'
checkToken = 'http://www.xszongping.com/School/PatriarchEpidemic/checkToken'
checkTokenT = 'http://www.xszongping.com/School/User/checkToken'
token = ''
userName = '未登入'
rdm = False

def cls() : 
    os.system('cls')

'''    #已弃用
def loginPat() :
    u = 'http://www.xszongping.com/School/PatriarchEpidemic/login'
    headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8"}
    info = 'password=pwd&phone=PHONE'
    PHONE = input("请输入电话：")
    pwd = input("请输入密码（身份证后六位）：")
    info = info.replace("pwd",pwd)
    info = info.replace("PHONE",PHONE)
    print ('Trying...')
    response = requests.post(u, data = info.encode('utf-8'), headers = headers)
    status = json.loads(response.text)
    data = status["data"]
    print ('状态:',status["message"])
    #print (status)
    #print (data)
    global token 
    token = data["token"]
    print ('token updated:',data["token"])
    return token
'''
def loginTec() :
    u = 'http://www.xszongping.com/School/User/loginMobile'
    headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8"}
    info = 'account=ACT&password=PWD&school_id=27'
    acc = input('请输入教工号：')
    pwd = input('请输入密码：')
    pwd = hashlib.md5(pwd.encode(encoding='UTF-8')).hexdigest()
    info = info.replace('ACT',acc)
    info = info.replace('PWD',pwd)
    response = requests.post(u, data = info.encode('utf-8'), headers = headers)
    status = json.loads(response.text)
    data = status["data"]
    print ('状态:',status["message"])
    #print (status)
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

def fill(stu) :
    global token
    global rdm
    global wh
    TEMP = 0.0
    if token == '' :
        token = input("请输入token：")

    #在这里更改地区以及班级id
    survey = 'animal_heat=TEMP&city=350000&city_name=福州市&county=350105&county_name=马尾区&grade_id=75&is_case=1&is_family_health=2&is_fever=2&is_health=1&is_hoose=2&is_leave=2&is_other_case_history=2&is_touch_abroad=2&is_touch_area=2&patriarch_id=6938&province=350000&province_name=福建省&record_phone=PHONE&school_id=27&student_id=IDS'
    headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8", 'token': token}
    print ("当前学生：", stu["student_name"])
    if rdm == True :
        print ('注意：随机数模式已启用！！！')
    o = input("输入i进行填写 输入s跳过 输入其他键退出：")
    if o == 'i' :
        if rdm == True :
            TEMP = str(float(random.randint(360, 367))/10.0)  #要是用random.uniform会生成精度太高的float 先这样写了
        else :
            TEMP = input('请输入温度 保留一位小数:')
        
        survey = survey.replace("TEMP",TEMP)
        survey = survey.replace("PHONE",stu["phone"])
        survey = survey.replace("IDS",str(stu["student_id"]))
        print ('请核对信息：',stu["student_name"] , TEMP, '摄氏度')
        i = input('确定请按回车 按其他任意键退出:')
        if i != '' :
            return True
        response = requests.post(url, data = survey.encode('utf-8'), headers = headers)
        # 返回信息
        status = json.loads(response.text)
        print ('状态：',status["message"])
        # 返回响应头
        print (response.status_code)
        input('>>按任意键填写下一个')
        return False
    elif o == 's' :
        return False
    else :
        return True

def getStudent() :
    global token
    #gradeId = '75' #2017级高三 暂时用不到
    classId = '809' #8班
    get = 'http://www.xszongping.com/Health/EpidemicHealthRecord/getRecordListByTypeFromSchool'
    headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8", 'token': token}
    post = 'class_ids%5B%5D=CLASSID&no_record=1&page=1&size=60'
    post = post.replace('CLASSID', classId)
    #post = 'no_record=1&page=1&size1=60'    #测试用 实际情况用上一个
    response = requests.post(get, data = post.encode('utf-8'), headers = headers)
    data = json.loads(response.text)
    print ('状态：',data["message"])
    data = data["data"]
    studentList = data["list"]
    print ('所有学生未填写人数:',data["total"])
    if data["total"] == 0 :
        input ('无可填写学生 按任意键返回主菜单')
        return
    print ('学生姓名:')
    for stu in studentList :
        print (stu["student_name"])

    o = input('1.从第一个开始填写 任意其他键.返回主菜单')
    if o == '1' : 
        for a in studentList :
            flag = fill(a)
            if flag == True :
                break
    else :
        return
    return

def wooHoo() :
    global token
    total = 0
    #gradeId = '75' #2017级高三 暂时用不到
    classId = '814' #9班/809
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
    input()

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
    

def secretMode () :
    global rdm
    print ('###终极秘密模式###')
    if rdm == False :
        rdm = True
        print ('随机体温模式已启用')
    else :
        rdm = False
        print ('随机体温模式已禁用')

exit = '1'
while exit != 'q' :
    cls()
    print ('===================================')
    print ('=          福建师大二附中         =')
    print ('========健康报备自动填写脚本=======')
    print ('Made by AkulaKirov')
    print ('Lisence: MPL 2.0')
    print ('===================================')
    print ('欢迎你：',userName)
    print ('注意：当前设定默认为福建省福州市马尾区 福建师大二附中 2017级9班')
    print ('1.教师登入 2.查看学生 3.随机体温模式 4.一键起飞 q.退出')
    q = input('请输入选项：')
    if q == '1' :
        loginTec()
        cls()
    elif q == '2' :
        getStudent()
        cls()
    elif q == '3' :
        secretMode()
        input()
        cls()
    elif q == '4' :
        wooHoo()
        cls()
    elif q == 'q' :
        exit = 'q'
        break
    else :
        print ('输入错误 请重新输入')
        input()




