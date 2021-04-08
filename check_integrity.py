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
import sys


try:
    target = sys.argv[1]
except:
    target = 'video'


def generate_checksums(path):
    report = pd.DataFrame(columns=['sample', 'cksum'])
    for f in os.listdir(path):
        report = report.append({'sample': f,
                                'cksum': hashlib.md5(open(os.path.join(path, f), 'rb').read()).hexdigest()},
                               ignore_index=True)
    report = report.set_index('sample')

    return report


def check_integrity(current, path):
    standard = pd.read_csv(path, index_col='sample').sort_values('sample')
    current = current.sort_values('sample')
    try:
        if current.equals(standard):
            print('Test against {} passed!'.format(path))
        else:
            print('Error (code 1)')
    except:
        print('Error (code 2)')


if __name__ == '__main__':
    if 'video' in target:
        current = generate_checksums(paths['video'])
        # current.to_csv(misc_paths['checksum_video'])
        check_integrity(current, misc_paths['checksum_video'])

    if 'rgb' in target:
        current = generate_checksums(paths['rgb'])
        # current.to_csv(misc_paths['checksum_rgb'])
        check_integrity(current, misc_paths['checksum_rgb'])

    if 'pose' in target:
        current = generate_checksums(paths['pose'])
        # current.to_csv(misc_paths['checksum_pose'])
        check_integrity(current, misc_paths['checksum_pose'])
