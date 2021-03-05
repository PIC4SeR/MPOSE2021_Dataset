import shutil
from zipfile import ZipFile
from init_vars import archives_paths, paths
import os
import tarfile

verbose = True


def unzip(filename, save_to):
    with ZipFile(filename, 'r') as zipObj:
        zipObj.extractall(save_to.replace('json/', ''))

if __name__ == '__main__':
    print('Extracting json archive...')
    unzip(filename=os.path.join(archives_paths['json'], os.listdir(archives_paths['json'])[0]),
          save_to=paths['json'])
