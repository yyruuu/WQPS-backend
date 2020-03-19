from django.shortcuts import render
import json
from . import models
from django.http import JsonResponse
# Create your views here.


def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        email = data['email']
        new_user = models.User()
        new_user.username = username
        new_user.password = password
        new_user.email = email
        new_user.save()
        res = {
            'err': 0,
            'info': "注册成功！",
            'data': {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email
            }
        }
        return JsonResponse(res)


def login(request):
    # 用户登录
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        try:
            user = models.User.objects.get(username=username)
        except:
            return JsonResponse({"err": 1, "info": "用户不存在"})

        if user.username != username or user.password != password:
            return JsonResponse({"err": 1, "info": "用户名或密码错误"})
        else:
            res = {
                "err": 0,
                "info": "登录成功！",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }
            request.session["userId"] = user.id
            return JsonResponse(res)

    # 检查用户是否登录
    elif request.method == 'GET':
        session_id = request.session['userId']
        if session_id:
            try:
                user = models.User.objects.get(id=session_id)
            except:
                return JsonResponse({"err": 1, "info": "用户不存在"})

            if user:
                res = {
                    "err": 0,
                    "info": "已登录！",
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    }
                }
                return JsonResponse(res)


def sign_out(request):
    request.session.clear()
    res = {
        "err": 0,
        "info": "注销成功！",
        "data": None
    }
    return JsonResponse(res)




