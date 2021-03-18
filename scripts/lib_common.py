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

from init_vars import paths
import os
import pickle
import pandas as pd
import numpy as np

def read_poses(path=paths['pose']):
    report = pd.DataFrame(columns=['sample', 'dataset', 'lenght', 'aver_conf'])
    for i in os.listdir(path):
        with open(os.path.join(path, i), 'rb') as f:
            d = pickle.load(f)
        report = report.append({'sample': d['name'],
                                'dataset': d['dataset'],
                                'actor': d['actor'],
                                'action': d['action'],
                                'length': d['length'],
                                'aver_conf': np.nanmean(d['seq'][:, 2, :])}, ignore_index=True)

    return report

