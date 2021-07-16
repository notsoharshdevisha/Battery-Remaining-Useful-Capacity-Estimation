import pandas as pd

for temp in [25, 35, 45]:
    df = pd.read_csv('Capacity_data/Data_Capacity_{}C01.txt'.format(temp),
                     delimiter='\t')
    new_cols = ['t_h', 'n_cycle', 'o_r', 'capacity']
    for col, new_c in zip(df.columns, new_cols):
        df = df.rename(columns={col: new_c})
    df['new_capacity'] = [0 for i in range(len(df.index))]
    df['t_h'] = df['t_h']/60

    col = df.columns.get_loc('o_r')
    jj = df.columns.get_loc('new_capacity')
    kk = df.columns.get_loc('capacity')
    dfgrouped = df.groupby('n_cycle')

    n_cycles = int(df['n_cycle'].max()) + 1

    for cycle in range(n_cycles):

        progress = int(((cycle + 1)/n_cycles * 50))
        print('Temperature: {} | [Progress]: ['.format(temp)
              + '#'*progress
              + '.'*(50-progress) + ']',
              end='\r')

        group = dfgrouped.get_group(cycle)
        group_cap_max = group['capacity'].max()
        for i in group.index:
            if df.iloc[i, col] == 1:
                df.iloc[i, jj] = df.iloc[i, kk]
            else:
                df.iloc[i, jj] = group_cap_max - df.iloc[i, kk]

    df.to_csv("Data_Capacity_{}C01_processed.csv".format(temp), index=False)
