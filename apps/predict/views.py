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
        # sel_model = "LSTM"
        # 后期可以选择需要预测未来多久的数据
        split_index = 183
        print("parammmm", sel_model)
        # 先加载数据
        data = data_preprocess.get_data()
        # 用一个月（4周）的数据预测一周数据，12个特征值
        n_weeks = 4
        n_features = 12
        # 构造一个4->1的监督学习型数据
        reframed = data_preprocess.series_to_supervised(data[:, 1:], n_weeks, 1, True)
        X = reframed.values[:, :n_weeks*n_features]
        y = reframed.values[:, n_weeks*n_features:]
        # 对X进行归一化
        scaler, X = data_preprocess.standard(X)
        # 将数据集分为训练集和测试集
        train_X, test_X, train_y, test_y = data_preprocess.train_test_split(X, y ,split_index, param, n_weeks, n_features)

        # 如果是LSTM，需要将数据转换为3D
        if sel_model == "LSTM":
            train_X, test_X = data_preprocess.trans_3d(train_X, test_X, n_weeks, n_features)
            model = lstm.train(train_X, train_y, test_X, test_y, param)
        elif sel_model == "SVR":
            model = svr.train(train_X, train_y, test_X, param)
        elif sel_model == "BP":
            model = bp.train(train_X, train_y, test_X, param)

        test_predict = model.predict(test_X)

        # 将归一化后的数据反转
        # 将数据格式化成 n行 * 48列
        # test_X = test_X.reshape((test_X.shape[0], n_weeks * n_features))
        # inv_test_predict = data_preprocess.inverse_trans(test_predict, test_X, scaler, n_weeks, n_features)
        # test_y = test_y.reshape((len(test_y), 1))
        # inv_test_y = data_preprocess.inverse_trans(test_y, test_X, scaler, n_weeks, n_features)
        # 使用最后四周的数据预测下四周
        last_predict = data_preprocess.get_last_predict(test_X, model, sel_model, n_weeks, n_features)
        if sel_model == "LSTM":
            test_predict = test_predict.reshape(1, -1)[0].tolist()
            last_predict = last_predict.reshape(1, -1)[0].tolist()

        # 最后四个真实值
        if param == "PH":
            true_last = data[:, 1][-4:]
        elif param == "DO":
            true_last = data[:, 2][-4:]
        elif param == "CODMn":
            true_last = data[:, 3][-4:]
        elif param == "NH3_N":
            true_last = data[:, 4][-4:]

        # 将预测结果返回
        time = data[:,0]
        time = time[split_index:]
        res = {
            "err": 0,
            "info": "返回训练结果",
            "data": {
                "time": list(time),
                "true": list(test_y),
                "predict": list(test_predict),
                "train_time": list(data[:,0][-4:]),
                "train_data": list(true_last),
                # "train_data": list(test_X[:, 2][-4:]),
                "last_predict": list(last_predict)
            }
        }
        return JsonResponse(res)
