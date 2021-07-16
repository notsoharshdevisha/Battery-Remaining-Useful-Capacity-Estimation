import pandas as pd
import numpy as np
import os

try:
    os.mkdir('EIS_data_processed')
except:
    print('Folder already exists. ',
          'The script might have already been run one. ',
          'Please check the folder once.')

state_dict = {'I': 1, 'II': 2,
              'III': 3, 'IV': 4,
              'V': 5, 'VI': 6,
              'VII': 7, 'VIII': 8,
              'IX': 9, 'X': 10}

temp_list = ['25C', '35C', '45C']

cell_list = ['C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08']

new_df_cols = ['cycle', 'f', 're', '-im', 'z', 'ph_z', 'max_cap']

filename = 'EIS_data/EIS_state_I_45C01.txt'
df = pd.read_csv(filename, delimiter='\t')

for temp in temp_list:
    if temp in filename:
        maxcap_df = pd.read_csv('Max_Capacity_Data/maxcap_data_{}.csv'.format(temp))

new_cols = ['time', 'cycle', 'f', 're', '-im', 'z', 'ph_z']
if '25C' in filename:
    for col, new_col in zip(df.columns, new_cols):
        df = df.rename(columns={col: new_col})
else:
    df.columns = new_cols

for state in state_dict.keys():
    if state in filename:
        df['state'] = [state for _ in range(len(df))]

# the cycle for all files strart from 1
max_cycles = df.cycle.max()
print(max_cycles)

grouped = df.groupby('cycle')



print(df.head(5))
print(len(maxcap_df))
