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
from scripts.init_vars import archives_paths, paths
import os
import tarfile

def unzip(filename, save_to, force=False, verbose=True):
    if verbose:
        print('Extracting OpenPose poses...')
    if any(os.scandir(paths['json'])) and not force:
        if verbose:
            print('\t{} already extracted, skipping...'.format(os.listdir(archives_paths['json'])[0]))
    else:
        if verbose:
            print('\tExtracting: {}'.format(os.listdir(archives_paths['json'])[0]))
        with ZipFile(filename, 'r') as zipObj:
            zipObj.extractall(save_to.replace('json/', ''))

def extract_json(force=False, verbose=True):
    unzip(filename=os.path.join(archives_paths['json'], os.listdir(archives_paths['json'])[0]),
          save_to=paths['json'], force=force, verbose=verbose)