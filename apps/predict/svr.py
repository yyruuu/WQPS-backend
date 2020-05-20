import numpy as np
from  sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error
from sklearn.externals import joblib


def train(train_X, train_y, test_X, param, n_weeks):
    string = "svr_"+param+str(n_weeks)+'.m'
    try:
        svr_model = joblib.load(string)
        print("训练好的", svr_model)
    except:
        svr_model = SVR(kernel='rbf', C=1.0, degree=3)
        svr_model.fit(train_X, train_y)
        joblib.dump(svr_model, string)

    return svr_model



