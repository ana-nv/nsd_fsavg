# dependencies
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations

def vertex_eudist(snum, sub_coords_path='../sub_coords'):
    '''
    Calculates euclidean distance between the xyz vertex positions in pairwise run comparisons for a given subject.
    Returns two numpy arrays for the subject (left and right hemi) with each pairwise difference in d (mm) and a list of pairwise labels
    Parameters:
    snum: int, subject number
    Optional:
    sub_coords_path: str (default: '../sub_coords'), path containing files with subject vertex coordinates (in fsaverage space)
    '''
    # load and reshape the data
    sub_name = 'subj0'+ str(snum) + '_all_'
    sub_all_lh = np.loadtxt(os.path.join(sub_coords_path, f'{sub_name}lh.csv'), delimiter=',')
    sub_all_lh = np.reshape(sub_all_lh, (int(len(sub_all_lh)/3),3,-1))
    sub_all_rh = np.loadtxt(os.path.join(sub_coords_path, f'{sub_name}rh.csv'), delimiter=',')
    sub_all_rh = np.reshape(sub_all_rh, (int(len(sub_all_rh)/3),3,-1))
    
    # calculate distance
    diffs_lh = []
    for run1, run2 in combinations(sub_all_lh, 2):
        diff = run1 - run2
        lendiff = np.sqrt(np.sum(diff**2, axis=0))
        diffs_lh.append(lendiff)

    diffs_rh = []
    for run1, run2 in combinations(sub_all_rh, 2):
        diff = run1 - run2
        lendiff = np.sqrt(np.sum(diff**2, axis=0))
        diffs_rh.append(lendiff)
    
    # generate pairwise labels
    label_range = list(range(1,len(sub_all_lh)+1))
    label_combo = list(combinations(label_range, 2))
    labels=[]
    for i in range(0,len(label_combo)):
        labels.append(str(label_combo[i][0])+'v'+str(label_combo[i][1]))

                         
    return diffs_lh, diffs_rh, labels