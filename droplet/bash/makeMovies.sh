#!/bin/bash

#makeMovies.sh
#Make all densityHalfA movies in parallel

whichmovie="vfield"
node="bethel"
script='/home/oge1/lammps/sapphire/analysis/exec/movie.sh'
name='movie_{}0A_'"$whichmovie"

#Make movie

## Spherical Sapphire ##

#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script $name $node '{}0A' $whichmovie '' 4 4
/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script $name $node '{}0A' $whichmovie '' 5 5

## Hemispherical Sapphire ##
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script $name $node 'Hemi{}0A' $whichmovie '' 5 5

## Sub951By50 ##

###Cyl
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Cyl{}0A_'"$whichmovie" $node 'Bob/Sub951By50/Cyl{}0A' $whichmovie '' 4 4
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Cyl{}0A_'"$whichmovie" $node 'Bob/Sub951By50/Cyl{}0A' $whichmovie '' 10 10
#
### New Cyl
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Cyl{}0A_New_'"$whichmovie" $node 'Bob/Sub951By50/Cyl{}0A/New' $whichmovie '' 6 6
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Cyl{}0A_New_'"$whichmovie" $node 'Bob/Sub951By50/Cyl{}0A/New' $whichmovie '' 10 10
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Cyl{}0A_New_'"$whichmovie" $node 'Bob/Sub951By100/Cyl{}0A/New' $whichmovie '' 10 10
#
###FullCyl
##/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script $name $node 'Bob/Sub951By50/FullCyl{}0A' $whichmovie '' 2 3
##/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script $name $node 'Bob/Sub951By50/FullCyl{}0A' $whichmovie '' 10 10
#
### Sub951By100 ##
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script $name $node 'Bob/Sub951By100/Cyl{}0A' $whichmovie '' 2 2
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script $name $node 'Bob/Sub951By100/Cyl{}0A' $whichmovie '' 5 5
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script $name $node 'Bob/Sub951By100/Cyl{}0A' $whichmovie '' 10 10

## Quartz ##

#120By120
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Bob/Quartz/120By120/{}0A' $node 'Bob/Quartz/120By120/{}0A' $whichmovie '' 2 2
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Bob/Quartz/120By120/{}5A' $node 'Bob/Quartz/120By120/{}5A' $whichmovie '' 2 2

#240By240
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Bob/Quartz/240By240/{}0A' $node 'Bob/Quartz/240By240/{}0A' $whichmovie '' 3 5
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Bob/Quartz/240By240/{}5A' $node 'Bob/Quartz/240By240/{}5A' $whichmovie '' 3 4

#403By51
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Bob/Quartz/403By51/{}0A' $node 'Bob/Quartz/403By51/{}0A' $whichmovie '' 3 3

## Prewet ##
#Both
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Bob/Prewet/Both/20A_{}0AonMonolayer' $node 'Bob/Prewet/Both/20A_{}0AonMonolayer' $whichmovie '' 2 2
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Bob/Prewet/Both/30A_{}0AonMonolayer' $node 'Bob/Prewet/Both/30A_{}0AonMonolayer' $whichmovie '' 2 3

#Old
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Bob/Prewet/Old/20A_{}0AonMonolayer' $node 'Bob/Prewet/Old/20A_{}0AonMonolayer' $whichmovie '' 2 2
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Bob/Prewet/Old/30A_{}0AonMonolayer' $node 'Bob/Prewet/Old/30A_{}0AonMonolayer' $whichmovie '' 2 3

#New
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Bob/Prewet/New/20A_{}0AonMonolayer' $node 'Bob/Prewet/New/20A_{}0AonMonolayer' $whichmovie '' 2 2
#/home/oge1/lammps/sapphire/analysis/exec/parallel.sh $script 'movie_Bob/Prewet/New/30A_{}0AonMonolayer' $node 'Bob/Prewet/New/30A_{}0AonMonolayer' $whichmovie '' 2 3


