# NSD fsavg

**Name**: nsdfsavg\
**Project url(s)**: [Github Repo](https://github.com/ana-nv/nsd_fsavg), [OSF Storage](https://osf.io/t6fph/?view_only=e5428abd0da84b4f92e89bbf30bd26aa), [Presentation Slides](https://osf.io/j7zkw?view_only=e5428abd0da84b4f92e89bbf30bd26aa)\
**Contributors**: [Ana Arsenovic](https://github.com/ana-nv)\
**Description of project**: The goal of this project is to investigate the reliability of Freesurfer outputs in individual subjects in the Natural Scenes Dataset (NSD; [Allen et al., 2022](https://doi.org/10.1038/s41593-021-00962-x)). The dataset contains in total 8 subjects with multiple 0.8 mm T1 acquisitions each (ranging from 4 to 10). NSD Data Manual is available [here](https://cvnlab.slite.com/p/CT9Fwl4_hc/NSD-Data-Manual).\
**How to get involved**: Post an issue or submit a PR.

### How to obtain the data:
**NSD**\
Follow the instructions given [here](https://cvnlab.slite.page/p/dC~rBTjqjb/How-to-get-the-data).\
**fsaverage**\
There are many packages that contain fsaverage files. For example:
```
import neuropythy as ny
subs = ny.data['benson_winawer_2018'].subjects
```

### How to use the modules
Fsaverage vertex coordinates are in this repo (*fsa_coords*).\
Vertex coordinates for all subjects can be downloaded from the [OSF project storage](https://osf.io/t6fph/?view_only=e5428abd0da84b4f92e89bbf30bd26aa)\
Otherwise, they can be calculated:
```
from coords_extract import fsa_coords_extract, sub_coords_extract
fsa_coords_extract(fsa)
sub_coords_extract(sublist, nsd_dir)
```
Likewise, curvature values for each subject are already available within this repo (*sub_curvatures*).\
They can also be calculated:
```
from curvature_extract import sub_curv_extract
sub_curv_extract(sub_list, fsa_dir, nsd_dir)
```
Currently, you can:
- extract subject vertex coordintas (in fsaverage space)
- extract fsa vertex coordinates
- extract subject curvature values
- calculate euclidean distance for pairwise runs within a subject
- plot some descriptive stats (kde, scatter and violin plots)
- plot pairwise curvature differences with a regression line and Pearson correlation coefficient
- plot pairwise submeshes on an inflated surface of the first given run 
- plot binary curvature differences on an inflated fsa surface
- plot gray masks differences between pairs of runs

