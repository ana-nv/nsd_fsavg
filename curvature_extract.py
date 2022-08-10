# dependencies
import os
import neuropythy as ny
import numpy as np
from glob import glob

def sub_curv_extract(sub_list, fsa_dir, nsd_dir):
    '''
    sub_curv_extract() interpolates curvatures of all runs for both hemispheres for the given list of subjects to freesurfer anatomy and saves each interpolated curvature in a separate .csv file.
    Args:
    sub_list: list of integers representing subject number
    fsa: location of fsaverage freesurfer directory
    nsd_dir: location of nsd freesurfer original directory that contains all original freesurfer outputs for all runs in all 8 subjects
    '''
    fsa = ny.freesurfer_subject(fsa_dir)
    subs = sub_list
    for snum in subs:
        sub_name = 'subj0'+ str(snum) + '_rep'
        
        # loop through subject runs      
        for rep in glob(os.path.join(nsd_dir, f'{sub_name}*')):
            rep_num = glob(os.path.join(nsd_dir, f'{sub_name}*')).index(rep)+1
            print(f'subject {snum} rep {rep_num} started')
            # load fs subject
            sub = ny.freesurfer_subject(rep)

            curv_lh = sub.lh.interpolate(fsa.rh, 'curvature')
            curv_rh = sub.rh.interpolate(fsa.rh, 'curvature')
            
            # save to file
            if not os.path.exists('sub_curvatures'):
                os. makedirs('sub_curvatures')
            np.savetxt(os.path.join('./sub_curvatures', f'{sub_name}_0{str(rep_num)}_lh.csv'), curv_lh, delimiter=',')
            np.savetxt(os.path.join('./sub_curvatures', f'{sub_name}_0{str(rep_num)}_rh.csv'), curv_rh, delimiter=',')

            # remove fs subject from cache
            ny.freesurfer.forget_subject(rep)

        print(f'subject {snum} curvatures calculated and saved for all runs')
        # remove fsa from cache
        ny.freesurfer.forget_subject(fsa_dir)