from django.shortcuts import render
import json
from django.core.paginator import Paginator
from . import models
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import itertools

# Create your views here.


# 返回所有气象数据
def get_weather_data(request):
    if request.method == 'GET':
        # 从body中获取offset和num
        num = request.GET.get('num')
        offset = request.GET.get('offset')
        weather_data_list = models.WeatherData.objects.all()
        paginator = Paginator(weather_data_list, num)
        page_obj = paginator.get_page(offset)
        if page_obj:
            res = {
                "err": 0,
                "info": "分页数据",
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


# 返回一条气象数据
def get_a_data(request, data_id):
    if request.method == 'GET':
        # data_id = int(request.GET.get('id'))
        print("data id:", data_id)
        data = models.WeatherData.objects.get(pk=data_id)
        if data:
            res = {
                "err": 0,
                "info": "获取到一条数据",
                "data": {
                    "id": data.pk,
                    "T": data.T,
                    "Po": data.Po,
                    "P": data.P,
                    "U": data.U,
                    "Ff": data.Ff,
                    "VV": data.VV,
                    "Td": data.Td,
                    "RRR": data.RRR,
                    "time": data.time
                }
            }
        else:
            res = {
                "err": 1,
                "info": "没有该id的数据",
                "data": None
            }
        return JsonResponse(res)


# 修改气象数据
def edit_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data_id = data["id"]
        T = data['T']
        Po = data['Po']
        P = data['P']
        U = data['U']
        Ff = data['Ff']
        VV = data['VV']
        Td = data['Td']
        RRR = data['RRR']
        time = data['time']
        weather = models.WeatherData.objects.get(pk=data_id)
        if weather:
            weather.T = T
            weather.Po = Po
            weather.P = P
            weather.U = U
            weather.Ff = Ff
            weather.VV = VV
            weather.Td = Td
            weather.RRR = RRR
            weather.time = time
            weather.save()
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


# 删除气象数据
def delete_data(request, data_id):
    if request.method == "GET":
        weather = models.WeatherData.objects.get(pk=data_id)
        if weather:
            weather.delete()
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


# 新增数据
def add_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("add:", data)
        T = data['T']
        Po = data['Po']
        P = data['P']
        U = data['U']
        Ff = data['Ff']
        VV = data['VV']
        Td = data['Td']
        RRR = data['RRR']
        time = data['time']

        new_weather = models.WeatherData()
        new_weather.T = T
        new_weather.Po = Po
        new_weather.P = P
        new_weather.U = U
        new_weather.Ff = Ff
        new_weather.VV = VV
        new_weather.Td = Td
        new_weather.RRR = RRR
        new_weather.time = time
        new_weather.save()
        res = {
            "err": 0,
            "info": "添加数据成功",
            "data": {
                "id": new_weather.pk,
                "T": new_weather.T,
                "Po": new_weather.Po,
                "P": new_weather.P,
                "U": new_weather.U,
                "Ff": new_weather.Ff,
                "VV": new_weather.VV,
                "Td": new_weather.Td,
                "RRR": new_weather.RRR,
                "time": new_weather.time
            }
        }
        return JsonResponse(res)


# 绘制数据趋势
def plot_data(request):
    if request.method == 'GET':
        param = request.GET.get('param')
        interval = request.GET.get('interval')
        print("param:::", param)
        print("interval:::", interval)
        if interval == "all":
            data = models.WeatherData.objects.all()
        else:
            data = models.WeatherData.objects.filter(time__year=interval)
        # print(list(data.values_list("PH")))
        # out = list(itertools.chain(*tuple))
        # print(list(itertools.chain(*data.values_list("PH"))))
        res_data = []
        res_data.append(list(itertools.chain(*data.values_list("time"))))
        res_data.append(list(itertools.chain(*data.values_list(param))))
        res = {
            "err": 0,
            "info": "绘图数据",
            "data": res_data
        }
        return JsonResponse(res)