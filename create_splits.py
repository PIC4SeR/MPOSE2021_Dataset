import os
from init_vars import *
import pandas as pd
from scripts.lib_common import read_poses

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
                      'shahar'],
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
                      'eli'],
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
                      'ira']}


report = read_poses()

for i in range(1, 3):
    split = pd.DataFrame({'sample': report.loc[report.actor.isin(testing_actors[i]), 'sample'],
                           'set': 'test'})
    split = pd.concat([split,
                       pd.DataFrame({'sample': report.loc[~report.actor.isin(testing_actors[i]), 'sample'],
                                     'set': 'train'})])
    split.to_csv(dataset_path + 'train_testing_split{}.txt'.format(i), sep='\t', index=None, header=None)
