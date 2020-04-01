from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import load_model

def train_and_predict(X_train, y_train, X_test):
    X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))
    try:
        model = load_model('lstm_model.h5')
        print("训练好的LSTM", model)
    except:
        X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
        model = Sequential()
        # 隐藏层有100个神经元
        model.add(LSTM(100, input_shape=(X_train.shape[1], X_train.shape[2]),
                       return_sequences=True))
        model.add(LSTM(300, activation='tanh'))
        # 输出层有一个神经元
        model.add(Dense(1))
        model.compile(loss='mae', optimizer='adam')
        model.fit(X_train, y_train, verbose=1, epochs=100)
        model.save('lstm_model.h5')

    predict = model.predict(X_test)
    return predict