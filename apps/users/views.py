from django.shortcuts import render
# import json
try:
    import json
except ImportError:
    import simplejson as json

from . import models
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.core import serializers

# Create your views here.


# 注册
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


# 返回所有用户
def get_user_datas(request):
    if request.method == 'GET':
        # 从body中获取offset和num
        num = request.GET.get('num')
        offset = request.GET.get('offset')
        user_data_list = models.User.objects.all()
        paginator = Paginator(user_data_list, num)
        page_obj = paginator.get_page(offset)
        if page_obj:
            res = {
                "err": 0,
                "info": "用户分页数据",
                "data": {
                    "results":  serializers.serialize("json", page_obj.object_list),
                    "total_records": paginator.count,
                    "total_pages": paginator.num_pages,
                    "page": page_obj.number,
                    "has_next": page_obj.has_next(),
                    "has_prev": page_obj.has_previous()
                }
            }
        else:
            res = {
                "err": 1,
                "info": "无数据",
                "data": None
            }
        return HttpResponse(JsonResponse(res), content_type="application/json")


# 返回一位用户的数据
def get_a_data(request, user_id):
    if request.method == 'GET':
        data = models.User.objects.get(pk=user_id)
        if data:
            res = {
                "err": 0,
                "info": "获取到一条数据",
                "data": {
                    "id": data.pk,
                    "username": data.username,
                    "password": data.password,
                    "email": data.username,
                    "time": data.createdAt
                }
            }
        else:
            res = {
                "err": 1,
                "info": "没有该id的数据",
                "data": None
            }
        return JsonResponse(res)


# 修改用户数据
def edit_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data_id = data["id"]
        username = data['username']
        email = data['email']
        password = data['password']
        user = models.User.objects.get(pk=data_id)
        if user:
            user.username = username
            user.email = email
            user.password = password
            user.save()
            res = {
                "err": 0,
                "info": "修改成功"
            }
        else:
            res = {
                "err": 1,
                "info": "未找到该条数据"
            }
        return JsonResponse(res)


# 删除用户数据
def delete_data(request, data_id):
    if request.method == "GET":
        user = models.User.objects.get(pk=data_id)
        if user:
            user.delete()
            res = {
                "err": 0,
                "info": "删除成功"
            }
        else:
            res = {
                "err": 1,
                "info": "无该条记录"
            }
        return JsonResponse(res)
