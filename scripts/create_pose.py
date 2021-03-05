from init_vars import *
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


jsons = os.listdir(paths['json'])
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

