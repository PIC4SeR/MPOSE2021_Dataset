from init_vars import *
import os
import scripts.lib_json as lj
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

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
def split_seq(s, d, f, label, trim=True, verbose=verbose):
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
                             label=meta['action'])
            if verbose:
                print('Saved: {}-{}-{}'.format(i, int(fra[0]), int(fra[-1])))


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
                             label=meta['action'])

    else:
        seq, det, fra = lj.read_sequence(paths['json'] + i)
        split_seq(s=seq, d=det, f=fra, label=meta['action'])

'''
report = pd.DataFrame(columns=['sample', 'dataset', 'num_frames', 'aver_conf'])
poses = dict()
for s, sample in enumerate(jsons):
    print(s, sample)
    pose = np.zeros((25, 3, max_frame_length))
    for i, file in enumerate(os.listdir(os.path.join(paths['json'], sample))):
        t = int(file[-27:-15])
        with open(os.path.join(paths['json'], sample, file)) as f:
            data = json.load(f)
        for entry in range(0, 3):
            try:
                pose[:, entry, t] = np.array(data['people'][0]['pose_keypoints_2d'])[range(entry, 75, 3)]
            except:
                pose[:, entry, t] = np.nan * np.zeros((1, 25))
    conf = np.nanmean(pose[:, 2, :], axis=0)
    num_frames = max_frame_length - np.isnan(conf).sum()
    report = report.append({'sample': sample,
                            'dataset': sample[0:sample.find('_')],
                            'num_frames': num_frames,
                            'aver_conf': np.nanmean(conf)}, ignore_index=True)
    poses[sample] = pose

num = []
report.groupby('dataset').median('aver_conf')
for dataset in report['dataset'].unique():
    num.append((report.loc[report['dataset'] == dataset, 'aver_conf'] > min_conf_threshold).sum())
    print(dataset, num[-1], (report['dataset'] == dataset).sum())
np.sum(num)

plt.figure()
ax = sns.boxplot(x="dataset", y="aver_conf", data=report, whis=np.inf)
#ax = sns.stripplot(x="dataset", y="aver_conf", data=report)
plt.savefig('report_aver_conf.png')
plt.show()

plt.figure()
ax = sns.stripplot(x="dataset", y="num_frames", data=report)
plt.savefig('report_frame_num.png')
plt.show()
'''
