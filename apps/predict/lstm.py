from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import load_model

def train(train_X, train_y, test_X, test_y, param):
    str = "lstm_"+param+'.h5'
    try:
        model = load_model(str)
        print("训练好的LSTM", model)
    except:
        model = Sequential()
        # 隐藏层有100个神经元
        model.add(LSTM(100, input_shape=(train_X.shape[1], train_X.shape[2]), return_sequences=True))
        model.add(LSTM(300, activation='tanh'))
        # 输出层有一个神经元
        model.add(Dense(1))
        model.compile(loss='mae', optimizer='adam')
        history = model.fit(train_X, train_y, verbose=1, epochs=100, validation_data=(test_X, test_y))
        model.save(str)
    return model