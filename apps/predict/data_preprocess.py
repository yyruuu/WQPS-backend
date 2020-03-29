# from .. import water
# from .. import weather
# from apps.water import models as water_models
# from apps.weather import models as weather_models
from water.models import WaterData
from weather.models import WeatherData

import numpy as np
from sklearn.preprocessing import StandardScaler

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


def get_X_y(data, param):
    X = data[:, 1:]
    if param == 'PH':
        y = data[:, 1]
    elif param == 'DO':
        print("ahahh", param)
        y = data[:, 2]
    elif param == 'CODMn':
        y = data[:, 3]
    elif param == 'NH3_N':
        y = data[:, 4]
    return X, y


def standard(X):
    std = StandardScaler()
    scaler = std.fit(X)
    X_std = scaler.transform(X)
    return X_std


def train_test_split(X, y, split_index):
    X_train = X[:split_index, :]
    X_test = X[split_index:, :]
    y_train = y[:split_index]
    y_test = y[split_index:]
    return X_train, X_test, y_train, y_test