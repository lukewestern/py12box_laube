#!/bin/sh
#SBATCH --job-name=run_py12box_invert_
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:05:0
#SBATCH --mem=1G
#SBATCH --array=1-4

#sbatch py12box_vollmer/slaunch_py12box_vollmer_array.sh

# Try to find out if you can extract this from
# the header rather than hardcoding.
NCPU=1
# Following https://github.com/xianyi/OpenBLAS/wiki/faq#multi-threaded
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1

dir=`python -c 'from py12box_vollmer import get_data; print(get_data("_").parents[1])'`
cd $dir

srun python py12box_vollmer/run_py12box_vollmer.py "all" $SLURM_ARRAY_TASK_ID 1 > $dir/tmp/run_py12box_invert_$SLURM_ARRAY_TASK_ID
