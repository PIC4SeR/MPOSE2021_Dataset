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
import os
import scripts.lib_seq as ls
import numpy as np

# remove empty frames at the beginning and at the end
def trim_seq(s, d, f):
    if d[0] == 0:
        start = next(i for i, obj in enumerate(d) if obj == 1)
    else:
        start = 0
    if d[-1] == 0:
        end = -1-next(i for i, obj in enumerate(d[::-1]) if obj == 1)
        return s[:, :, start:end], d[start:end], f[start:end]
    else:
        return s[:, :, start:], d[start:], f[start:]

# split sequence in parts with min_frame_length >= frames >= max_frame_length
def split_seq(s, d, f, meta, video, trim=True):
    if trim:
        s, d, f = trim_seq(s, d, f)
    s = s[:, :, d == 1]
    frames = f[d == 1]
    for count, start in enumerate(range(0, s.shape[2], max_frame_length)):
        sub_s = s[:, :, start:start+max_frame_length]
        fra = frames[start:start + max_frame_length]
        if sub_s.shape[2] >= min_frame_length:
            name = '{}-{}-{}'.format(meta['sample'].replace('.avi', ''),
                                                    int(fra[0]),
                                                    int(fra[-1]))
            ls.save_sequence(seq=sub_s,
                             det=np.ones((sub_s.shape[2])),
                             fra=fra,
                             name=name,
                             meta=meta,
                             video=video)

def read_video(path):
    vidcap = cv2.VideoCapture(path)
    success, image = vidcap.read()
    frames = []
    while success:
        frames.append(image)
        success, image = vidcap.read()
    vidcap.release()
    cv2.destroyAllWindows()
    return frames

def create_rgb_pose():
    jsons = os.listdir(paths['json'])
    for i in jsons:
        meta = ls.get_meta(i)
        video = read_video(os.path.join(paths['video'], i))
        seq, det, fra = ls.read_sequence(paths['json'] + i)
        split_seq(s=seq, d=det, f=fra, meta=meta, video=video)

if __name__ == '__main__':
    create_rgb_pose()