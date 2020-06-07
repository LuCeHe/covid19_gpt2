#!/bin/bash
#SBATCH --time=48:00:00
#SBATCH --account=def-jrouat
#SBATCH --mem 32G
#SBATCH --cpus-per-task 4
#SBATCH --gres=gpu:p100:1
#SBATCH --mail-user=luca.celotti@usherbrooke.ca
#SBATCH --mail-type=END
module load python/3.6
source ~/projects/def-jrouat/lucacehe/denv2/bin/activate
cd ~/projects/def-jrouat/lucacehe/work/covid19_gpt2
python main.py