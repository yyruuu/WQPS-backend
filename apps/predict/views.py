from django.shortcuts import render
# import json
from django.core.paginator import Paginator
from . import models
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import itertools
from . import data_preprocess
from . import svr
from . import bp
from . import lstm
# import pandas as pd

def train(request):
    if request.method == 'GET':
        # 获取需要训练的参数
        param = request.GET.get('param')
        sel_model = request.GET.get('model')

        # 后期可以选择需要预测未来多久的数据
        split_index = 187
        print("parammmm", sel_model)
        # 先加载数据
        data = data_preprocess.get_data()
        # 获取总的X和y
        X_raw, y = data_preprocess.get_X_y(data, param)
        # 归一化
        X = data_preprocess.standard(X_raw)
        # 将数据集分为训练集和测试集
        X_train, X_test, y_train, y_test = data_preprocess.train_test_split(X, y, split_index)
        # 训练、预测
        if sel_model == "SVR":
            y_predict = svr.train_and_predict(X_train, y_train, X_test)
        elif sel_model == 'BP':
            y_predict = bp.train_and_predict(X_train, y_train, X_test)
        elif sel_model == 'LSTM':
            y_predict = lstm.train_and_predict(X_train, y_train, X_test)
            # y_predict = y_predict.flatten()
            y_predict = y_predict.reshape(1, -1)[0].tolist()
        # 将预测结果返回
        time = data[:,0]
        time = time[split_index:]
        res = {
            "err": 0,
            "info": "返回训练结果",
            "data": {
                "time": list(time),
                "true": list(y_test),
                "predict": list(y_predict),
                "train_time": list(data[:,0][:split_index]),
                "train_data": list(y_train)
            }
        }
        return JsonResponse(res)
