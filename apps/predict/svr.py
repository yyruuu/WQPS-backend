import numpy as np
from  sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error
from sklearn.externals import joblib


def train_and_predict(X_train, y_train, X_test):
    try:
        svr_model = joblib.load("svr_model.m")
        print("训练好的", svr_model)
    except:
        svr_model = SVR(kernel='rbf')
        svr_model.fit(X_train, y_train)
        joblib.dump(svr_model, "svr_model.m")

    predict = svr_model.predict(X_test)
    return predict



