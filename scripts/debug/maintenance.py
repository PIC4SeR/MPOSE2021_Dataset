import os
import shutil
from ..init_vars import *
import pickle as pkl

def change_meta(file, meta, new_meta):
    dict = pkl.load(open(file, 'rb'))
    dict[meta] = new_meta
    if meta == 'action':
        dict['name'] = os.path.basename(file)[:-2]
    pkl.dump(dict, open(file, 'wb'))


def rename_class(dataset, old_class, new_class):
    for folder in ['json', 'rgb', 'pose']:
        target = [i for i in os.listdir(paths[folder]) if (dataset in i) and (old_class in i)]
        for i in target:
            os.rename(os.path.join(paths[folder], i), os.path.join(paths[folder], i.replace(old_class, new_class)))
            print('Renamed: {} into {}'.format(i, i.replace(old_class, new_class)))


def modify_meta_in_p(dataset, target_class, target_meta, new_meta):
    target = [i for i in os.listdir(paths['pose']) if (dataset in i) and (target_class in i)]
    for i in target:
        change_meta(os.path.join(paths['pose'], i), target_meta, new_meta)
        print('Changed meta for: {}'.format(i))


def delete_files(dataset, class_to_remove):
    for folder in ['json', 'rgb', 'pose']:
        target = [i for i in os.listdir(paths[folder]) if (dataset in i) and (class_to_remove in i)]
        for i in target:
            try:
                os.remove(os.path.join(paths[folder], i))
                print('THRASHED: {}'.format(i))
            except:
                shutil.rmtree(os.path.join(paths[folder], i))
                print('THRASHED: {}'.format(i))


if __name__ == '__main__':

    dataset = 'utdmhad'

    # old_class = 'boxing'
    # new_class = 'box'
    # rename_class(dataset, old_class, new_class)
    # modify_meta_in_p(dataset, 'box', 'action', 'box')

    # to_remove = 'point'
    # delete_files(dataset, to_remove)
