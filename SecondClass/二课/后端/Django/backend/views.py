from django.http import JsonResponse
from django.views.decorators.http import require_POST
from backend.models import UserProfile
import json
import requests
import datetime
import time
import random
from django.conf import settings
from django.http import HttpResponse


import os


@require_POST
def login(request):
    data = json.loads(request.body)

    username = data['username']
    password = data['password']
    encrypt = data['encrypt']

    request.session['username'] = username
    request.session['user_agent'] = data['user_agent']['User-Agent']

    dic = {
        "username": username,
        "password": password,
        "validateCode": "",
        "loginType": "",
        "redirectUrl": ""
    }
    headers = {
        'User-Agent': request.session.get('user_agent', None)
    }
    while True:
        response = requests.post("https://ywtb.cuit.edu.cn/api/base/login", json=dic, headers=headers, verify=False)



        first_cookie = list(response.cookies)[0]
        cookie_name = first_cookie.name
        cookie_value = first_cookie.value
        request.session['cookie_name'] = cookie_name
        request.session['cookie_value'] = cookie_value

        if cookie_name and cookie_value:
            headers['Cookie'] = f'{cookie_name}={cookie_value}'
        response2 = requests.get(
            f"https://ywtb.cuit.edu.cn/api/base/check_login?timestamp={str(int(time.time())) + '123'}",
            cookies=request.session.get('cookies_dict', None), verify=False, headers=headers)
        dic2 = response2.json()
        data = {
            'grant_type': 'password',
            'username': '',
            'loginInfo': dic2['data'],
            'password': encrypt
        }

        headers2 = {
            'Host': 'ywtb.cuit.edu.cn',
            'Authorization': 'Bearer',
            'Connection': 'keep-alive',
            'Content-Length': '870',
            'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': request.session.get('user_agent', None),
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://ywtb.cuit.edu.cn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://ywtb.cuit.edu.cn/file/apps/cxek/index.html?code=123&state=GZState',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
        }
        cookie_name = request.session.get('cookie_name')
        cookie_value = request.session.get('cookie_value')
        if cookie_name and cookie_value:
            headers2['Cookie'] = f'{cookie_name}={cookie_value}'
        response3 = requests.post(
            'https://ywtb.cuit.edu.cn/third_api/cxek/PhoneApi/api/Account/Login?code=123&state=GZState',
            headers=headers2, data=data, verify=False)
        dic3 = response3.json()
        request.session['access_token'] = dic3['access_token']
        dicd={}
        dicd['data'] = {'info': dic3['access_token'], 'username': username,
                        'user-agent': request.session['user_agent']}
        dicd['info'] = dic2
        if dic3:
            break
    if dic3:
        user_profile, created = UserProfile.objects.get_or_create(username=request.session.get('username', None))

        if created:
            return JsonResponse({"status": "ok", "message": "登录成功", 'data': dicd})
        else:
            return JsonResponse({"status": "ok", "message": "登录成功", 'data': dicd})
    else:
        return JsonResponse({"status": "error", "message": "登录失败"})


@require_POST
def sc_data(request):
    date = json.loads(request.body)

    page = date.get('page')
    data = date.get('data')
    access_token = data['info']
    username = data['username']
    user_agent = data['user-agent']
    headers3 = {
        'Authorization': f"Bearer {access_token}",
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://ywtb.cuit.edu.cn/file/apps/cxek/index.html?code=123&state=GZState',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }

    response4 = requests.get(
        f'https://ywtb.cuit.edu.cn/third_api/cxek/PhoneApi/api/Activity/GetStuActActivityList?pageIndex={page}&activityType=&activityName=&activityStatus=&moduleCode=',
        headers=headers3,verify=False)
    dic4 = response4.json()

    return JsonResponse({'info': dic4})


@require_POST
def choose(request):
    date = json.loads(request.body)
    id = date.get('id')
    data = date.get('data')
    access_token = data['info']
    username = data['username']
    user_agent = data['user-agent']
    headers4 = {
        'Authorization': f"Bearer {access_token}",
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://ywtb.cuit.edu.cn/file/apps/cxek/index.html?code=123&state=GZState',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }

    timestamp = time.time()
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    year = dt_object.year
    month = dt_object.month
    day = dt_object.day
    hour = dt_object.hour
    minute = dt_object.minute
    second = dt_object.second

    data = f'ApplyInfo%5BNoApplyReaon%5D=&ApplyInfo%5BId%5D=00000000-0000-0000-0000-000000000000&ApplyInfo%5BActivityId%5D={id}&ApplyInfo%5BStudentId%5D={username}&ApplyInfo%5BUserType%5D=S&ApplyInfo%5BActivityRoleId%5D=00000000-0000-0000-0000-000000000000&ApplyInfo%5BInsertUserId%5D={username}&ApplyInfo%5BInsertTime%5D={year}%2F{month}%2F{day}%20{hour}%3A{minute}%3A{second}&ApplyInfo%5BAttendanceStatus%5D=&ApplyInfo%5BLeaveReason%5D=&ApplyInfo%5BLeaveStatus%5D=&ApplyInfo%5BLeaveThing%5D=&ApplyInfo%5BLeaveDate%5D=&ApplyInfo%5BLeaveMen%5D=&ApplyInfo%5BSignInTime%5D=&ApplyInfo%5BSignOutTime%5D=&ApplyInfo%5BRemoveBlack%5D=&ApplyInfo%5BDataSoure%5D=&ApplyInfo%5BBigState%5D=&ApplyInfo%5BStatusName%5D=&ApplyInfo%5BIsEdit%5D=1&ApplyInfo%5BNextStepMsg%5D=&ApplyInfo%5BFlowStatus%5D=0&ApplyInfo%5BCollegeAsName%5D=%E5%AD%A6%E9%99%A2'
    response5 = requests.post(f'https://ywtb.cuit.edu.cn/third_api/cxek/PhoneApi/api/Activity/SaveActActivityApply',
                              headers=headers4, data=data, verify=False)

    return JsonResponse({'return_data': response5.text, 'data': data}, safe=False)


@require_POST
def register_data(request):
    date = json.loads(request.body)
    page = date.get('data')
    data = date.get('data')
    access_token = data['info']
    username = data['username']
    user_agent = data['user-agent']
    headers5 = {
        'Authorization': f"Bearer {access_token}",
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://ywtb.cuit.edu.cn/file/apps/cxek/index.html?',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }
    cookie_name = request.session.get('cookie_name')
    cookie_value = request.session.get('cookie_value')
    if cookie_name and cookie_value:
        headers5['Cookie'] = f'{cookie_name}={cookie_value}'
    response6 = requests.get(
        f'https://ywtb.cuit.edu.cn/third_api/cxek/PhoneApi/api/Activity/GetStuAllActApplyList?activityType=&activityName=&qdType=&qtType=&pageIndex={page}',
        headers=headers5,verify=False)
    dic5 = response6.json()
    return JsonResponse({'info': dic5})


@require_POST
def register(request):
    date = json.loads(request.body)
    id = date.get('id')
    data = date.get('data')
    access_token = data['info']
    username = data['username']
    user_agent = data['user-agent']
    headers6 = {
        'Authorization': f"Bearer {access_token}",
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://ywtb.cuit.edu.cn/file/apps/cxek/index.html?code=123&state=GZState',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }

    tm_1 = str(int(time.time()))
    tm_2 = str(int(time.time()) + random.randint(20, 100))
    response7 = requests.get(
        f'https://ywtb.cuit.edu.cn/third_api/cxek/PhoneApi/api/Activity/StuSaveQrCode?content={id}|{tm_1}|QD',
        headers=headers6, verify=False)
    time.sleep(1)
    response8 = requests.get(
        f'https://ywtb.cuit.edu.cn/third_api/cxek/PhoneApi/api/Activity/StuSaveQrCode?content={id}|{tm_2}|QT',
        headers=headers6, verify=False)
    if response7.json().get('errcode') == 0 and response8.json().get('errcode') == 0:
        return JsonResponse({'states': 'ok', 'msg': "签到成功"})
    else:
        return JsonResponse({'msg1': response7.text, 'msg2': response8.text})


@require_POST
def basin_data(request):
    date = json.loads(request.body)
    data = date.get('data')
    print(data)
    access_token = data['info']
    username = data['username']
    user_agent = data['user-agent']
    headers7 = {
        'Authorization': f"Bearer {access_token}",
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://ywtb.cuit.edu.cn/file/apps/cxek/index.html?code=123&state=GZState',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }

    response9 = requests.get('https://ywtb.cuit.edu.cn/third_api/cxek/PhoneApi/api/Student/GetStudentInfo',
                             verify=False, headers=headers7)
    return JsonResponse({'info': response9.json()})


@require_POST
def img(request):
    if request.method == 'POST' and request.FILES['file']:
        image = request.FILES['file']
        file_path = fr'C:\Users\Administrator\Desktop\Django\static\media\avatars\{request.session.get("username", None)}'
        if os.path.exists(file_path):
            os.remove(file_path)
        profile = UserProfile.objects.get(username=request.session.get("username", None))
        profile.img_path = request.FILES['file']
        profile.save()

        return JsonResponse({'image_url': 'ok', 'username': request.session.get("username", None)})
    else:
        return JsonResponse({'error': "error"})


@require_POST
def get_image(request):
    user_profile = UserProfile.objects.get(username=request.session.get("username", None))

    image_name = str(user_profile.img_path)
    image_path = os.path.join(settings.MEDIA_ROOT, image_name)
    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        response = HttpResponse(image_data, content_type='image/jpeg')
        return response
    except:
        with open(r'C:\Users\Administrator\Desktop\R-C.gif', 'rb') as image_file:
            image_data = image_file.read()
        response = HttpResponse(image_data, content_type='image/jpeg')
        return response



from django.http import JsonResponse
from django.views.decorators.http import require_POST
from backend.models import UserProfile
import json
import requests
import datetime
import time
import random
from django.conf import settings
from django.http import HttpResponse


import os


@require_POST
def login(request):
    data = json.loads(request.body)

    username = data['username']
    password = data['password']
    encrypt = data['encrypt']

    request.session['username'] = username
    request.session['user_agent'] = data['user_agent']['User-Agent']

    dic = {
        "username": username,
        "password": password,
        "validateCode": "",
        "loginType": "",
        "redirectUrl": ""
    }
    headers = {
        'User-Agent': request.session.get('user_agent', None)
    }
    while True:
        response = requests.post("https://ywtb.cuit.edu.cn/api/base/login", json=dic, headers=headers, verify=False)



        first_cookie = list(response.cookies)[0]
        cookie_name = first_cookie.name
        cookie_value = first_cookie.value
        request.session['cookie_name'] = cookie_name
        request.session['cookie_value'] = cookie_value

        if cookie_name and cookie_value:
            headers['Cookie'] = f'{cookie_name}={cookie_value}'
        response2 = requests.get(
            f"https://ywtb.cuit.edu.cn/api/base/check_login?timestamp={str(int(time.time())) + '123'}",
            cookies=request.session.get('cookies_dict', None), verify=False, headers=headers)
        dic2 = response2.json()
        data = {
            'grant_type': 'password',
            'username': '',
            'loginInfo': dic2['data'],
            'password': encrypt
        }

        headers2 = {
            'Host': 'ywtb.cuit.edu.cn',
            'Authorization': 'Bearer',
            'Connection': 'keep-alive',
            'Content-Length': '870',
            'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': request.session.get('user_agent', None),
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://ywtb.cuit.edu.cn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://ywtb.cuit.edu.cn/file/apps/cxek/index.html?code=123&state=GZState',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
        }
        cookie_name = request.session.get('cookie_name')
        cookie_value = request.session.get('cookie_value')
        if cookie_name and cookie_value:
            headers2['Cookie'] = f'{cookie_name}={cookie_value}'
        response3 = requests.post(
            'https://ywtb.cuit.edu.cn/third_api/cxek/PhoneApi/api/Account/Login?code=123&state=GZState',
            headers=headers2, data=data, verify=False)
        dic3 = response3.json()
        request.session['access_token'] = dic3['access_token']
        dicd={}
        dicd['data'] = {'info': dic3['access_token'], 'username': username,
                        'user-agent': request.session['user_agent']}
        dicd['info'] = dic2
        if dic3:
            break
    if dic3:
        user_profile, created = UserProfile.objects.get_or_create(username=request.session.get('username', None))

        if created:
            return JsonResponse({"status": "ok", "message": "登录成功", 'data': dicd})
        else:
            return JsonResponse({"status": "ok", "message": "登录成功", 'data': dicd})
    else:
        return JsonResponse({"status": "error", "message": "登录失败"})


@require_POST
def sc_data(request):
    date = json.loads(request.body)

    page = date.get('page')
    data = date.get('data')
    access_token = data['info']
    username = data['username']
    user_agent = data['user-agent']
    headers3 = {
        'Authorization': f"Bearer {access_token}",
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://ywtb.cuit.edu.cn/file/apps/cxek/index.html?code=123&state=GZState',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }

    response4 = requests.get(
        f'https://ywtb.cuit.edu.cn/third_api/cxek/PhoneApi/api/Activity/GetStuActActivityList?pageIndex={page}&activityType=&activityName=&activityStatus=&moduleCode=',
        headers=headers3,verify=False)
    dic4 = response4.json()

    return JsonResponse({'info': dic4})


@require_POST
def choose(request):
    date = json.loads(request.body)
    id = date.get('id')
    data = date.get('data')
    access_token = data['info']
    username = data['username']
    user_agent = data['user-agent']
    headers4 = {
        'Authorization': f"Bearer {access_token}",
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://ywtb.cuit.edu.cn/file/apps/cxek/index.html?code=123&state=GZState',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }

    timestamp = time.time()
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    year = dt_object.year
    month = dt_object.month
    day = dt_object.day
    hour = dt_object.hour
    minute = dt_object.minute
    second = dt_object.second

    data = f'ApplyInfo%5BNoApplyReaon%5D=&ApplyInfo%5BId%5D=00000000-0000-0000-0000-000000000000&ApplyInfo%5BActivityId%5D={id}&ApplyInfo%5BStudentId%5D={username}&ApplyInfo%5BUserType%5D=S&ApplyInfo%5BActivityRoleId%5D=00000000-0000-0000-0000-000000000000&ApplyInfo%5BInsertUserId%5D={username}&ApplyInfo%5BInsertTime%5D={year}%2F{month}%2F{day}%20{hour}%3A{minute}%3A{second}&ApplyInfo%5BAttendanceStatus%5D=&ApplyInfo%5BLeaveReason%5D=&ApplyInfo%5BLeaveStatus%5D=&ApplyInfo%5BLeaveThing%5D=&ApplyInfo%5BLeaveDate%5D=&ApplyInfo%5BLeaveMen%5D=&ApplyInfo%5BSignInTime%5D=&ApplyInfo%5BSignOutTime%5D=&ApplyInfo%5BRemoveBlack%5D=&ApplyInfo%5BDataSoure%5D=&ApplyInfo%5BBigState%5D=&ApplyInfo%5BStatusName%5D=&ApplyInfo%5BIsEdit%5D=1&ApplyInfo%5BNextStepMsg%5D=&ApplyInfo%5BFlowStatus%5D=0&ApplyInfo%5BCollegeAsName%5D=%E5%AD%A6%E9%99%A2'
    response5 = requests.post(f'https://ywtb.cuit.edu.cn/third_api/cxek/PhoneApi/api/Activity/SaveActActivityApply',
                              headers=headers4, data=data, verify=False)

    return JsonResponse({'return_data': response5.text, 'data': data}, safe=False)


@require_POST
def register_data(request):
    date = json.loads(request.body)
    page = date.get('data')
    data = date.get('data')
    access_token = data['info']
    username = data['username']
    user_agent = data['user-agent']
    headers5 = {
        'Authorization': f"Bearer {access_token}",
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://ywtb.cuit.edu.cn/file/apps/cxek/index.html?',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }
    cookie_name = request.session.get('cookie_name')
    cookie_value = request.session.get('cookie_value')
    if cookie_name and cookie_value:
        headers5['Cookie'] = f'{cookie_name}={cookie_value}'
    response6 = requests.get(
        f'https://ywtb.cuit.edu.cn/third_api/cxek/PhoneApi/api/Activity/GetStuAllActApplyList?activityType=&activityName=&qdType=&qtType=&pageIndex={page}',
        headers=headers5,verify=False)
    dic5 = response6.json()
    return JsonResponse({'info': dic5})


@require_POST
def register(request):
    date = json.loads(request.body)
    id = date.get('id')
    print(date)
    data = date.get('data')
    access_token = data['info']
    username = data['username']
    user_agent = data['user-agent']
    headers6 = {
        'Authorization': f"Bearer {access_token}",
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://ywtb.cuit.edu.cn/file/apps/cxek/index.html?code=123&state=GZState',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }

    tm_1 = str(int(time.time()))
    tm_2 = str(int(time.time()) + random.randint(20, 100))
    response7 = requests.get(
        f'https://ywtb.cuit.edu.cn/third_api/cxek/PhoneApi/api/Activity/StuSaveQrCode?content={id}|{tm_1}|QD',
        headers=headers6, verify=False)
    time.sleep(1)
    response8 = requests.get(
        f'https://ywtb.cuit.edu.cn/third_api/cxek/PhoneApi/api/Activity/StuSaveQrCode?content={id}|{tm_2}|QT',
        headers=headers6, verify=False)
    if response7.json().get('errcode') == 0 and response8.json().get('errcode') == 0:
        return JsonResponse({'states': 'ok', 'msg': "签到成功"})
    else:
        return JsonResponse({'msg1': response7.text, 'msg2': response8.text})


@require_POST
def basin_data(request):
    date = json.loads(request.body)
    data = date.get('data')
    print(data)
    access_token = data['info']
    username = data['username']
    user_agent = data['user-agent']
    headers7 = {
        'Authorization': f"Bearer {access_token}",
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://ywtb.cuit.edu.cn/file/apps/cxek/index.html?code=123&state=GZState',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }

    response9 = requests.get('https://ywtb.cuit.edu.cn/third_api/cxek/PhoneApi/api/Student/GetStudentInfo',
                             verify=False, headers=headers7)
    return JsonResponse({'info': response9.json()})


@require_POST
def img(request):
    if request.method == 'POST' and request.FILES['file']:
        image = request.FILES['file']
        file_path = fr'C:\Users\Administrator\Desktop\Django\static\media\avatars\{request.session.get("username", None)}'
        if os.path.exists(file_path):
            os.remove(file_path)
        profile = UserProfile.objects.get(username=request.session.get("username", None))
        profile.img_path = request.FILES['file']
        profile.save()

        return JsonResponse({'image_url': 'ok', 'username': request.session.get("username", None)})
    else:
        return JsonResponse({'error': "error"})


@require_POST
def get_image(request):
    user_profile = UserProfile.objects.get(username=request.session.get("username", None))

    image_name = str(user_profile.img_path)
    image_path = os.path.join(settings.MEDIA_ROOT, image_name)
    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        response = HttpResponse(image_data, content_type='image/jpeg')
        return response
    except:
        with open(r'C:\Users\Administrator\Desktop\R-C.gif', 'rb') as image_file:
            image_data = image_file.read()
        response = HttpResponse(image_data, content_type='image/jpeg')
        return response



