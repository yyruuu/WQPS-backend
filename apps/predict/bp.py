from sklearn.neural_network.multilayer_perceptron import MLPRegressor
from sklearn.externals import joblib


def train(train_X, train_y, test_X, param, n_weeks):
    string = "bp_"+param+str(n_weeks)+'.m'
    try:
        bp_model = joblib.load(string)
        print("训练好的bp", bp_model)
    except:
        bp_model = MLPRegressor(hidden_layer_sizes=(18), max_iter=5000, learning_rate_init=0.1)
        bp_model.fit(train_X, train_y)
        joblib.dump(bp_model, string)
    return bp_model