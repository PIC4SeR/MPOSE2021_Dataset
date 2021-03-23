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

from init_vars import *
from misc.video_lists import *
import os
import cv2
import pandas as pd
import shutil


def process_former(dataset):
    if dataset == 'weizmann':
        print('WEIZMANN DATASET PRE-PROCESSING:')
        unique_id = 0
        for i in weizmann_video_list:
            action = i[i.find('_') + 1:i.find('.')]
            actor = i[:i.find('_')]
            if action in ['bend', 'jump', 'pjump', 'run', 'walk', 'wave1', 'wave2']:
                new_name = '{}{}_{}_{}_{}{}'.format(paths['video'], dataset, actor, action, unique_id,
                                                    video_extention)
                print('\tCopying: {}'.format(new_name))
                shutil.copy(former_paths[dataset] + i, new_name)
                unique_id += 1

    elif dataset == 'isldas':
        print('{} pre-processing:'.format(dataset))
        for unique_id, i in enumerate(isldas_video_list):
            res = [j for j in range(len(i)) if i.startswith('_', j)]
            actor = i[res[0] + 1:res[1]]
            action = i[res[1] + 1:res[2]]
            if action == '7':
                action = 'walk'
            elif action == '8':
                action = 'wave1'
            elif action == '9':
                action = 'box'
            elif action == '10':
                action = 'kick'
            elif action == '11':
                action = 'point'
            elif action == '15':
                action = 'bend'
            elif action == '16':
                action = 'hands-clap'
            elif action == '17':
                action = 'wave2'
            elif action == '21':
                action = 'run'
            else:
                continue
            new_name = '{}{}_{}_{}_{}{}'.format(paths['video'], dataset, actor, action, unique_id,
                                                video_extention)
            print('\tEncoding: {}'.format(new_name))
            shutil.copy('{}{}'.format(former_paths[dataset], i), new_name)

    elif dataset == 'isld':
        print('{} pre-processing:'.format(dataset))
        unique_id = 0
        for i in isld_video_list:
            actor = i[:i.find('_')]
            gt = pd.read_excel(misc_paths[dataset], sheet_name=actor, header=1, usecols='A:F')
            gt = gt.sort_values(by='start')
            vidcap = cv2.VideoCapture(former_paths[dataset] + i)
            success, image = vidcap.read()
            frame_num = 1
            count = 0
            index = gt.index[count]
            start = gt.loc[index, 'start']
            while success:
                if frame_num == start:
                    if gt.loc[index, 'Action'] == 'checkwatch':
                        action = 'check-watch'
                    elif gt.loc[index, 'Action'] == 'scratchhead':
                        action = 'scratch-head'
                    elif gt.loc[index, 'Action'] == 'crossarms':
                        action = 'cross-arms'
                    elif gt.loc[index, 'Action'] == 'hclap':
                        action = 'hands-clap'
                    elif gt.loc[index, 'Action'] == 'hwav2':
                        action = 'wave2'
                    elif gt.loc[index, 'Action'] == 'hwav1':
                        action = 'wave1'
                    elif gt.loc[index, 'Action'] == 'sitdown':
                        action = 'sit-down'
                    elif gt.loc[index, 'Action'] == 'getup':
                        action = 'get-up'
                    elif gt.loc[index, 'Action'] == 'nothing':
                        action = 'standing'
                    else:
                        action = gt.loc[index, 'Action']
                    new_name = '{}{}_{}_{}_{}{}'.format(paths['video'], dataset, actor.lower(), action, unique_id,
                                                        video_extention)
                    print('\tEncoding: {}'.format(new_name))
                    out = cv2.VideoWriter(new_name,
                                          codec,
                                          fps[dataset],
                                          frame_size[dataset])
                if frame_num >= start:
                    out.write(cv2.resize(image, frame_size[dataset], fx=0, fy=0, interpolation=resize_interpolation))

                if frame_num == gt.loc[index, 'end']:
                    out.release()
                    unique_id += 1
                    count += 1
                    try:
                        index = gt.index[count]
                        start = gt.loc[index, 'start']
                    except:
                        break
                success, image = vidcap.read()
                frame_num += 1
            vidcap.release()

    elif dataset == 'ixmas':
        print('{} pre-processing:'.format(dataset))
        for unique_id, i in enumerate(ixmas_video_list):
            res = [j for j in range(len(i)) if i.startswith('_', j)]
            actor = i[:res[0]]
            action = i[res[1] + 1:res[2]]
            if action == 'wave':
                action = 'wave1'
            elif action == 'turn-around':
                action = 'turn'
            elif action == 'punch':
                action = 'box'
            new_name = '{}{}_{}_{}_{}{}'.format(paths['video'], dataset, actor, action, unique_id,
                                                video_extention)
            print('\tCopying: {}'.format(new_name))
            shutil.copy('{}{}'.format(former_paths[dataset], i), new_name)
            unique_id += 1

    elif dataset == 'kth':
        print('{} pre-processing:'.format(dataset))
        unique_id = 0
        for i in kth_video_list:
            print('\t', 'Splitting: {}'.format(i))
            res = [j for j in range(len(i)) if i.startswith('_', j)]
            actor = i[:res[0]]
            action = i[res[0] + 1:res[1]]
            if action == 'running':
                action = 'run'
            elif action == 'walking':
                action = 'walk'
            elif action == 'handwaving':
                action = 'wave2'
            elif action == 'boxing':
                action = 'box'
            elif action == 'hwav2':
                action = 'wave2'
            elif action == 'jogging':
                action = 'jog'
            elif action == 'handclapping':
                action = 'hands-clap'
            new_name = '{}{}_{}_{}_{}{}'.format(paths['video'], dataset, actor, action, unique_id,
                                                video_extention)
            print('\tCopying: {}'.format(new_name))
            shutil.copy('{}{}'.format(former_paths[dataset], i), new_name)
            unique_id += 1

    elif dataset == 'i3dpost':
        print('{} pre-processing:'.format(dataset))
        gt = pd.read_csv(misc_paths[dataset], header=0, dtype=str)
        unique_id = 0
        for actor in i3dpost_list['actor']:
            child_dir = os.listdir(os.path.join(former_paths[dataset], actor))[0]
            for s in i3dpost_list[actor]:
                action = gt.loc[(gt['Code'] == s) & (gt['Actor'] == actor), 'Action'].values[0].lower()
                if action == 'hand-wave':
                    action = 'wave1'
                elif action == 'jump in place':
                    action = 'pjump'
                for pov in i3dpost_list['pov'][actor]:
                    unique_id += 1
                    folder = os.path.join(former_paths[dataset], actor, child_dir, s, pov)
                    new_name = '{}{}_{}_{}_{}{}'.format(paths['video'], dataset, actor.lower(), action, unique_id,
                                                        video_extention)
                    print('\tEncoding: {}'.format(new_name))
                    out = cv2.VideoWriter(new_name,
                                          codec,
                                          fps[dataset],
                                          frame_size[dataset])
                    frame_num = 0
                    success = True
                    while success:
                        try:
                            image = cv2.imread(folder + '/' + '0' * (5 - len(str(frame_num))) + str(frame_num) + '.png')
                            out.write(
                                cv2.resize(image, frame_size[dataset], fx=0, fy=0, interpolation=resize_interpolation))
                            frame_num += 1
                        except:
                            success = False
                    out.release()


if __name__ == '__main__':
    for dataset in [
        'weizmann',
        'isldas',
        'isld',
        'ixmas',
        'kth',
        'i3dpost'
    ]:
        process_former(dataset)




