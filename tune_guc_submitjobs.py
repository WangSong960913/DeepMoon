#These jobs are submitted to ICS
#This tunes the post-processed hypers, calls the get_unique_craters (guc) pipeline.

import itertools
import numpy as np
import os

#iterate parameters
longlat_thresh2 = np.array([0.6,1.0,1.4,1.8,2.2,2.6,3.0,3.4,3.8])
rad_thresh = np.array([0.2,0.6,1.0,1.4,1.8,2.2,2.6,3.0,3.4,3.8])

#all combinations of above params
params = list(itertools.product(*[longlat_thresh2, rad_thresh]))

#submit jobs as you make them. If ==0 just make them
submit_jobs = 1

#make jobs
jobs_dir = "tune_guc"
counter = 0
for llt2,rt in params:
    name = "tuneguc_llt%.2e_rt%.2e"%(llt2,rt)
    pbs_script_name = "%s.pbs"%name
    with open('%s/%s'%(jobs_dir,pbs_script_name), 'w') as f:
        f.write('#!/bin/bash\n')
        f.write('#PBS -l nodes=1:ppn=1\n')
        f.write('#PBS -l walltime=36:00:00\n')
        f.write('#PBS -l pmem=4gb\n')
        f.write('#PBS -A ebf11_a_g_sc_default\n')
        f.write('#PBS -j oe\n')
        f.write('module load python/3.3.2\n')
        f.write('export PATH="/storage/work/ajs725/conda/install/bin:$PATH"\n')
        f.write('cd $PBS_O_WORKDIR\n')
        f.write('python run_get_unique_craters.py %f %f > %s/%s.txt\n'%(llt2,rt,jobs_dir,name))
    f.close()

    if submit_jobs == 1:
        os.system('mv %s/%s %s'%(jobs_dir,pbs_script_name, pbs_script_name))
        os.system('qsub %s'%pbs_script_name)
        os.system('mv %s %s/%s'%(pbs_script_name,jobs_dir,pbs_script_name))
        counter += 1

print("submitted %d jobs"%counter)