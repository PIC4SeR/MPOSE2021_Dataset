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

import shutil
from zipfile import ZipFile
from init_vars import former_paths, archives_paths
import os
import tarfile

def unzip(filename, save_to):
    with ZipFile(filename, 'r') as zipObj:
        for member in zipObj.namelist():
            file = os.path.basename(member)
            # skip directories
            if not file:
                continue
            source = zipObj.open(member)
            target = open(os.path.join(save_to, file), "wb")
            with source, target:
                shutil.copyfileobj(source, target)

def untar(filename, save_to):
    tf = tarfile.open(filename)
    tf.extractall(save_to)

def untar_isld(filename, save_to):
    target = 'ISLD/ISLD_RGB_original_videos.tar.xz'
    tar = tarfile.open(filename)
    for member in tar.getmembers():
        if member.name == target:
            tar.extract(member, save_to)
            sub_tar = tarfile.open(save_to+target)
            sub_tar.extractall(save_to)
            for i in os.listdir(save_to+'RGB/'):
                os.replace(save_to+'RGB/'+i, save_to+i)
            shutil.rmtree(save_to+'RGB/')
            shutil.rmtree(save_to + 'ISLD/', ignore_errors=True)

def unzip_all(filename, save_to):
    with ZipFile(filename, 'r') as zipObj:
        zipObj.extractall(save_to)

def extract(dataset, verbose=True):
    print('Extracting from {} archive...'.format(dataset))
    files = [f for f in os.listdir(archives_paths[dataset]) if os.path.isfile(os.path.join(archives_paths[dataset], f))]
    for file in files:
        if verbose:
            print('\tExtracting: {}'.format(file))
        if dataset in ['utkinect', 'utdmhad']:
            unzip_all(filename=archives_paths[dataset] + file,
                  save_to=former_paths[dataset])
        elif file.endswith('.zip'):
            unzip(filename=archives_paths[dataset]+file,
                  save_to=former_paths[dataset])
        elif file.endswith('.tar.gz'):
            untar(filename=archives_paths[dataset]+file,
                  save_to=former_paths[dataset])
        elif file.endswith('.tar.xz') and dataset == 'isld':
            untar_isld(filename=archives_paths[dataset]+file,
                       save_to=former_paths[dataset])

def extract_formers(verbose=True):
    for dataset in precursors:
        extract(dataset, verbose=verbose)
            
            
if __name__ == '__main__':
    extract_formers()
