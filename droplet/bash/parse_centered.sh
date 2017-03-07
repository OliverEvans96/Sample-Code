#/bin/bash

#2 arguments
#Input file & output folder in sapphire/analysis/results

if [[ $1 == "compile" ]]
then
	#Compile C++ files
	echo "Compiling source files"
	g++ /home/oge1/lammps/sapphire/analysis/src/calculations_centered.cpp -o /home/oge1/lammps/sapphire/analysis/exec/calculations_centered.out

elif [[ $# == 2 ]]
then 
	#Source
	source_file=$1
	#Destination
	out_folder=/home/oge1/lammps/sapphire/analysis/results/$2
	
	echo "Destination: $out_folder"

	#Make destination
	mkdir -p $out_folder

	#Calculate dipole angles and velocities
	echo "Calculating dipole angles and velocities"
	/home/oge1/lammps/sapphire/analysis/exec/calculations_centered.out $out_folder/waters_sorted.txt $out_folder/calculated.txt

	#:)
	echo "Done!"

else
	echo "2 arguments required! - Input file & output folder name in sapphire/analysis"
	echo "$# arguments given"

fi
