from init_vars import *
import pandas as pd
from lib.lib_common import read_poses

testing_actors = {1: ['person12',
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
                      's02',
                      's07',
                      'ss1',
                      'ss4'],
                  2: ['person01',
                      'person07',
                      'person16',
                      'person20',
                      'person25',
                      'karam',
                      'zeyu',
                      'florian1',
                      'daniel2',
                      'andreas1',
                      'nicolas3',
                      'amel1',
                      'chiara3',
                      'jean',
                      'haidi',
                      'daria',
                      'eli',
                      's08',
                      's05',
                      'ss7',
                      'ss8'],
                  3: ['person03',
                      'person11',
                      'person17',
                      'person21',
                      'person14',
                      'scott',
                      'zaid',
                      'hedlena3',
                      'julien1',
                      'nicolas2',
                      'amel3',
                      'daniel1',
                      'chiara1',
                      'hansung',
                      'nikos',
                      'moshe',
                      'ira',
                      's04',
                      's10',
                      'ss2',
                      'ss5']}


def create_splits():
    report = read_poses()
    for i in range(1, 4):
        split = pd.DataFrame({'sample': report.loc[report.actor.isin(testing_actors[i]), 'sample'],
                              'set': 'test'})
        split = pd.concat([split,
                           pd.DataFrame({'sample': report.loc[~report.actor.isin(testing_actors[i]), 'sample'],
                                         'set': 'train'})])
        split.to_csv(logs_path + 'train_test_split{}.txt'.format(i), sep='\t', index=None, header=None)

if __name__ == '__main__':
    create_splits()