import json

from django.http import JsonResponse, HttpResponse

import random
# from utils import zhenzismsclient
from django.views.decorators.csrf import csrf_exempt

from user.models import user
from Questionnaire.views import *

# defaultId = 0

@csrf_exempt
def login(request):
    if request.method == 'POST':
        result = json.loads(request.body)
        newUsername = result.get("username");
        newPassword = result.get("password");
        users = user.objects.filter(username = newUsername)
        if len(users)==0:
            return JsonResponse({
                "status":400,
                "result":"请注册",
            });
        if users[0].password != newPassword:
            return JsonResponse({
                "status": 300,
                "result": "密码错误",
            });
        else:
            request.session.set_expiry(0)
            request.session['id'] = users[0].id
            print(users[0].id)
            request.session['kind'] = "user"
            return JsonResponse({
                "status": 200,
                "result": "登录成功",
                "uid":users[0].id,
                "session":request.session.get('id'),
                "session2":request.session.get('kind'),
            })

def register(request):
    if request.method == 'POST':
        result = json.loads(request.body.decode())
        newUsername = result.get("username");
        newPassword = result.get("password");
        newEmail = result.get("Email");
        newPhone = result.get("phone");
        newSFID = result.get("sfID");
        if len(user.objects.filter(username=newUsername))==0 and \
                len(user.objects.filter(email = newEmail))==0 and len(user.objects.filter(phone=newPhone))==0:
            newUser = user();
            newUser.username = newUsername;
            newUser.password = newPassword;
            newUser.sfID = newSFID;
            newUser.email = newEmail;
            newUser.phone = newPhone
            user.save(newUser);
            return JsonResponse({
                "status": 200,
                "result": "注册成功",
            })
        else:
            return JsonResponse({
                "status": 400,
                "result": "用户已存在",
            })



def getMyInfo(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        try:
            authorId = req.get('authorId')
            print(authorId)
        except Exception:
            return JsonResponse({'status':400,'result':"用户未登录"})
        else:
            myuser = user.objects.get(id=authorId)
            return JsonResponse({
                "status":200,
                "result":"请求成功",
                "email":myuser.email,
                "username":myuser.username,
                "phone":myuser.phone,
                "uid":myuser.id,
            })


def logout(request):
    if request.method == 'GET':
        return JsonResponse({
            "status":200,
            "result":"登出成功"
        })
    else:
        return JsonResponse({
            "status": 400,
            "result": "请求方式错误"
        })

# 找回密码
def retrievePassword(request):
    if request.method == 'POST':
        params = json.loads(request.body.decode())
        username = params.get("username")
        phone = params.get("phone")
        email = params.get("email")
        try:
            user1 = user.objects.get(username=username,
                                     phone=phone,
                                     email=email)
        except Exception:
            return JsonResponse({
                "status":400,
                "result":"输入信息不正确"
            })
        return JsonResponse({
            "status":200,
            "result":"找回密码成功",
            "password":user1.password
        })

# 修改密码
def changePassword(request):
    if request.method == 'POST':
        params = json.loads(request.body.decode())
        username = params.get("username")
        password = params.get("password")
        user1 = user.objects.get(username=username)
        user1.password = password
        user1.save()
        return JsonResponse({
            "status":200,
            "result":"修改密码成功"
        })