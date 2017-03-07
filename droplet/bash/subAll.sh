#!/bin/bash

p=/home/oge1/lammps/sapphire/analysis/exec/parallel.sh
node=bethel

#Compile
echo "Compiling..."
/home/oge1/lammps/sapphire/analysis/root/compilePS.sh

#Submit jobs
echo "Submitting jobs..."
#$p /home/oge1/lammps/sapphire/analysis/exec/analyze.sh ps_20A_atom{} $node /home/oge1/lammps/sapphire/analysis/results/20A/atom{}/calculated.txt 20A/atom{} polarScatter 2 3
#$p /home/oge1/lammps/sapphire/analysis/exec/analyze.sh ps_30A_atom{} $node /home/oge1/lammps/sapphire/analysis/results/30A/atom{}/calculated.txt 30A/atom{} polarScatter 1 6
#$p /home/oge1/lammps/sapphire/analysis/exec/analyze.sh ps_40A_atom{} $node /home/oge1/lammps/sapphire/analysis/results/40A/atom{}/calculated.txt 40A/atom{} polarScatter 11 12
$p /home/oge1/lammps/sapphire/analysis/exec/analyze.sh ps_50A_atom{} $node /home/oge1/lammps/sapphire/analysis/results/50A/atom{}/calculated.txt 50A/atom{} polarScatter 1 12
#$p /home/oge1/lammps/sapphire/analysis/exec/analyze.sh ps_60A_atom{} $node /home/oge1/lammps/sapphire/analysis/results/60A/atom{}/calculated.txt 60A/atom{} polarScatter 1 5

# Hemisphere
#$p /home/oge1/lammps/sapphire/analysis/exec/analyze.sh ps_Hemi50A_atom{} $node /home/oge1/lammps/sapphire/analysis/results/Hemi50A/atom{}/calculated.txt Hemi50A/atom{} polarScatter 6 9
echo "Done submitting jobs!"
