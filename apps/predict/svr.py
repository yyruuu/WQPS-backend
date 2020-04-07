import numpy as np
from  sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error
from sklearn.externals import joblib


def train(train_X, train_y, test_X, param):
    str = "svr_"+param+'.m'
    try:
        svr_model = joblib.load(str)
        print("训练好的", svr_model)
    except:
        svr_model = SVR(kernel='rbf')
        svr_model.fit(train_X, train_y)
        joblib.dump(svr_model, str)

    return svr_model



