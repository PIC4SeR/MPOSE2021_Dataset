import os
from init_vars import *
import pandas as pd
from scripts.lib_seq import get_meta
import pickle

# Remove sample in post-processing as video-encoding is failed
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
                meta['action'] = new_action
                new_sample = '{}_{}_{}_{}-{}'.format(meta['dataset'], meta['actor'], meta['action'], meta['unique_id'], meta['window'])
                try:
                    os.rename(os.path.join(paths['rgb'], sample+'.avi'), os.path.join(paths['rgb'], new_sample+'.avi'))
                    os.rename(os.path.join(paths['pose'], sample+'.p'), os.path.join(paths['pose'], new_sample+'.p'))
                    print('Renamed: {} into {}'.format(sample, new_sample))
                except:
                    print('Already renamed: {} into {}'.format(sample, new_sample))
            elif new_action == 'remove':
                try:
                    os.remove(os.path.join(paths['rgb'], sample + '.avi'))
                    os.remove(os.path.join(paths['pose'], sample + '.p'))
                    print('REMOVED: {}'.format(sample))
                except:
                    print('Already REMOVED: {}'.format(sample))

# pick-up action --> bend action
# turn action --> walk
for i in os.listdir(paths['rgb']):
    if 'pick-up' in i:
        old = os.path.join(paths['rgb'], i)
        new = os.path.join(paths['rgb'], i.replace('pick-up', 'bend'))
        os.rename(old, new)
        print('Renamed: {} into {}'.format(old, new))
        old = os.path.join(paths['pose'], i.replace('.avi', '.p'))
        new = os.path.join(paths['pose'], i.replace('pick-up', 'bend').replace('.avi', '.p'))
        os.rename(old, new)
        dict = pickle.load(open(new, 'rb'))
        dict['action'] = 'bend'
        dict['name'] = os.path.basename(new)[:-2]
        pickle.dump(dict, open(new, 'wb'))
        print('Renamed: {} into {}'.format(old, new))
    if 'turn' in i:
        old = os.path.join(paths['rgb'], i)
        new = os.path.join(paths['rgb'], i.replace('turn', 'walk'))
        os.rename(old, new)
        print('Renamed: {} into {}'.format(old, new))
        old = os.path.join(paths['pose'], i.replace('.avi', '.p'))
        new = os.path.join(paths['pose'], i.replace('turn', 'walk').replace('.avi', '.p'))
        os.rename(old, new)
        dict = pickle.load(open(new, 'rb'))
        dict['action'] = 'walk'
        dict['name'] = os.path.basename(new)[:-2]
        pickle.dump(dict, open(new, 'wb'))
        print('Renamed: {} into {}'.format(old, new))



















