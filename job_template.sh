#!/bin/bash

#SBATCH --job-name=example      # job name (default is the name of this file)
#SBATCH --output=log.%x.job_%j  # file name for stdout/stderr (%x will be replaced with the job name, %j with the jobid)
#SBATCH --time=1-10:00:00          # maximum wall time allocated for the job (D-H:MM:SS)

#SBATCH --partition=gp          # partition/queue name for the job submission
#SBATCH --gres=gpu:2
#SBATCH --ntasks=1              # number of tasks/processes

#SBATCH --mem=10G
#SBATCH --cpus-per-task=8       # number of CPUs per process

# start the job in the directory it was submitted from
cd "$SLURM_SUBMIT_DIR"

# run the computation
./tnl-lbm/sim_NSE/run sim_1 4 FILENAME.txt

# move the output file to the results directory and clean up
mv /mnt/gp3/home/bures/tnl-lbm/sim_NSE/tmp/val_FILENAME.txt /mnt/gp3/home/bures/tnl-lbm/sim_NSE/results/val_FILENAME.txt
rm /mnt/gp3/home/bures/tnl-lbm/job_FILENAME.sh
