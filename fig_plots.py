# dependencies
import os
from glob import glob
import neuropythy as ny
import numpy as np
import matplotlib.pyplot as plt
import ipyvolume as ipv
from itertools import combinations

def plot_submesh_diff(snum, reppair, hemi, thresh, sub_coords_path='../sub_coords', fsa_path='../fsaverage', view=None):
    '''
    Calculates the difference submeshes between two given mesh objects in fsaverage space, 
    plots the two submeshes together with the mesh of the first rep and returns an ipyvolume figure.
    The difference submeshes are made out of those vertices that differ more than a given threshold (mm) between the reps.
    If there are no vertices with difference greater than the given threshold, no figure will be created.
    Parameters:
    snum: int, subject number
    reppair: list, reps to be compared
    hemi: str, which hemisphere ('lh' or 'rh')
    thresh: int, vertices with rep difference over thresh value are used to create submeshes
    Optional parameters:
    view: str (default: None), camera view for plotting. If None, it will default to a lateral view ('right' for right hemisphere and 'left' for left hemisphere). Possible views: 'front', 'back', 'rear', 'posterior', 'anterior', 'top', 'bottom', 'inferior', 'superior', 'right', 'left'.
    sub_coords_path: str (default: '../sub_coords'), path containing files with subject vertex coordinates (in fsaverage space)
    fsa_path: str (default: '../fsaverage'), fsaverage directory path (needed to create meshes)
    '''
    # load coordinates for both reps
    sub_all = np.loadtxt(os.path.join(sub_coords_path, f'subj0{str(snum)}_all_{hemi}.csv'), delimiter=',')
    sub_all = np.reshape(sub_all, (int(len(sub_all)/3),3,-1))
    r1_coords = sub_all[reppair[0]-1]
    r2_coords = sub_all[reppair[1]-1]
    # calculate euclidean distance for each vertex pai
    diff = r1_coords - r2_coords
    lendiff = np.sqrt(np.sum(diff**2, axis=0))
    # generate mask for vertices with difference above given threshold
    r1r2_mask = np.where(lendiff>10)[0]
    # check if the mask is empty
    if r1r2_mask.size == 0:
        return print(f'No differences greater than {thresh} mm, nothing to plot.')
    else:
        # load fsaverage subject to make rep-specific surface meshes
        fsa = ny.freesurfer_subject(fsa_path)
        if hemi == 'lh':
            fsa1_mesh = fsa.lh.surface('inflated').copy(coordinates=r1_coords)
            fsa2_mesh = fsa.lh.surface('inflated').copy(coordinates=r2_coords)
            if view is None:
                view = 'left'
        elif hemi == 'rh':
            fsa1_mesh = fsa.rh.surface('inflated').copy(coordinates=r1_coords)
            fsa2_mesh = fsa.rh.surface('inflated').copy(coordinates=r2_coords)
            if view is None:
                view = 'right'

        # submesh of mask relative to run 1
        submesh12_on1 = fsa1_mesh.submesh(r1r2_mask)
        # submesh of mask relative to run 2
        submesh12_on2 = fsa2_mesh.submesh(r1r2_mask)
        
        # plot and return the figure
        f = ipv.figure(height=2048, width=2048)
        ny.cortex_plot(submesh12_on1, figure=f, color="orange", alpha=0.5)
        ny.cortex_plot(submesh12_on2, figure=f, color="red")
        ny.cortex_plot(fsa1_mesh, mesh_alpha=0.5, figure=f, color='white', alpha=0.5, camera_fov=0.6, view=view)
        return ipv.show()
    
    
def plot_gray_diff(sub_list, hemi, slices, nsd_dir='../nsddata_other/freesurferoriginals'):
    '''
    Iterates over all subjects and pairwise runs. Loads gray mask images in pairs and calculates the difference between two given images, then plots all three and saves into a .png file. 
    plots the difference as an overlay on an inflated fsaverage surface and returns an ipyvolume figure.
    Parameters:
    sub_list: list, subjects (1 to 8)
    hemi: str, which hemisphere ('lh' or 'rh')
    slices: list, how to slice image for plotting
    Optional parameters:
    nsd_dir: str (default:'../nsddata_other/freesurferoriginals'), subject freesurfer location
    '''
    # loop through subjects
    for snum in sub_list:
        # go through all pairwise combinations
        rep_files = glob(os.path.join(nsd_dir, f'subj0{snum}_rep0*'))
        
        # generate pairwise labels
        label_range = list(range(1,len(rep_files)+1))
        label_combo = list(combinations(label_range, 2))
        labels=[]
        for i in range(0,len(label_combo)):
            labels.append(str(label_combo[i][0])+'v'+str(label_combo[i][1]))
        c = 0
        for rep1, rep2 in combinations(rep_files, 2):
            # load reps
            sub1 = ny.freesurfer_subject(rep1)
            sub2 = ny.freesurfer_subject(rep2)
            # get gray masks
            mgh1= sub1.images[f'{hemi}_gray_mask']
            mgh2 = sub2.images[f'{hemi}_gray_mask']
            slice1 = mgh1.get_fdata()[slices]
            slice2 = mgh2.get_fdata()[slices]
            slice12diff = slice1-slice2

            # plot gray mask differences
            if not os.path.exists('plots'):
                os.makedirs('plots')
            if not os.path.exists('plots/graymask_diffs'):
                os.makedirs('plots/graymask_diffs')
            f, axs = plt.subplots(1,3,figsize=(12,5), sharey=True)
            axs[0].imshow(slice1.T)
            axs[1].imshow(np.abs(slice12diff.T))
            axs[2].imshow(slice2.T)
            axs[0].title.set_text(f'rep{str(label_combo[c][0])}')
            axs[1].title.set_text(f'Subject {snum} ({hemi}), rep diff')
            axs[2].title.set_text(f'rep{str(label_combo[c][1])}')
            f.tight_layout()
            f.savefig(f'./plots/graymask_diffs/{snum}_{hemi}_{labels[c]}.png', facecolor='white')
            plt.close()
            c +=1
            # remove reps from cache
            ny.freesurfer.forget_subject(rep1)
            ny.freesurfer.forget_subject(rep2)
        print(f'subject {snum} finished')
        
        
def plot_curv_diff(snum, reps, hemi, sub_curv_path='./sub_curvatures', fsa_path='../fsaverage', view=None):
    '''
    Calculates the curvature difference between two given runs for the given subject number, 
    plots the difference as an overlay on an inflated fsaverage surface and returns an ipyvolume figure.
    The difference is taken from previously extracted curvature values via sub_curv_extract() from curvature_extract.py.
    Parameters:
    snum: int, subject number
    reps: list, reps to be compared
    hemi: str, which hemisphere ('lh' or 'rh')
    Optional parameters:
    sub_curv_path: str (default: './sub_curvatures'), path containing files with curvature values
    fsa_path: str (default: '../fsaverage'), fsaverage directory path (needed to plot onto)
    view: str (default: None), camera view for plotting. If None, it will default to a lateral view ('right' for right hemisphere and 'left' for left hemisphere). Possible views: 'front', 'back', 'rear', 'posterior', 'anterior', 'top', 'bottom', 'inferior', 'superior', 'right', 'left'.
    '''
    # load fsaverage subject for plotting
    fsa = ny.freesurfer_subject(fsa_path)    
    # load curvatures
    curv1 = np.loadtxt(os.path.join(sub_curv_path, f'subj0{str(snum)}_rep_0{str(reps[0])}_{hemi}.csv'), delimiter=',')
    curv2 = np.loadtxt(os.path.join(sub_curv_path, f'subj0{str(snum)}_rep_0{str(reps[1])}_{hemi}.csv'), delimiter=',')
    curvdiff = curv1 - curv2
    f = ipv.figure(height=2048, width=2048)
    if hemi == 'lh':
        view='left'
        f = ny.cortex_plot(fsa.lh.surface('inflated'), figure=f, underlay=None,color=np.abs(curvdiff), cmap="jet", vmax=0.2, vmin=0, view=view)
    else:
        view='right'
        f = ny.cortex_plot(fsa.rh.surface('inflated'), figure=f, underlay=None,color=np.abs(curvdiff), cmap="jet", vmax=0.2, vmin=0, view=view)
    return ipv.show()