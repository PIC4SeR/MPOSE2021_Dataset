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
from scripts.init_vars import *
import os
import pandas as pd
import sys


def generate_checksums(path):
    report = pd.DataFrame(columns=['sample', 'cksum'])
    for f in os.listdir(path):
        report = report.append({'sample': f,
                                'cksum': hashlib.md5(open(os.path.join(path, f), 'rb').read()).hexdigest()},
                               ignore_index=True)
    report = report.set_index('sample')

    return report

def check_checksums(current, path):
    standard = pd.read_csv(path, index_col='sample').sort_values('sample')
    if current.equals(standard):
        print('Test against {} passed!'.format(path))
    else:
        print('Error! {} checksum does not match'.format(path))

def check_integrity(data='video'):
    print('Checking {} integrity...'.format(data))
    current = generate_checksums(paths[data]).sort_values('sample')
    current.to_csv(logs_path + data + '.csv')
    check_checksums(current, misc_paths['checksum_' + data])