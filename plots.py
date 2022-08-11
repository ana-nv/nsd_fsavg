# dependencies
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from stats import vertex_eudist

sns.set(style='white')

def desc_plots(sub_list, nsd_dir):
    subs = sub_list
    
    for snum in subs:
        sub_name = 'subj0'+ str(snum)
        diffs_lh, diffs_rh, labels = vertex_eudist(snum)

        medians_lh = np.median(diffs_lh, axis=1)
        means_lh = np.mean(diffs_lh, axis=1)
        stds_lh = np.std(diffs_lh, axis=1)
        
        medians_rh = np.median(diffs_rh, axis=1)
        means_rh = np.mean(diffs_rh, axis=1)
        stds_rh = np.std(diffs_rh, axis=1)
        
        if not os.path.exists('plots'):
            os. makedirs('plots')
        # kde plots
        f, axs = plt.subplots(1,2,figsize=(12,5),sharey=True)
        for pair in diffs_rh:
            lh_density = sns.kdeplot(pair,bw_adjust=0.5, levels=6, clip=(0,6), ax=axs[0])
        for pair in diffs_rh:
            rh_density = sns.kdeplot(pair,bw_adjust=0.5, levels=6, clip=(0,6), ax=axs[1])
        if not os.path.exists('plots/kde'):
            os. makedirs('plots/kde')
        axs[0].set_xlabel('d (mm)')
        axs[1].set_xlabel('d (mm)')
        axs[0].set_title(f'{sub_name} LH')
        axs[1].set_title(f'{sub_name} RH')
        f.tight_layout()
        f.savefig(f'./plots/kde/{sub_name}_density.png')
        plt.close()
        
        # scatter plots
        if not os.path.exists('plots/scatter_median'):
            os. makedirs('plots/scatter_median')
        hemi_lbl = ['LH', 'RH']
        plt.scatter(labels, medians_lh)
        plt.scatter(labels, medians_rh, color='red')
        plt.legend(hemi_lbl)
        plt.ylim([0, 1.2])
        plt.ylabel("median d (mm)")
        plt.title(f'{sub_name}')
        if snum == 2: # too many pairs
            plt.xticks(rotation=90)

        plt.savefig(f'./plots/scatter_median/{sub_name}_scatter_median.png', facecolor='white')
        plt.close()
        
        # violin plots
        if not os.path.exists('plots/violin'):
            os. makedirs('plots/violin')
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

        violh = sns.violinplot(data=diffs_lh, linewidth=0.2, ax=axs[0])
        axs[0].axhline(5, color='red', lw=0.7, ls='-')
        axs[0].text(1, 5.5, f'{round(perc_over_5_lh,3)}%', color='red')
        axs[0].set_title(f'{sub_name} LH')

        viorh = sns.violinplot(data=diffs_rh, linewidth=0.2, ax=axs[1])
        axs[1].axhline(5, color='red', lw=0.7, ls='-')
        axs[1].text(1, 5.5, f'{round(perc_over_5_rh,3)}%', color='red')
        axs[1].set_title(f'{sub_name} RH')
        if snum == 2: # too many pairs
            axs[0].set_xticklabels(labels, rotation=90)
            axs[1].set_xticklabels(labels, rotation=90)
        else:
            axs[1].set_xticklabels(labels)
            axs[0].set_xticklabels(labels)
        f.tight_layout()
        plt.savefig(f'./plots/violin/{sub_name}_violin.png')
        plt.close()
        print(f'{sub_name} done!')
    print('finished')