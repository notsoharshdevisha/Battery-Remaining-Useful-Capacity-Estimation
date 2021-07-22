import os 
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import (mean_squared_error, mean_absolute_error,
                             mean_absolute_percentage_error)
import numpy as np
import warnings
warnings.filterwarnings('ignore')


df = pd.read_csv('EIS_data_processed/eis_data_processed_25C.csv')
 
for filename in os.listdir('EIS_data_processed'):
    if filename == 'eis_data_processed_25C.csv':
        continue
    data = pd.read_csv('EIS_data_processed/'+filename)
    df = pd.concat([df, data], ignore_index=True)
 
X = df.drop(columns=['max_capacity', 'cell'])
y = df.max_capacity
 
# preprocessing
X = pd.get_dummies(X)

X = np.array(X)
y = np.array(y)
scaler = MinMaxScaler()
X = scaler.fit_transform(X)
y = scaler.fit_transform(y.reshape(-1, 1))
 
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    shuffle=True,
                                                    random_state=123)


# initializing model
model = Sequential()
model.add(Dense(50, input_dim=X.shape[1], activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(1, activation='relu'))
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=10, batch_size=32)
y_pred = model.predict(x_test)

y_test = scaler.inverse_transform(y_test)
y_pred = scaler.inverse_transform(y_pred)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)




    
