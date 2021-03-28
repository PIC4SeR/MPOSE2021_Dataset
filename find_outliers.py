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

import os
from init_vars import *
import pandas as pd
import cv2
from pathlib import Path
import numpy as np
import sys

action = input('Which action? (type label): ')
dataset = input('Which dataset? (type name): ')
text = []
rgb = os.listdir(paths['rgb'])
num = np.sum([1 for i in rgb if (action in i) and (dataset in i)])
count = 0
for i in rgb:
    if (action in i) and (dataset in i):
        count += 1
        # Create a VideoCapture object and read from input file
        cap = cv2.VideoCapture(os.path.join(paths['rgb'], i))

        # Check if camera opened successfully
        if (cap.isOpened() == False):
            print("Error opening video  file")

            # Read until video is completed
        while (cap.isOpened()):

            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
                if frame.shape[0] < 100:
                    frame = cv2.resize(frame, (frame.shape[1]*3, frame.shape[0]*3), fx=0, fy=0, interpolation=resize_interpolation)
                # Display the resulting frame
                cv2.imshow('Frame', frame)

                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

            # Break the loop
            else:
                break

        while True:
            to_do = input('\t{}/{}: {} - What should I do? (remove-9, or type new action, or just press enter to skip): '.format(count, num, i))
            if to_do in ['9', ''] or to_do in actions.keys():
                break
            else:
                print('Please, input a valid value.\t')
                continue

        if to_do == '':
            continue
        elif to_do == '9':
            text.append('{}\t{}'.format(i, 'remove'))
        else:
            text.append('{}\t{}'.format(i, to_do))


        # When everything done, release
        # the video capture object
        cap.release()

        # Closes all the frames
        cv2.destroyAllWindows()

print('Finished!\t')
with open('temp_{}_outliers.txt'.format(action), 'w') as f:
    for item in text:
        f.write("%s\n" % item)
print('Saved: temporary file temp_{}_outliers.txt\t'.format(action))

while True:
    error_occurred = False
    to_do = input('Do you want to integrate results into misc/refine_dataset/{}_outliers.txt? (y/n): '.format(action))
    if to_do == 'y':
        outliers = pd.read_csv(os.path.join(misc_paths['outliers'], '{}_outliers.txt'.format(action)), delimiter='\t', header=None)
        for t in text:
            name = t[:t.find('.avi')]
            do = t[t.find('\t')+1:]
            if name not in outliers[0].to_list():
                outliers = outliers.append({0: name, 1: do}, ignore_index=True)
            else:
                error_occurred = True
                print('{} is conflicting, is \'{}\' but was previously set to \'{}\'. Therefore, skipped.'.format(name,
                                                                                                                  do,
                                                                                                                 outliers.loc[outliers[0] == name, 1].values[0]))
        break
    elif to_do == 'n':
        break
    else:
        print('Please, input a valid value.\t')
        continue

if error_occurred:
    sys.exit()
else:
    if to_do == 'y':
        while True:
            to_do = input('Save a new misc/refine_dataset/{}_outliers.txt? (y/n): '.format(action))
            if to_do == 'y':
                np.savetxt('misc/refine_dataset/{}_outliers.txt'.format(action), outliers.values, fmt='%s\t%s', delimiter='\t')
                break
            elif to_do == 'n':
                break
            else:
                print('Please, input a valid value.\t')
                continue
    else:
        sys.exit()

