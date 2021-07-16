import os
import pandas as pd
import numpy as np

try:
    os.mkdir('Max_Capacity_Data')
except:
    print('The folder already exists maybe. ',
          'Maybe you\'ve already run the code before. '
          'Please check your folder once. ',
          'Otherwise will append same data to same files. ')

if len(os.listdir('Max_Capacity_Data')) == 0:

    cell_dict = {'C01': 1, 'C02': 2,
                 'C03': 3, 'C04': 4,
                 'C05': 5, 'C06': 6,
                 'C07': 7, 'C08': 8}

    diff_list = ['25C02', '25C03', '25C04', '25C06', '25C07', '25C08']
    temp_list = ['45C', '35C', '25C']
    counter = 0
    total_files = len(os.listdir('Capacity_data'))

    for filename in os.listdir('Capacity_data'):
        df = pd.read_csv('Capacity_data/'+filename, delimiter='\t')

        if any(str_ in filename for str_ in diff_list):
            new_cols = ['t_s', 'cycle', 'o_r', 'V', 'I', 'capacity']
            for col, new_col in zip(df.columns, new_cols):
                df = df.rename(columns={col: new_col})
        else:
            new_cols = ['t_s', 'cycle', 'o_r', 'capacity']
            for col, new_c in zip(df.columns, new_cols):
                df = df.rename(columns={col: new_c})

        cellname = None
        for cell in cell_dict.keys():
            if cell in filename:
                cellname = cell

        if cellname is None:
            raise ValueError('No such cell')

        cycle_max_cap_list = []

        max_cycles = int(df.cycle.max() + 1)
        grouped = df.groupby('cycle')
        for cycle in range(max_cycles):
            cycle_max_cap = grouped.get_group(cycle).capacity.max()
            cycle_max_cap_list.append([cycle, cycle_max_cap, cellname])

        maxcapdata = pd.DataFrame(np.array(cycle_max_cap_list),
                                  columns=['cycle', 'max_capacity', 'cell'])

        for str_ in temp_list:
            if str_ in filename: 
                if 'maxcap_data_{}.csv'.format(str_) in os.listdir('Max_Capacity_Data'):
                    maxcapdata.to_csv('Max_Capacity_Data/maxcap_data_{}.csv'.format(str_),
                                      header=False, index=False, mode='a')
                else:
                    maxcapdata.to_csv('Max_Capacity_Data/maxcap_data_{}.csv'.format(str_),
                                      index=False)
        counter += 1
        print('file {} of {} Done'.format(counter, total_files), end='\r')
