from init_vars import *
import os
import scripts.lib_json as lj
import numpy as np

verbose = True


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
def split_seq(s, d, f, action, trim=True, verbose=verbose):
    if trim:
        s, d, f, = trim_seq(s, d, f)
    s = s[:, :, d == 1]
    frames = f[d == 1]
    for count, start in enumerate(range(0, s.shape[2], max_frame_length)):
        sub_s = s[:, :, start:start+max_frame_length]
        fra = frames[start:start + max_frame_length]
        if sub_s.shape[2] >= min_frame_length:
            lj.save_sequence(seq=sub_s,
                             det=np.ones((sub_s.shape[2])),
                             fra=fra,
                             sample=i,
                             name='{}-{}-{}'.format(i, int(fra[0]), int(fra[-1])),
                             action=action)
            if verbose:
                print('Saved: {}-{}-{}'.format(i, int(fra[0]), int(fra[-1])))


if __name__ == '__main__':
    jsons = os.listdir(paths['json'])
    for i in jsons:
        meta = lj.get_meta(i)
        if meta['dataset'] == 'isldas':
            seq, det, fra = lj.read_sequence(paths['json'] + i)
            if det.sum() >= min_frame_length:
                lj.save_sequence(seq=seq,
                                 det=det,
                                 fra=fra,
                                 sample=i,
                                 name=i,
                                 action=meta['action'])
                if verbose:
                    print('Saved: {}'.format(i))
        else:
            seq, det, fra = lj.read_sequence(paths['json'] + i)
            split_seq(s=seq, d=det, f=fra, action=meta['action'])


