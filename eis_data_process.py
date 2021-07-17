import pandas as pd
import numpy as np
import os
'''
try:
    os.mkdir('EIS_data_processed')
except:
    print('Folder already exists. ',
          'The script might have already been run one. ',
          'Please check the folder once.')
'''

state_dict = {'I': 1, 'II': 2,
              'III': 3, 'IV': 4,
              'V': 5, 'VI': 6,
              'VII': 7, 'VIII': 8,
              'IX': 9, 'X': 10}

temp_list = ['25C', '35C', '45C']

cell_list = ['C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08']

new_cols = ['time', 'cycle', 'f', 're', '-im', 'z', 'ph_z']


filename = 'EIS_data/EIS_state_III_45C02.txt'
if '25C' in filename:
    df = pd.read_csv(filename, delimiter='\t')
    df.columns = new_cols
else:
    df = pd.read_csv(filename, delimiter='\t', header=None)
    df.columns = new_cols


for temp in temp_list:
    if temp in filename:
        maxcap_df = pd.read_csv('Max_Capacity_Data/maxcap_data_{}.csv'.format(temp))
        room_temp = temp
maxcap_col = maxcap_df.columns.get_loc('max_capacity')


new_df_col = list(df[df.cycle == 1].f)
new_df_col.extend(['cycle', 'state', 'temperature', 'max_capacity'])
fin_df = pd.DataFrame(columns=new_df_col)


grouped = df.groupby('cycle')
max_cycle = int(df.cycle.max())
indexes_to_append = range(max_cycle)
for index_to_append, cycle in zip(indexes_to_append, range(1, max_cycle+1)):
    group = grouped.get_group(cycle)
    row = list()
    z = group.z
    row.extend(list(z))
    for state in state_dict:
        if state in filename:
            cell_state = state
    row.extend([cycle, cell_state, room_temp])

    for cell in cell_list:
        if cell in filename:
            temp_df = maxcap_df[(maxcap_df.cycle == cycle) & (maxcap_df.cell == cell)]
            row.append(temp_df.iloc[0, maxcap_col])
    fin_df.loc[index_to_append] = row

print(fin_df.head(5))
fin_df.to_csv('test.csv')
