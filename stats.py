# dependencies
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations

def desc_plots(sub_list):
    subs = sub_list
    for sub_name in subs:
        sub1_all_lh = np.loadtxt(f'./sub_coords/{sub_name}_all_lh.csv', delimiter=',')
        sub1_all_lh = np.reshape(sub1_all_lh, (int(len(sub1_all_lh)/3),3,-1))
        sub1_all_rh = np.loadtxt(f'./sub_coords/{sub_name}_all_rh.csv', delimiter=',')
        sub1_all_rh = np.reshape(sub1_all_rh, (int(len(sub1_all_rh)/3),3,-1))

        # generate pairwise labels
        label_range = list(range(1,len(sub1_all_rh)+1))
        label_combo = list(combinations(label_range, 2))
        labels=[]
        for i in range(0,len(label_combo)):
            labels.append(str(label_combo[i][0])+'v'+str(label_combo[i][1]))

        f, axs = plt.subplots(1,2,figsize=(12,5),sharey=True)
        labels_lh = []
        diffs_lh = []
        medians_lh = []
        means_lh = []
        stds_lh = []
        for run1, run2 in combinations(sub1_all_lh, 2):

            diff = run1 - run2
            lendiff = np.sqrt(np.sum(diff**2, axis=0))
            medians_lh.append(np.median(lendiff))
            means_lh.append(np.mean(lendiff))
            stds_lh.append(np.std(lendiff))
            diffs_lh.append(lendiff)
            lh_density = sns.kdeplot(lendiff,bw_adjust=0.5, levels=6, clip=(0,6), ax=axs[0])

        diffs_rh = []
        medians_rh = []
        means_rh = []
        stds_rh = []
        for run1, run2 in combinations(sub1_all_rh, 2):
            diff = run1 - run2
            lendiff = np.sqrt(np.sum(diff**2, axis=0))
            diffs_rh.append(lendiff)
            medians_rh.append(np.median(lendiff))
            means_rh.append(np.mean(lendiff))
            stds_rh.append(np.std(lendiff))
            #plt.hist(lendiff, bins=10, alpha=0.2)
            rh_density = sns.kdeplot(lendiff,bw_adjust=0.5, levels=6, clip=(0,6), ax=axs[1])
        axs[0].set_title(f'{sub_name} LH')
        axs[1].set_title(f'{sub_name} RH')
        f.tight_layout()
        f.savefig(f'./plots/{sub_name}_density.png')
        plt.clf()

        hemi_lbl = ['LH', 'RH']
        plt.scatter(labels, medians_lh)
        plt.scatter(labels, medians_rh, color='red')
        plt.legend(hemi_lbl)
        plt.ylim([0, 1.2])
        plt.ylabel("median d (mm)")
        plt.title(f'{sub_name}')
        plt.savefig(f'./plots/{sub_name}_scatter_median.png')
        plt.clf()

        f, axs = plt.subplots(1,2,figsize=(12,5),sharey=True)
        count_over_5_lh= []
        count_over_5_rh= []
        for i in range(0,len(diffs_rh)):
            count_over_5_lh.append(len(np.where(diffs_lh[i]>5)[0]))
            count_over_5_rh.append(len(np.where(diffs_rh[i]>5)[0]))
        m_count_over_5_lh = np.mean(count_over_5_lh)
        m_count_over_5_rh = np.mean(count_over_5_rh)
        perc_over_5_lh = m_count_over_5_lh / np.count_nonzero(diffs_lh[0])
        perc_over_5_rh = m_count_over_5_rh / np.count_nonzero(diffs_rh[0])
        perc_over_5_lh
        perc_over_5_rh

        violh = sns.violinplot(data=diffs_lh, linewidth=0.2, ax=axs[0])
        axs[0].set_xticklabels(labels)
        axs[0].axhline(5, color='red', lw=0.7, ls='-')
        axs[0].text(1, 5.5, f'{round(perc_over_5_lh,3)}%', color='red')
        axs[0].set_title(f'{sub_name} LH')

        viorh = sns.violinplot(data=diffs_rh, linewidth=0.2, ax=axs[1])
        axs[1].set_xticklabels(labels)
        axs[1].axhline(5, color='red', lw=0.7, ls='-')
        axs[1].text(1, 5.5, f'{round(perc_over_5_rh,3)}%', color='red')
        axs[1].set_title(f'{sub_name} RH')

        f.tight_layout()
        plt.savefig(f'./plots/{sub_name}_violin.png')
        plt.clf()
        print(f'{sub_name} done!')
    print('finished')