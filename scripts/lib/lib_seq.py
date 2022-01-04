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

import json
import numpy as np
from init_vars import *
import os
from matplotlib import collections as mc
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import pickle


def read(file, compress=False):
    with open(file) as json_file:
        try:
            data = np.array(json.load(json_file)['people'][0]['pose_keypoints_2d'])
            detection = 1
            data[data == 0] = np.nan
        except:
            detection = 0

        if detection == 1:
            if compress:
                x = np.zeros((25, 3))
                for i in range(0, 3):
                    x[:, i] = data[range(i, 75, 3)]
                if np.isnan(x[openpose_parts['head'], :]).all():
                    x[0, :] = [np.nan, np.nan, np.nan]
                else:
                    x[0, :] = np.nanmean(x[openpose_parts['head'], :], axis=0)
                if np.isnan(x[openpose_parts['right_foot'], :]).all():
                    x[11, :] = [np.nan, np.nan, np.nan]
                else:
                    x[11, :] = np.nanmean(x[openpose_parts['right_foot'], :], axis=0)
                if np.isnan(x[openpose_parts['left_foot'], :]).all():
                    x[14, :] = [np.nan, np.nan, np.nan]
                else:
                    x[14, :] = np.nanmean(x[openpose_parts['left_foot'], :], axis=0)
                return x[0:15, :], detection
            else:
                return data.reshape((25, 3)), detection
        else:
            if compress:
                return np.nan * np.zeros((15, 3)), detection
            else:
                return np.nan * np.zeros((25, 3)), detection


def create_limbs(body):
    graph = [[0, 1], [1, 2], [1, 5], [1, 8], [2, 3], [3, 4],
             [5, 6], [6, 7], [8, 9], [8, 12], [9, 10], [10, 11],
             [12, 13], [13, 14]]
    limbs = []
    for i in graph:
        limbs.append([(body[i[0], 0], body[i[0], 1]), (body[i[1], 0], body[i[1], 1])])
    return limbs


def animation(seq, filename, path=temp_path):
    if filename.find('.avi'):
        filename.replace('avi', '')

    def animationUpdate(k):
        x = seq[:, 0, k]
        y = seq[:, 1, k]
        scat.set_offsets(np.c_[x, y])
        lines = create_limbs(seq[:, :, k])
        lc = mc.LineCollection(lines, linewidths=2, alpha=0.1)
        ax1.add_collection(lc)
        return scat,

    f = plt.figure(figsize=(10, 5))
    min_x = np.nanmin(seq[:, 0, :]).round()
    max_x = np.nanmax(seq[:, 0, :]).round()
    width = max_x - min_x
    min_y = np.nanmin(seq[:, 1, :]).round()
    max_y = np.nanmax(seq[:, 1, :]).round()
    heigth = max_y - min_y
    xlim = (min_x - width*0.2, max_x + width*0.2)
    ylim = (min_y - heigth*0.2, max_y + heigth*0.2)
    ax1 = plt.subplot(111, xlim=xlim, ylim=ylim)
    scat = ax1.scatter(x=seq[:, 0, 0], y=seq[:, 1, 0], s=70)
    lines = create_limbs(seq[:, :, 0])
    lc = mc.LineCollection(lines, linewidths=2, alpha=0.1)
    ax1.add_collection(lc)
    anim = FuncAnimation(f, animationUpdate, frames=seq.shape[2], interval=40, blit=True)
    plt.gca().invert_yaxis()
    plt.title(filename)
    plt.axis('off')
    plt.gca().set_aspect('equal', adjustable='box')
    anim.save(os.path.join(path, filename) + '.gif', writer='pillow')
    print('Saved GIF: {}'.format(os.path.join(path, filename) + '.gif'))


def read_sequence_to_animate(sample, animate_path):
    jsons = os.listdir(sample)
    sequence = np.nan * np.zeros((15, 3, len(jsons)))
    detections = np.nan * np.zeros((len(jsons)))
    frames = np.nan * np.zeros((len(jsons)))
    for i in jsons:
        t = int(i[-27:-15])
        sequence[:, :, t], detections[t] = read(os.path.join(sample, i), compress=True)
        frames[t] = t

    animation(sequence, animate_path, os.path.basename(sample).replace('.avi', ''))

    return sequence, detections, frames


def read_sequence(sample):
    jsons = os.listdir(sample)
    sequence = np.nan * np.zeros((25, 3, len(jsons)))
    detections = np.nan * np.zeros((len(jsons)))
    frames = np.nan * np.zeros((len(jsons)))
    for i in jsons:
        t = int(i[-27:-15])
        sequence[:, :, t], detections[t] = read(os.path.join(sample, i), compress=False)
        frames[t] = t

    return sequence, detections, frames


def save_sequence(seq, det, fra, name, meta, video):
    # save POSE
    to_save = dict(seq=seq,
                   det=det,
                   length=seq.shape[2],
                   frames=fra,
                   name=name,
                   action=meta['action'],
                   dataset=meta['dataset'],
                   actor=meta['actor'],
                   unique_id=meta['unique_id'])
    pickle.dump(to_save, open(os.path.join(paths['pose'], name+'.p'), 'wb'))

    # save RGB
    out = cv2.VideoWriter(os.path.join(paths['rgb'], name+'.avi'),
                          codec,
                          fps[meta['dataset']],
                          frame_size[meta['dataset']])
    for i in fra:
        out.write(video[int(i)])
    out.release()
    print('Saved: {}'.format(name))


def get_meta(sample, is_video=True):
    if is_video:
        res = [i for i in range(len(sample)) if sample.startswith('_', i)]
        return dict(sample=sample,
                    dataset=sample[:res[0]],
                    actor=sample[res[0]+1:res[1]],
                    action=sample[res[1]+1:res[2]],
                    unique_id=sample[res[2]+1:sample.find('.avi')])
    else:
        res = [i for i in range(len(sample)) if sample.startswith('_', i)]
        das = [i for i in range(len(sample)) if sample.startswith('-', i)]
        if das == []:
            das = [len(sample)]
        return dict(sample=sample,
                    dataset=sample[:res[0]],
                    actor=sample[res[0]+1:res[1]],
                    action=sample[res[1]+1:res[2]],
                    window=sample[das[0]+1::])

