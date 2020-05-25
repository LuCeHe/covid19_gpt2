#!/bin/bash
#SBATCH --time=4:00:00
#SBATCH --account=def-jrouat
#SBATCH --mem 8G
#SBATCH --cpus-per-task 2
module load python/3.6
source ~/projects/def-jrouat/lucacehe/denv2/bin/activate
cd ~/projects/def-jrouat/lucacehe/work/covid19_gpt2
python main.py