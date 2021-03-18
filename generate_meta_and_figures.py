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

import os
from init_vars import *
import pandas as pd
from scripts.lib_seq import get_meta
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import numpy as np

## TODO: this funciton was in lib_common.py
def read_poses(path=paths['pose']):
    report = pd.DataFrame(columns=['name', 'dataset', 'actor', 'action', 'lenght', 'aver_conf'])
    for i in os.listdir(path):
        with open(os.path.join(path, i), 'rb') as f:
            d = pickle.load(f)
        report = report.append({'name': d['name'],
                                'dataset': d['dataset'],
                                'actor': d['actor'],
                                'action': d['action'],
                                'length': d['length'],
                                'aver_conf': np.nanmean(d['seq'][:, 2, :])}, ignore_index=True)
    return report


def read_video(path=paths['video']):
    report = pd.DataFrame(columns=['name', 'dataset', 'actor', 'action', 'lenght', 'aver_conf'])
    for i in os.listdir(path):
        meta = get_meta(i)
        report = report.append({'name': meta['sample'],
                                'dataset': meta['dataset'],
                                'actor': meta['actor'],
                                'action': meta['action']}, ignore_index=True)
    return report

report_vid = read_video()
actions = report_vid.action.drop_duplicates().sort_values()
ax = sns.countplot(x="action", data=report_vid, order=actions)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

report = read_poses()
actions = report.action.drop_duplicates().sort_values()
ax = sns.countplot(x="action", data=report, order=actions)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# split 1
testing_actors = [
    'person12',
    'person23',
    'person08',
    'person02',
    'person24',
    'anna',
    'jiawei',
    'andreas3',
    'julien3',
    'daniel3',
    'alba2',
    'clare3',
    'andreas2',
    'jon',
    'joe',
    'lyova',
    'shahar',
]

df = pd.DataFrame(columns=['sample', 'set'])
for i in os.listdir(paths['rgb']):
    meta = get_meta(i, is_video=False)
    if meta['actor'] in testing_actors:
        df = df.append({'sample': i, 'set': 'test'}, ignore_index=True)
    else:
        df = df.append({'sample': i, 'set': 'train'}, ignore_index=True)

