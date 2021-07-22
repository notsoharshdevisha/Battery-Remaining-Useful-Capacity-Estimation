import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from natsort import index_natsorted
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (mean_absolute_percentage_error,
                             mean_absolute_error,
                             mean_squared_error)
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

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    shuffle=True,
                                                    random_state=123)
#'''
# modelling
regressor = RandomForestRegressor(n_jobs=-1)
regressor.fit(x_train, y_train)
y_pred = regressor.predict(x_test)
mabsp_err = mean_absolute_percentage_error(y_test, y_pred)
mabs_err = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred)
print(f' Mean Absolute Percentage Error: {mabsp_err}\n',
      f'Mean Absolute Error(mAh): {mabs_err}\n',
      f'RMSE: {rmse}')

feat_imp = regressor.feature_importances_
# print(feat_imp)
#'''

print('Performing KFold for further analysis..')
# performing on kfolds
kf = KFold(n_splits=5, random_state=123, shuffle=True)

kf_err = []
x = np.array(X)
for i, (train_index, test_index) in enumerate(kf.split(X)):
    x_train, x_test = x[train_index], x[test_index]
    y_train, y_test = y[train_index], y[test_index]

    regressor = RandomForestRegressor(n_jobs=-1, verbose=True)
    regressor.fit(x_train, y_train)
    y_pred = regressor.predict(x_test)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    kf_err.append([i, rmse, mape, mae])

# print(kf_err)

kf_err_df = pd.DataFrame(columns=['KFold', 'RMSE', 'MAPE', 'MAE'])
kf_err_df['KFold'] = [row[0] for row in kf_err]
kf_err_df['RMSE'] = [row[1] for row in kf_err]
kf_err_df['MAPE'] = [row[2] for row in kf_err]
kf_err_df['MAE'] = [row[3] for row in kf_err]
# print(kf_err_df.head(5))

fig, ax = plt.subplots()
ax.bar(kf_err_df.KFold-0.3, kf_err_df.RMSE, width=0.3, label='RMSE', color='#5899DA')
ax.bar(kf_err_df.KFold, kf_err_df.MAPE, width=0.3, label='MAPE', color='#19A979')
ax.bar(kf_err_df.KFold+0.3, kf_err_df.MAE, width=0.3, label='MAE', color='#ED4A7B')
ax.set_xlabel('KFold')
ax.set_title('Errors')
plt.legend()
plt.tight_layout()
plt.show()

feat_imp_df = pd.DataFrame(index=X.columns)
feat_imp_df['feature importance'] = feat_imp
feat_imp_df = feat_imp_df.sort_values(by='feature importance',
                                      ascending=False,
                                      key=lambda x: np.argsort(index_natsorted(feat_imp_df['feature importance'])))


top_ten_feat = feat_imp_df.iloc[0:10, :]
fig, ax = plt.subplots()
ax.bar(top_ten_feat.index, top_ten_feat['feature importance'], color='#1866b4')
ax.set_xticklabels(top_ten_feat.index, rotation=45)
ax.set_xlabel('Features')
ax.set_ylabel('Weights')
ax.set_title('Feature Importance')
plt.tight_layout()
plt.show()
