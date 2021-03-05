import shutil
from zipfile import ZipFile
from init_vars import former_paths, archives_paths
import os
import tarfile

verbose = True


def unzip(filename, save_to):
    with ZipFile(filename, 'r') as zipObj:
        for member in zipObj.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue
            source = zipObj.open(member)
            target = open(os.path.join(save_to, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)
            if verbose:
                print('\t', 'Unzipped file {} to {}'.format(filename, save_to))


def untar(filename, save_to):
    tf = tarfile.open(filename)
    tf.extractall(save_to)


def extract(dataset):
    print('Extracting {} dataset...'.format(dataset))
    files = [f for f in os.listdir(archives_paths[dataset]) if os.path.isfile(os.path.join(archives_paths[dataset], f))]
    for file in files:
        if verbose:
            print('\tExtracting: {}'.format(file))
        if file.endswith('.zip'):
            unzip(filename=archives_paths[dataset]+file,
                  save_to=former_paths[dataset])
        elif file.endswith('.tar.gz'):
            untar(filename=archives_paths[dataset]+file,
                  save_to=former_paths[dataset])
        else:
            raise Exception('Extension not supported')


if __name__ == '__main__':
    for dataset in [
        'weizmann',
        'isldas',
        'isld',
        'ixmas',
        'kth',
        'i3dpost'
    ]:
        extract(dataset)