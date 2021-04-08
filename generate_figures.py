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

import seaborn as sns
import matplotlib.pyplot as plt
from create_splits import *
import sys


if __name__ == '__main__':

    print('Reading openpose sequences...')
    report = read_poses()
    report['detector'] = 'openpose'

    actions = report.action.drop_duplicates().sort_values()
    actors = report.actor.drop_duplicates()

    palette = sns.color_palette("Spectral", len(actions))

    fig = plt.figure(figsize=(15, 10))
    df_plot = report.groupby(['dataset', 'action']).size().reset_index().pivot(columns='dataset', index='action', values=0)
    df_plot.plot(kind='bar', stacked=True)
    plt.title('MPOSE2021 ({} actions, {} actors, {} samples)'.format(len(actions),
                                                                     len(actors),
                                                                     len(report)))
    plt.xticks(rotation=90)
    plt.ylabel('samples')
    plt.tight_layout()
    plt.savefig(os.path.join(paths['figures'], 'mpose2021_summary.pdf'))

    for split_id in range(1, 4):
        fig, axs = plt.subplots(2,1, figsize=(10, 10))
        axs[0] = sns.countplot(x="action", data=report.loc[~report.actor.isin(testing_actors[split_id])],
                               order=actions, ax=axs[0], palette=palette)
        axs[0].tick_params(labelrotation=45)
        axs[0].set_title('Split{} - Training Data Summary'.format(split_id))
        axs[1] = sns.countplot(x="action", data=report.loc[report.actor.isin(testing_actors[split_id])],
                               order=actions, ax=axs[1], palette=palette)
        axs[1].tick_params(labelrotation=45)
        axs[1].set_title('Split{} - Testing Data Summary'.format(split_id))
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(os.path.join(paths['figures'], 'split{}_summary.pdf'.format(split_id)))

    print('Reading posenet sequences...')
    report_posenet = read_poses(paths['posenet'])
    report_posenet['detector'] = 'posenet'
    report_tot = report.append(report_posenet)

    fig = plt.figure(figsize=(10, 5))
    palette = sns.color_palette()
    sns.boxplot(x="dataset", y="aver_conf", data=report_tot, palette=palette, hue='detector')
    plt.title('Sequence Averaged Detection Confidence (POSE)')
    plt.tight_layout()
    plt.savefig(os.path.join(paths['figures'], 'averaged_confidence.pdf'))

    fig = plt.figure(figsize=(10, 5))
    palette = sns.color_palette()
    sns.boxplot(x="dataset", y="fn%", data=report_tot, palette=palette, hue='detector')
    plt.title('Sequence false negative percentage')
    plt.ylabel('False Negative (%)')
    plt.tight_layout()
    plt.savefig(os.path.join(paths['figures'], 'fn_percentage.pdf'))
