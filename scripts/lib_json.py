import json
import numpy as np
from init_vars import *
import os
from matplotlib import collections as mc
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import pickle


def read(file):
    with open(file) as json_file:
        data = np.array(json.load(json_file)['people'][0]['pose_keypoints_2d'])
        if isinstance(data, list):
            detection = 0
            return np.nan * np.zeros((15, 3)), detection
        else:
            detection = 1
            data[data == 0] = np.nan
            x = np.zeros((25, 3))
            for i in range(0, 3):
                x[:, i] = data[range(i, 75, 3)]
            x[0, :] = np.nanmean(x[openpose_parts['head'], :], axis=0)
            x[11, :] = np.nanmean(x[openpose_parts['right_foot'], :], axis=0)
            x[14, :] = np.nanmean(x[openpose_parts['left_foot'], :], axis=0)
            return x[0:15, :], detection


def create_limbs(body):
    graph = [[0, 1], [1, 2], [1, 5], [1, 8], [2, 3], [3, 4],
             [5, 6], [6, 7], [8, 9], [8, 12], [9, 10], [10, 11],
             [12, 13], [13, 14]]
    limbs = []
    for i in graph:
        limbs.append([(body[i[0], 0], body[i[0], 1]), (body[i[1], 0], body[i[1], 1])])
    return limbs


def animation(seq, path, filename):

    def animationUpdate(k):
        x = seq[:, 0, k]
        y = seq[:, 1, k]
        scat.set_offsets(np.c_[x, y])
        lines = create_limbs(seq[:, :, k])
        lc = mc.LineCollection(lines, linewidths=2, alpha=0.1)
        ax1.add_collection(lc)
        return scat,

    f = plt.figure(figsize=(10, 5))
    min_x = seq[:, 0, :].min().round()
    max_x = seq[:, 0, :].max().round()
    width = max_x - min_x
    min_y = seq[:, 1, :].min().round()
    max_y = seq[:, 1, :].max().round()
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


def read_sequence(sample, animate_path=None):
    jsons = os.listdir(sample)
    sequence = np.nan * np.zeros((15, 3, len(jsons)))
    detections = np.nan * np.zeros((len(jsons)))
    frames = np.nan * np.zeros((len(jsons)))
    for i in jsons:
        t = int(i[-27:-15])
        sequence[:, :, t], detections[t] = read(os.path.join(sample, i))
        frames[t] = t

    if animate_path is not None:
        animation(sequence, animate_path, os.path.basename(sample).replace('.avi', ''))

    return sequence, detections, frames


def save_sequence(seq, det, fra, sample, name, path=paths['pose']):
    to_save = dict(seq=seq, det=det, length=seq.shape[2], frames=fra, sample=sample)
    to_save.update(get_meta(sample))
    pickle.dump(to_save, open(os.path.join(path, name+'.p'), 'wb'))


def get_meta(sample):
    res = [i for i in range(len(sample)) if sample.startswith('_', i)]
    return dict(sample=sample,
                dataset=sample[:res[0]],
                actor=sample[res[0] + 1:res[1]],
                unique_id=sample[res[1] + 1:res[2]])


if __name__ == '__main__':
    sample = paths['json'] + 'i3dpost_chris_bend_177.avi'
    seq, det, frames = read_sequence(sample)
    save_sequence(seq=seq, det=det, sample=os.path.basename(sample))
