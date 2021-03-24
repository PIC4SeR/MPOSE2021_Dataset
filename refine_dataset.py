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
import pickle


def change_meta(file, new_action):
    dict = pickle.load(open(file, 'rb'))
    dict['action'] = new_action
    dict['name'] = os.path.basename(file)[:-2]
    pickle.dump(dict, open(file, 'wb'))


# Remove sample in post-processing as video-encoding has failed
samples_to_remove = [
    'ixmas_hedlena3_get-up_572.avi-50-79.avi',
]

# remove samples
for i in samples_to_remove:
    if os.path.exists(os.path.join(paths['rgb'], i)):
        os.remove(os.path.join(paths['rgb'], i))
        os.remove(os.path.join(paths['pose'], i))
        print('REMOVED: {}'.format(i))
    else:
        print('Already REMOVED: {}'.format(i))

# redefine outliers (reassign/remove)
for i in os.listdir(misc_paths['outliers']):
    outliers = pd.read_csv(os.path.join(misc_paths['outliers'], i), delimiter='\t', header=None)
    for k, row in outliers.iterrows():
        sample = row[0]
        new_action = row[1]
        meta = get_meta(sample, is_video=False)
        if meta['action'] == new_action:
            continue
        else:
            if new_action in actions.keys():
                new_sample = sample.replace(meta['action'], new_action)
                old = os.path.join(paths['rgb'], sample+'.avi')
                new = os.path.join(paths['rgb'], new_sample+'.avi')
                if (not os.path.exists(old)) and os.path.exists(new):
                    print('\t (done previously) renamed: {} into {}'.format(sample, new_sample))
                elif os.path.exists(old) and (not os.path.exists(new)):
                    os.rename(old, new)
                    old = os.path.join(paths['pose'], sample+'.p')
                    new = os.path.join(paths['pose'], new_sample+'.p')
                    change_meta(file=old, new_action=new_action)
                    os.rename(old, new)
                    print('Renamed: {} into {}'.format(sample, new_sample))

            elif new_action == 'remove':
                old = os.path.join(paths['rgb'], sample+'.avi')
                if not os.path.exists(old):
                    print('\t (done previously) TRASHED: {}'.format(sample))
                else:
                    os.remove(os.path.join(paths['rgb'], sample + '.avi'))
                    os.remove(os.path.join(paths['pose'], sample + '.p'))
                    print('TRASHED: {}'.format(sample))



# pick-up action --> bend action
# turn action --> walk
# for i in os.listdir(paths['rgb']):
#     if 'pick-up' in i:
#         old = os.path.join(paths['rgb'], i)
#         new = os.path.join(paths['rgb'], i.replace('pick-up', 'bend'))
#         os.rename(old, new)
#         print('Renamed: {} into {}'.format(old, new))
#         old = os.path.join(paths['pose'], i.replace('.avi', '.p'))
#         new = os.path.join(paths['pose'], i.replace('pick-up', 'bend').replace('.avi', '.p'))
#         change_meta(file=old, new_action='bend')
#         os.rename(old, new)
#         print('Renamed: {} into {}'.format(old, new))
#     if 'turn' in i:
#         old = os.path.join(paths['rgb'], i)
#         new = os.path.join(paths['rgb'], i.replace('turn', 'walk'))
#         os.rename(old, new)
#         print('Renamed: {} into {}'.format(old, new))
#         old = os.path.join(paths['pose'], i.replace('.avi', '.p'))
#         new = os.path.join(paths['pose'], i.replace('turn', 'walk').replace('.avi', '.p'))
#         change_meta(file=old, new_action='walk')
#         os.rename(old, new)
#         print('Renamed: {} into {}'.format(old, new))
#


















