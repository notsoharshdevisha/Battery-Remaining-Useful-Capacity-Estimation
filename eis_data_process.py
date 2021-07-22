import pandas as pd
import numpy as np
import os


try:
    os.mkdir('EIS_data_processed')
except:
    raise FileExistsError('Folder already exists. ',
                          'The script might have already been run once. ',
                          'Please check the folder once.')

state_dict = {'I': 1, 'II': 2,
              'III': 3, 'V': 5,
              'IV': 4, 'VI': 6,
              'VII': 7, 'VIII': 8,
              'X': 10, 'IX': 9}

temp_dict = {'25C': 25, '35C': 35, '45C': 45}

cell_list = ['C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08']

new_cols = ['time', 'cycle', 'f', 're', '-im', 'z', 'ph_z']

total_files = len(os.listdir('EIS_data'))-1
files_done = 0

if len(os.listdir('EIS_data_processed')) == 0:
    for filename in os.listdir('EIS_data'):

        if filename == '.DS_Store':
            continue

        if '25C' in filename:
            df = pd.read_csv('EIS_data/'+filename, delimiter='\t')
            df.columns = new_cols
        else:
            df = pd.read_csv('EIS_data/'+filename, delimiter='\t', header=None)
            df.columns = new_cols

        for temp in temp_dict.keys():
            if temp in filename:
                maxcap_df = pd.read_csv('Max_Capacity_Data/maxcap_data_{}.csv'.format(temp))
                room_temp = temp_dict[temp]

        maxcap_col = maxcap_df.columns.get_loc('max_capacity')

        new_df_col = list(df[df.cycle == 1].f)
        new_df_col.extend(['cycle', 'state', 'temperature', 'cell', 'max_capacity'])
        fin_df = pd.DataFrame(columns=new_df_col)
        expected_cols = len(new_df_col)

        grouped = df.groupby('cycle')
        max_cycles = int(df.cycle.max())
        indexes_to_append = range(max_cycles)
        for index_to_append, cycle in zip(indexes_to_append, range(1, max_cycles+1)):
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
                    current_cell = cell
                    temp_df = maxcap_df[(maxcap_df.cycle == cycle) & (maxcap_df.cell == cell)]
                    if not temp_df.empty:
                        row.extend([current_cell, temp_df.iloc[0, maxcap_col]])

# 65 columns expected 60 frequencies and 5 added
            if len(row) == 65:
                fin_df.loc[index_to_append] = row

        for temp in temp_dict.keys():
            if temp in filename:
                if 'eis_data_processed_{}.csv'.format(temp) in os.listdir('EIS_data_processed'):
                    fin_df.to_csv('EIS_data_processed/eis_data_processed_{}.csv'.format(temp),
                                  index=False, header=False, mode='a')
                else:
                    fin_df.to_csv('EIS_data_processed/eis_data_processed_{}.csv'.format(temp),
                                  index=False)

        files_done += 1
        print(f'{files_done} of {total_files} files done!', end='\r')

