#!/bin/bash

#Parse all parts in a sim in parallel

#Arg 1: sim
#Arg 2: part min
#Arg 3: part max
#Arg 4: node

#ex: ./parseAll 50A 1 12 n004

sim=$1
min=$2
max=$3
node=$4

if [ $# == 4 ]; then
	script=/home/oge1/lammps/sapphire/analysis/exec/parse.sh
	name=parseAll_${sim}_atom{}
	arg1=/home/oge1/lammps/sapphire/analysis/data/${sim}/atom{} 
	arg2=${sim}/atom{}  
	arg3=""

	$script compile
	/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script $name $node $arg1 $arg2 "" $min $max
else
	echo "Please use 4 command line arguments: sim, min, max, node"
fi
