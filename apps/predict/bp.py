from sklearn.neural_network.multilayer_perceptron import MLPRegressor
from sklearn.externals import joblib


def train_and_predict(X_train, y_train, X_test):
    try:
        bp_model = joblib.load("bp_model.m")
        print("训练好的bp", bp_model)
    except:
        bp_model = MLPRegressor(hidden_layer_sizes=(11), activation='logistic', max_iter=5000, learning_rate_init=0.01)
        bp_model.fit(X_train, y_train)
        joblib.dump(bp_model, "bp_model.m")
    predict = bp_model.predict(X_test)
    return predict