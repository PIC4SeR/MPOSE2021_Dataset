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

import hashlib
from init_vars import *
import os
import pandas as pd


def generate_checksums():
    report = pd.DataFrame(columns=['sample', 'cksum'])
    for f in os.listdir(paths['video']):
        report = report.append({'sample': f,
                                'cksum': hashlib.md5(open(os.path.join(paths['video'], f), 'rb').read()).hexdigest()},
                               ignore_index=True)
    report = report.set_index('sample')
    report.to_csv(os.path.join(temp_path, 'cksum.csv'))


def check_integrity():
    current = pd.read_csv(os.path.join(temp_path, 'cksum.csv'), index_col='sample')
    target = pd.read_csv(misc_paths['checksum'], index_col='sample')
    try:
        if ((target == current).sum() == len(target)).values[0]:
            print('Test passed!')
        else:
            print('Error (code 1)')
    except:
        print('Error (code 2)')


if __name__ == '__main__':
    generate_checksums()
    check_integrity()

