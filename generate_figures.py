# Copyright (C) 2021  Federico Angelini
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details:
# http://www.gnu.org/licenses/gpl.txt

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scripts.lib_common as lc
import numpy as np
import os
from init_vars import *

report_openpose = lc.read_poses(paths['pose'])
report_posenet = lc.read_poses(paths['posenet'])

datasets = ['KTH',
            'IXMAS',
            'i3DPost',
            'Weizmann',
            'ISLD',
            'ISLD-AS',
            'UTKinect',
            'UTD-MHAD']
palette = sns.color_palette('tab10', n_colors=len(datasets))
colors = {dataset.lower().replace('-', ''): palette[i] for i, dataset in enumerate(datasets)}

# average confidence
df1 = report_openpose[['dataset', 'aver_conf']]
df1['detector'] = 'openpose'
df2 = report_posenet[['dataset', 'aver_conf']]
df2['detector'] = 'posenet'
plt.figure()
ax = sns.boxplot(x="dataset", y="aver_conf", hue='detector', data=df1.append(df2), whis=np.inf)
ax.set_xticklabels(datasets)
plt.xticks(rotation=45)
plt.savefig(os.path.join(paths['figures'], 'report_aver_conf.pdf'), bbox_inches='tight')
print('Saved figure: {}'.format(os.path.join(paths['figures'], 'report_aver_conf.pdf')))

# number of frames
report = report_openpose
fig, axs = plt.subplots(4, 2, figsize=(7, 7))
sns.set(style="darkgrid")
for ax, dataset_label in zip(axs.reshape(-1)[:len(datasets)], datasets):
    dataset = dataset_label.lower().replace('-', '')
    sns.histplot(data=report[report['dataset'] == dataset],
                 x="length", color=colors[dataset], label=dataset_label,
                 ax=ax, discrete=True, legend=True)
    ax.set_ylabel('samples')
    ax.set_xlabel('length')
    ax.set_xticks(range(20, 32, 2))
    ax.legend(loc='upper left')
    ax.set_xlim([19, 31])
    ax.set_yscale('log')
plt.tight_layout()
plt.savefig(os.path.join(paths['figures'], 'report_frame_num.pdf'), bbox_inches='tight')
print('Saved figure: {}'.format(os.path.join(paths['figures'], 'report_frame_num.pdf')))

# summary
report = report_openpose
f, ax = plt.subplots()
sns.color_palette("Set1", n_colors=6, desat=.5)
df = {}
total = pd.DataFrame(columns=['samples'], index=sorted(actions.keys()))
total['samples'] = 0
for dataset_label in datasets:
    dataset = dataset_label.lower().replace('-', '')
    df[dataset] = pd.DataFrame(columns=['samples'], index=sorted(actions.keys()))
    df_plot = pd.DataFrame(report.loc[report['dataset'] == dataset, 'action'].value_counts())
    df_plot.rename(columns={'action': 'samples'}, inplace=True)
    df[dataset].update(df_plot)
    df[dataset].fillna(0, inplace=True)
    ax.bar(df[dataset].index, df[dataset].samples, bottom=total.samples, width=1, label=dataset_label, color=colors[dataset])
    total = total.add(df[dataset])
ax.legend(ncol=1, frameon=True, loc='upper left',  bbox_to_anchor=(1, 1))
plt.title('MPOSE2021 ({} actions, {} actors, {} samples)'.format(len(report.action.drop_duplicates()),
                                                                 len(report.actor.drop_duplicates()),
                                                                 len(report)))
ax.set(ylabel="samples",
       xlabel="")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(paths['figures'], 'mpose2021_summary.pdf'))







