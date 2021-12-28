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
            gt = pd.read_excel(misc_paths[dataset], sheet_name=actor, header=1, usecols='A:F', engine='openpyxl')
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

    elif dataset == 'utkinect':
        print('{} pre-processing:'.format(dataset))
        temp = pd.read_csv(misc_paths[dataset], header=None)
        gt = pd.DataFrame(columns=['sample', 'actor', 'counter', 'action', 'start', 'end'])
        ids = [i for i, row in temp.iterrows() if row[0] in utkinect_list]
        for i, j in zip(ids[:-1], ids[1:]):
            sample = temp.loc[i, 0]
            record = {'sample': sample,
                      'actor': sample[:sample.find('_')],
                      'counter': sample[sample.find('_') + 1:]}
            for k, row in temp.loc[range(i+1, j)].iterrows():
                row = row[0].strip()
                record['action'] = row[:row.find(':')]
                if record['action'] == 'sitDown':
                    record['action'] = 'sit-down'
                elif record['action'] == 'standUp':
                    record['action'] = 'get-up'
                elif record['action'] == 'pickUp':
                    record['action'] = 'pick-up'
                elif record['action'] == 'waveHands':
                    record['action'] = 'wave2'
                elif record['action'] == 'clapHands':
                    record['action'] = 'hands-clap'
                elif record['action'] == 'pull':
                    record['action'] = 'point'
                elif record['action'] == 'push':
                    record['action'] = 'point'
                elif record['action'] == 'carry':
                    record['action'] = 'walk'
                elif record['action'] == 'throw':
                    record['action'] = 'wave1'
                record['start'], record['end'] = [int(i) for i in row[row.find(':')+2:].split(' ')]
                gt = gt.append(record, ignore_index=True)

        for unique_id, sample in enumerate(utkinect_list):
            folder = os.path.join(former_paths[dataset], 'RGB', sample)
            frames_nums = sorted([int(i.replace('colorImg', '').replace('.jpg', '')) for i in os.listdir(folder) if 'Copy' not in i])
            for i, row in gt.loc[gt['sample'] == sample].iterrows():
                window = [t for t in frames_nums if t>= row['start'] and t<=row['end']]
                new_name = '{}{}_{}_{}_{}_{}-{}-{}{}'.format(paths['video'], dataset,
                                                             row['actor'], row['action'], row['counter'],
                                                             unique_id, row['start'], row['end'], video_extention)
                print('\tEncoding: {}'.format(new_name))
                out = cv2.VideoWriter(new_name,
                                      codec,
                                      fps[dataset],
                                      former_frame_size[dataset])
                for t in window:
                    image = cv2.imread(os.path.join(folder, 'colorImg'+str(t)+'.jpg'))
                    out.write(cv2.resize(image, frame_size[dataset], fx=0, fy=0, interpolation=resize_interpolation))
                out.release()

    elif dataset == 'utdmhad':
        print('{} pre-processing:'.format(dataset))
        gt = pd.read_csv(misc_paths[dataset], header=0, index_col=0)
        unique_id = 0
        for sample in utdmhad_list:
            action, actor, counter, _ = sample.split('_')
            action = gt.loc[int(action[1:])].values[0]
            actor = 's'+actor
            if action in ['swipt_left', 'swipt_right', 'wave', 'throw', 'catch', 'knock', 'draw_x', 'draw_circle_CW',
                          'draw_circle_CCW', 'draw_triangle', 'tennis_swing', 'catch']:
                action = 'wave1'
            elif action == 'clap':
                action = 'hands-clap'
            elif action == 'arm_cross':
                action = 'cross-arms'
            elif action == 'sit2stand':
                action = 'get-up'
            elif action == 'stand2sit':
                action = 'sit-down'
            elif action in ['basketball_shoot', 'baseball_swing', 'tennis_serve']:
                action = 'wave2'
            elif action == 'boxing':
                action = 'box'
            elif action in ['push', 'bowling', 'arm_curl', 'knock', 'pickup_throw', 'lunge', 'squat']:
                continue
            unique_id += 1
            file = os.path.join(former_paths[dataset], 'RGB', sample)
            new_file = os.path.join(paths['video'], '{}_{}_{}_{}_{}.avi'.format(dataset, actor, action, counter, unique_id))
            print('\tCopying: {}'.format(new_file))
            shutil.copy(file, new_file)


if __name__ == '__main__':
    for dataset in [
        'weizmann',
        'isldas',
        'isld',
        'ixmas',
        'kth',
        'i3dpost',
        'utkinect',
        'utdmhad',
    ]:
        process_former(dataset)




