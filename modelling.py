import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (mean_absolute_percentage_error,
                             mean_absolute_error,
                             mean_squared_error)

qualitative_feat = ['state']

df = pd.read_csv('EIS_data_processed/eis_data_processed_25C.csv')
df['temperature'] = [25 for _ in range(len(df))]

for filename in os.listdir('EIS_data_processed'):
    if filename == 'eis_data_processed_25C.csv':
        continue
    data = pd.read_csv('EIS_data_processed/'+filename)
    df = pd.concat([df, data], ignore_index=True)

X = df.drop(columns=['max_capacity'])
y = df.max_capacity

# preprocessing
X = pd.get_dummies(X)

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    shuffle=True,
                                                    random_state=123)

regressor = RandomForestRegressor(n_jobs=-1, verbose=True)
regressor.fit(x_train, y_train)
y_pred = regressor.predict(x_test)
mabsp_err = mean_absolute_percentage_error(y_test, y_pred)
mabs_err = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred)
print(f'Mean Absolute Percentage Error: {mabsp_err}\n',
      f'Mean Absolute Error(mAh): {mabs_err}\n',
      f'RMSE: {rmse}')
