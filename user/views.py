import json

from django.http import JsonResponse, HttpResponse
# from utils import zhenzismsclient
import random
from utils import zhenzismsclient

# Create your views here.
from user.models import user


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
                "status": 400,
                "result": "密码错误",
            });
        else:
            request.session['id'] = users[0].id
            request.session['kind'] = "user"
            return JsonResponse({
                "status": 200,
                "result": "登录成功",
            })
def register(request):
    if request.method == 'POST':
        result = json.loads(request.body)
        newUsername = result.get("username");
        newPassword = result.get("password");
        newEmail = result.get("Email");
        newPhone = result.get("phone");
        newSFID = result.get("sfID");
        if len(user.objects.filter(username=newUsername))==0:
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

def getCode(request):
    if request.method == 'POST':
        ggg = json.loads(request.body)
        number = ggg.get("number");
        code = ''
        for num in range(1, 5):
            code = code + str(random.randint(0, 9))
        client = zhenzismsclient.ZhenziSmsClient('https://sms_developer.zhenzikj.com', "108980","ee6d9744-1128-4d50-abb8-b227b793f196" )
        params = {};
        params['number'] =number;
        params['templateId'] = '5130';
        params['templateParams'] = [code, '15分钟'];
        result = client.send(params)
        # return HttpResponse(json.dumps(result),content_type="application/json")
        # return JsonResponse(result,safe=False,json_dumps_params={'ensure_ascii':False})
        if(result[8]=='0'):
            return JsonResponse({
                "status":200,
                "result":"发送成功"
            })
        else:
            return JsonResponse({
                "status": 400,
                "result": "发送失败"
            })

def getMyInfo(request):
    if request.method == 'GET':
        if request.session.get('kind') == 'user':
            myuser = user.objects.get(id=request.session.get('id'))
            return JsonResponse({
                "status":200,
                "result":"请求成功",
                "email":myuser.email,
                "username":myuser.username,
                "phone":myuser.phone,
                "sdID":myuser.sfID
            })