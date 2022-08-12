import os
import neuropythy as ny
import numpy as np
from glob import glob

def sub_coords_extract(sublist, nsd_dir='../nsddata_other/freesurferoriginals'):
    for snum in sublist:
        print(f'subject {snum} started')
        sub_name = 'subj0'+ str(snum) + '_rep'
        fsa_coords_lh = np.loadtxt('./fsa_coords_lh.csv', delimiter=',')
        fsa_coords_rh = np.loadtxt('./fsa_coords_rh.csv', delimiter=',')
        sub_all_lh = None
        sub_all_rh = None
        
        for rep in glob(os.path.join(nsd_dir, f'{sub_name}*')):
                sub = ny.freesurfer_subject(os.path.join(nsd_dir, rep))
                sub_sphere_lh = sub.lh.surface('fsaverage')
                sub_addresses_lh = sub_sphere_lh.address(fsa_coords_lh)
                sub_unaddresses_lh = sub.lh.surface('white').unaddress(sub_addresses_lh)
                if sub_all_lh is None:
                    sub_all_lh = sub_unaddresses_lh
                else:
                    sub_all_lh = np.append(sub_all_lh, np.array(sub_unaddresses_lh), axis=0)
                del sub_sphere_lh, sub_addresses_lh, sub_unaddresses_lh
                print("lh done")              
                
                sub_sphere_rh = sub.rh.surface('fsaverage')
                sub_addresses_rh = sub_sphere_rh.address(fsa_coords_rh)
                sub_unaddresses_rh = sub.rh.surface('white').unaddress(sub_addresses_rh)
                if sub_all_rh is None:
                    sub_all_rh = sub_unaddresses_rh
                else:
                    sub_all_rh = np.append(sub_all_rh, np.array(sub_unaddresses_rh), axis=0)
                del sub, sub_sphere_rh, sub_addresses_rh, sub_unaddresses_rh
                print("rh done")

                ny.freesurfer.forget_subject(os.path.join(nsd_dir, rep))
                
        np.savetxt(os.path.join('../sub_coords', f'subj0{snum}_all_lh.csv'), sub_all_lh, delimiter=',')
        np.savetxt(os.path.join('../sub_coords', f'subj0{snum}_all_rh.csv'), sub_all_rh, delimiter=',')
        print(f'all subject {snum} runs done')

        
def fsa_coords_extract(fsa_path='../fsaverage'):
        # source path of fsaverage data
        fsa = ny.freesurfer_subject(fsa_path)
        
        fsa_sphere_lh = fsa.lh.surface('sphere')
        fsa_coords_lh = fsa_sphere_lh.coordinates
        fsa_mesh_lh = fsa.lh.surface('sphere').copy(coordinates=fsa_coords_lh)

        fsa_sphere_rh = fsa.rh.surface('sphere')
        fsa_coords_rh = fsa_sphere_rh.coordinates
        fsa_mesh_rh = fsa.rh.surface('sphere').copy(coordinates=fsa_coords_rh)
        
        np.savetxt("./fsa_coords/fsa_coords_lh.csv", fsa_coords_lh, delimiter=",")
        np.savetxt("./fsa_coords/fsa_coords_rh.csv", fsa_coords_rh, delimiter=",")
