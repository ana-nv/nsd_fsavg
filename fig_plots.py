# dependencies
import os
import neuropythy as ny
import numpy as np
import matplotlib.pyplot as plt
import ipyvolume as ipv

def plot_submesh_diff(snum, reppair, hemi, thresh, sub_coords_path='./sub_coords', fsa_path='../fsaverage', view=None):
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
    sub_coords_path: str (default: './sub_coords'), path containing files with subject vertex coordinates (in fsaverage space)
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