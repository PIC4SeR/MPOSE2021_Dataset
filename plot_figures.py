import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scripts.lib_common as lc
import numpy as np
import os
from init_vars import *

report, data, frames = lc.read_poses()

datasets = ['KTH', 'IXMAS', 'ISLD', 'ISLDAS', 'Weizmann', 'i3DPost']
palette = sns.color_palette('tab10', n_colors=6)
colors = {dataset.lower(): palette[i] for i, dataset in enumerate(datasets)}

# average confidence
plt.figure()
ax = sns.boxplot(x="dataset", y="aver_conf", data=report, whis=np.inf, palette=colors)
plt.savefig(os.path.join(paths['figures'], 'report_aver_conf.png'), bbox_inches='tight')
print('Saved figure: {}'.format(os.path.join(paths['figures'], 'report_aver_conf.png')))

# number of frames
fig, axs = plt.subplots(3, 2, figsize=(7, 7))
sns.set(style="darkgrid")
for ax, dataset in zip(axs.reshape(-1)[:len(datasets)], datasets):
    sns.histplot(data=report[report['dataset'] == dataset.lower()],
                 x="length", color=colors[dataset.lower()], label=dataset,
                 ax=ax, discrete=True, legend=True)
    ax.set_ylabel('sequences')
    ax.set_xlabel('length')
    ax.legend(loc='upper left')
    ax.set_xlim([19, 31])
plt.tight_layout()
plt.savefig(os.path.join(paths['figures'], 'report_frame_num.png'), bbox_inches='tight')
print('Saved figure: {}'.format(os.path.join(paths['figures'], 'report_frame_num.png')))

