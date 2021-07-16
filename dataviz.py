import matplotlib.pyplot as plt
import pandas as pd

# uncomment to see the result of processing
'''
# befiore-after comaparison
cycle1 = 0
cycle2 = 1
df = pd.read_csv('processed_data/Data_Capacity_25C01_processed.csv')
df = df[(df['n_cycle'] == cycle1) | (df['n_cycle'] == cycle2)]
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 6))
ax[0].plot(df.t_h, df.capacity, label='Cycle {} and {}'.format(cycle1, cycle2))
ax[0].set_xlabel('Time (h)')
ax[0].set_ylabel('Capacity (mAh)')
ax[0].set_title('Before Processing')
ax[0].grid(linewidth=0.5, alpha=0.5)
ax[0].legend()
ax[1].plot(df.t_h, df.new_capacity, label='Cycle {} and {}'.format(cycle1, cycle2))
ax[1].set_xlabel('Time (h)')
ax[1].set_ylabel('Capacity (mAh)')
ax[1].set_title('After Processing')
ax[1].grid(linewidth=0.5, alpha=0.5)
ax[1].legend()
plt.tight_layout()
plt.show()
'''


for temp in [25, 35, 45]:
    df = pd.read_csv('processed_data/Data_Capacity_{}C01_processed.csv'.format(temp))
    grouped = df.groupby('n_cycle')
    fig, ax = plt.subplots(figsize=(20, 10))
    for cycle in range(int(df.n_cycle.max())+1):
        group = grouped.get_group(cycle)
        color = 'blue' if cycle % 2 == 0 else 'orange'
        ax.plot(group.t_h, group.new_capacity, c=color)
    ax.set_xlabel('time (Hours)')
    ax.set_ylabel('Capacity (mAh)')
    ax.set_title(u'Capacity Degradarion at {}\N{DEGREE SIGN}C for {} cycles'.format(temp, int(df.n_cycle.max()+1)))
    ax.set_xlim(df.t_h.min(), df.t_h.max())
    ax.set_ylim(0, None)
    ax.grid(linewidth=0.5, alpha=0.5)
    plt.tight_layout()
    plt.show()
