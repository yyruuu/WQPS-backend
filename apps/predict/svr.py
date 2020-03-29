import numpy as np
from  sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error


def train_and_predict(X_train, y_train, X_test):
    svr_model = SVR(kernel='rbf')
    svr_model.fit(X_train, y_train)
    predict = svr_model.predict(X_test)
    return predict



