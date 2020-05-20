# from .. import water
# from .. import weather
# from apps.water import models as water_models
# from apps.weather import models as weather_models
from water.models import WaterData
from weather.models import WeatherData

import numpy as np
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from math import sqrt
from numpy import concatenate
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from pandas import DataFrame
from pandas import concat

# 从数据库中获取数据
def get_data():
    water_db = WaterData.objects.all()
    time = water_db.values('time')
    PH = water_db.values('PH')
    DO = water_db.values('DO')
    CODMn = water_db.values('CODMn')
    NH3_N = water_db.values('NH3_N')

    weather_db = WeatherData.objects.all()
    T = weather_db.values('T')
    Po = weather_db.values('Po')
    P = weather_db.values('P')
    U = weather_db.values('U')
    Ff = weather_db.values('Ff')
    VV = weather_db.values('VV')
    Td = weather_db.values('Td')
    RRR = weather_db.values('RRR')

    length = len(time)
    data = []
    for i in range(0, length):
        rcd = [time[i]['time'], PH[i]['PH'], DO[i]['DO'], CODMn[i]['CODMn'], NH3_N[i]['NH3_N'],
               T[i]['T'], Po[i]['Po'], P[i]['P'], U[i]['U'], Ff[i]['Ff'], VV[i]['VV'], Td[i]['Td'],
               RRR[i]['RRR']]
        data.append(rcd)
    data = np.array(data)
    return data


# 将时许数据转换为监督问题
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg





# def get_X_y(data, param):
#     X = data[:, 1:]
#     if param == 'PH':
#         y = data[:, 1]
#     elif param == 'DO':
#         print("ahahh", param)
#         y = data[:, 2]
#     elif param == 'CODMn':
#         y = data[:, 3]
#     elif param == 'NH3_N':
#         y = data[:, 4]
#     return X, y


def standard(values):
    # std = StandardScaler()
    # scaler = std.fit(X)
    # X_std = scaler.transform(X)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)
    return scaler, scaled


def train_test_split(X, y, split_index, param, n_weeks, n_features):
    # X_train = X[:split_index, :]
    # X_test = X[split_index:, :]
    # y_train = y[:split_index]
    # y_test = y[split_index:]

    # 前三年半的数据来训练
    n_train_weeks = split_index
    # train = values[:n_train_weeks, :]
    # test = values[n_train_weeks:, :]
    # split into input and outputs
    n_obs = n_weeks * n_features
    if param == "PH":
        y_index = 0
    elif param == "DO":
        y_index = 1
    elif param == "CODMn":
        y_index = 2
    elif param == "NH3_N":
        y_index = 3
    # 有60=(5*12)列数据，取前48=(4*12) 列作为X，倒数第12列=(第49列)作为Y
    train_X, train_y = X[:n_train_weeks, :], y[:n_train_weeks, y_index]
    test_X, test_y = X[n_train_weeks:, :], y[n_train_weeks:, y_index]
    return train_X, test_X, train_y, test_y


# 对于LSTM，需要将数据转换为3D输入
def trans_3d(train_X, test_X, n_weeks, n_features):
    # 将数据转换为3D输入，timesteps=4，4条数据预测1条 [samples, timesteps, features]
    train_X = train_X.reshape((train_X.shape[0], n_weeks, n_features))
    test_X = test_X.reshape((test_X.shape[0], n_weeks, n_features))
    return train_X, test_X


# predit -> yhat, origin_data -> test_X
def inverse_trans(predict, origin_data, scaler, n_weeks, n_features):
    # 将预测列据和后11列数据拼接，因后续逆缩放时，数据形状要符合 n行*12列 的要求
    inv_predict = np.column_stack((predict, origin_data[:, -11:]))
    # 对拼接好的数据进行逆缩放
    inv_predict = scaler.inverse_transform(inv_predict)
    inv_predict = inv_predict[:, 0]
    return inv_predict


# 获取最后四周的数据
def get_last_predict(test_X, model, sel_model, n_weeks, n_features):
    # last = test_X[-4:, :]
    if sel_model == "LSTM":
        test_X = test_X.reshape((test_X.shape[0], n_weeks, n_features))
    last = test_X[-n_weeks:, :]
    last_predict = model.predict(last)
    # inverse
    # if sel_model == "LSTM":
    #     last = last.reshape((last.shape[0], n_weeks * n_features))
    # else:
    #     last_predict.reshape(-1, 1)
    # last_predict = np.column_stack((last_predict, last[:, -11:]))
    # last_predict = scaler.inverse_transform(last_predict)
    # last_predict = last_predict[:, 0]

    return last_predict