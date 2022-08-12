# dependencies
import os
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from itertools import combinations
from stats_helper import vertex_eudist

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
    
    
def curv_diff_plots(sub_list, sub_curv_path='./sub_curvatures'):
    '''
    Plot differences in curvature for each run combination within a subject for a given subject list.
    Uses interpolated curvature values obtained via sub_curv_extract() from curvature_extract.py
    Parameters:
    sub_list: list, contains integers of subjects to loop through (1 to 8)
    Optional:
    sub_curv_path: str, (default: './sub_curvatures'), path containing files with subject curvature values
    '''
    subs = sub_list
    for snum in subs:
        print(f'subject {snum} plotting started')
        # load curvatures
        run_list_lh = glob(os.path.join(sub_curv_path, f'subj0{snum}*lh.csv'))
        run_list_rh = glob(os.path.join(sub_curv_path, f'subj0{snum}*rh.csv'))
        # generate pairwise labels
        label_range = list(range(1,len(run_list_lh)+1))
        label_combo = list(combinations(label_range, 2))
        labels=[]
        for i in range(0,len(label_combo)):
            labels.append(str(label_combo[i][0])+'v'+str(label_combo[i][1]))
        c = 0
        
        # left hemi
        for run1, run2 in combinations(run_list_lh, 2):
            # fetch run names
            run1_name = 'run'+labels[c][0]
            run2_name = 'run'+labels[c][2]
            #load curvatures
            curv1_lh = np.loadtxt(run1)
            curv2_lh = np.loadtxt(run2)
            r, p = stats.pearsonr(curv1_lh, curv2_lh)

            # save plot
            if not os.path.exists('curv_diff_plots'):
                os. makedirs('curv_diff_plots')
            g = sns.jointplot(x=curv1_lh,y=curv2_lh, kind="reg")
            g.set_axis_labels(run1_name, run2_name)
            plt.suptitle(f'subj0{snum} LH')
            regline = g.ax_joint.get_lines()[0]
            regline.set_color('red')
            regline.set_zorder(5)
            g.ax_marg_x.set_xlim(-3, 3)
            g.ax_marg_y.set_ylim(-3, 3)
            g.ax_joint.annotate(f'$\\rho = {r:.3f}, p = {p:.3f}$', xy=(-2, 2))
            g.savefig(f'./curv_diff_plots/subj0{snum}_{labels[c]}_lh.png')
            plt.close()
            c += 1
        # right hemi
        c = 0
        for run1, run2 in combinations(run_list_rh, 2):
            # fetch run names
            run1_name = 'run'+labels[c][0]
            run2_name = 'run'+labels[c][2]
            #load curvatures
            curv1_rh = np.loadtxt(run1)
            curv2_rh = np.loadtxt(run2)
            r, p = stats.pearsonr(curv1_rh, curv2_rh)

            # save plot
            if not os.path.exists('curv_diff_plots'):
                os. makedirs('curv_diff_plots')
            g = sns.jointplot(x=curv1_rh,y=curv2_rh, kind="reg")
            g.set_axis_labels(run1_name, run2_name)
            plt.suptitle(f'subj0{snum} RH')
            regline = g.ax_joint.get_lines()[0]
            regline.set_color('red')
            regline.set_zorder(5)
            g.ax_marg_x.set_xlim(-3, 3)
            g.ax_marg_y.set_ylim(-3, 3)
            g.ax_joint.annotate(f'$\\rho = {r:.3f}, p = {p:.3f}$', xy=(-2, 2))
            g.savefig(f'./curv_diff_plots/subj0{snum}_{labels[c]}_rh.png')
            plt.close()
            c += 1
    print(f'all subjsects plotting finished')