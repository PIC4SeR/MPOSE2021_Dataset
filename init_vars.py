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
import cv2

# path where the dataset will be exported 
# (specify an absolute path, leave 'MPOSE2021' to export in the current folder)
dataset_path = '/media/MPOSE2021/'

# paths where the formers dataset archives will be stored
# which requires around 180 GB of free space
# (leave as it is if you want to store archives into the "'dataset_path'/archives/" folder)
archives_path = dataset_path + 'archives/'

# temporary folder, which requires 200 GB of free space
# it will contain unzipped archives
# (leave as it is if you want to store temporary files into the "'dataset_path'/temp/" folder)
temp_path = dataset_path + 'temp/'

'''
########################################################################
################ do NOT modify after this point ########################
########################################################################
'''
max_frame_length = 30
min_frame_length = 20

archives_paths = dict(kth=archives_path + 'kth/',
                      ixmas=archives_path + 'ixmas/',
                      i3dpost=archives_path + 'i3dpost/',
                      weizmann=archives_path + 'weizmann/',
                      isld=archives_path + 'isld/',
                      isldas=archives_path + 'isldas/',
                      utkinect=archives_path + 'utkinect/',
                      utdmhad=archives_path + 'utdmhad/',
                      json=archives_path + 'json/',
                      posenet=archives_path + 'posenet/')
del archives_path

former_paths = dict(kth=temp_path + 'kth/',
                    ixmas=temp_path + 'ixmas/',
                    i3dpost=temp_path + 'i3dpost/',
                    weizmann=temp_path + 'weizmann/',
                    isld=temp_path + 'isld/',
                    isldas=temp_path + 'isldas/',
                    utkinect=temp_path + 'utkinect/',
                    utdmhad=temp_path + 'utdmhad/')

paths = dict(video=dataset_path + 'video/',
             pose=dataset_path + 'pose/',
             posenet=dataset_path + 'posenet_pose/',
             json=dataset_path + 'json/',
             figures=dataset_path + 'figures/',
             rgb=dataset_path + 'rgb/')

actions = {'standing': 0,
           'check-watch': 1,
           'cross-arms': 2,
           'scratch-head': 3,
           'sit-down': 4,
           'get-up': 5,
           'turn': 6,
           'walk': 7,
           'wave1': 8,
           'box': 9,
           'kick': 10,
           'point': 11,
           'pick-up': 12,
           'bend': 13,
           'hands-clap': 14,
           'wave2': 15,
           'jog': 16,
           'jump': 17,
           'pjump': 18,
           'run': 19}

fps = dict(kth=25,
           ixmas=25,
           i3dpost=25,
           weizmann=25,
           isld=25,
           isldas=19,
           utkinect=19,
           utdmhad=15)

former_frame_size = dict(kth=(160, 120),
                         ixmas=(64, 48),
                         i3dpost=(1920, 1080),
                         weizmann=(180, 144),
                         isld=(1920, 1080),
                         isldas=(960, 600),
                         utkinect=(640, 480),
                         utdmhad=(640, 480))

frame_size = dict(kth=(160, 120),
                  ixmas=(48, 64),
                  i3dpost=(480, 270),
                  weizmann=(180, 144),
                  isld=(480, 270),
                  isldas=(960, 600),
                  utkinect=(640, 480),
                  utdmhad=(640, 480))
resize_interpolation = cv2.INTER_CUBIC

misc_paths = dict(kth='misc/kth_splitter.csv',
                  ixmas='misc/ixmas_exclude.csv',
                  i3dpost='misc/i3dpost_archives.csv',
                  isld='misc/isld_truth.xlsx',
                  utkinect='misc/utkinect_splitter.txt',
                  utdmhad='misc/utdmhad_truth.csv',
                  checksum_video='misc/cksum_video.csv',
                  checksum_rgb='misc/cksum_rgb.csv',
                  checksum_pose='misc/cksum_pose.csv',
                  outliers='misc/refine_dataset')

video_extention = '.avi'
codec = cv2.VideoWriter_fourcc(*'MPEG')

# OpenPose keypoints index (used for animation only, see scripts.lib_seq.py)
openpose_parts = dict(head=[0, 15, 16, 17, 18],
                      right_foot=[11, 22, 23, 24],
                      left_foot=[14, 19, 20, 21])


if __name__ == '__main__':
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    for i in archives_paths.keys():
        if not os.path.exists(archives_paths[i]):
            os.makedirs(archives_paths[i])
    for i in paths.keys():
        if not os.path.exists(paths[i]):
            os.makedirs(paths[i])
    for i in former_paths.keys():
        if not os.path.exists(former_paths[i]):
            os.makedirs(former_paths[i])

