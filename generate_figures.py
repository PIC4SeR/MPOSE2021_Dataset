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


if __name__ == '__main__':
    report = read_poses()
    actions = report.action.drop_duplicates().sort_values()

    palette = sns.color_palette("Spectral", len(actions))

    fig = plt.figure(figsize=(10, 5))
    sns.countplot(x="action",
                  data=report,
                  order=actions,
                  palette=palette)
    plt.title('MPOSE2021 Summary')
    plt.xticks(rotation=90)
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

    fig = plt.figure(figsize=(10, 5))
    palette = sns.color_palette("Spectral", len(report.dataset.drop_duplicates()))
    sns.boxplot(x="dataset", y="aver_conf", data=report, palette=palette)
    plt.title('Sequence Averaged Detection Confidence (POSE)')
    plt.tight_layout()
    plt.savefig(os.path.join(paths['figures'], 'averaged_confidence.pdf'))
