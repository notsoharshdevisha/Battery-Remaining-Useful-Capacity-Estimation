import os


cell_dict = {'C01': 1, 'C02': 2,
             'C03': 3, 'C04': 4,
             'C05': 5, 'C06': 6,
             'C07': 7, 'C08': 8}

for filename in os.listdir('Capacity_data'):
    for cell in cell_dict.keys():
        print(cell in filename)
