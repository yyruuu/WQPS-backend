from django.shortcuts import render
import json
from django.core.paginator import Paginator
from . import models
from django.http import JsonResponse, HttpResponse
from django.core import serializers

# Create your views here.


# 返回所有水质数据from django.core.serializers import serialize
def get_water_data(request):
    if request.method == 'GET':
        # 从body中获取offset和num
        num = request.GET.get('num')
        offset = request.GET.get('offset')
        water_data_list = models.WaterData.objects.all()
        paginator = Paginator(water_data_list, num)
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


# 返回一条水质数据
def get_a_data(request, data_id):
    if request.method == 'GET':
        # data_id = int(request.GET.get('id'))
        print("data id:", data_id)
        data = models.WaterData.objects.get(pk=data_id)
        if data:
            res = {
                "err": 0,
                "info": "获取到一条数据",
                "data": {
                    "id": data.pk,
                    "PH": data.PH,
                    "DO": data.DO,
                    "CODMn": data.CODMn,
                    "NH3_N": data.NH3_N,
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

# 修改水质数据
def edit_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data_id = data["id"]
        ph = data['PH']
        do = data['DO']
        codmn = data['CODMn']
        nh3n = data['NH3_N']
        time = data['time']
        water = models.WaterData.objects.get(pk=data_id)
        if water:
            water.PH = ph
            water.DO = do
            water.CODMn = codmn
            water.NH3_N = nh3n
            water.time = time
            water.save()
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


# 删除水质数据
def delete_data(request, data_id):
    if request.method == "GET":
        water = models.WaterData.objects.get(pk=data_id)
        if water:
            water.delete()
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
        ph = data['PH']
        do = data['DO']
        codmn = data['CODMn']
        nh3n = data['NH3_N']
        time = data['time']
        new_water = models.WaterData()
        new_water.PH = ph
        new_water.DO = do
        new_water.CODMn = codmn
        new_water.NH3_N = nh3n
        new_water.time = time
        new_water.save()
        res = {
            "err": 0,
            "info": "添加数据成功",
            "data": {
                "id": new_water.pk,
                "PH": new_water.PH,
                "DO": new_water.DO,
                "CODMn": new_water.CODMn,
                "NH3_N": new_water.NH3_N,
                "time": new_water.time
            }
        }
        return JsonResponse(res)

