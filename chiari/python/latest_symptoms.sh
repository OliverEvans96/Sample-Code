#!/bin/bash
#latest_symptom.sh
#Find most recently modified version of each symptom result file

cd /home/oevans/chiari/results/symptoms

#List all files
sorted_files=($(ls -t))

#Most recently modified files
most_recent=()

#Names that have already been saved
saved_names=()

#Counters
i=0    #Count all files
n=0    #Count most recent files

#Loop through files
for file in ${sorted_files[@]}
do
    #Remove date, number and file extension from end
    symptom_name=${file%%-*}

    #Save full file name if symptom_name not already recorded
    #At first, it has not been found
    found=false

    #Loop through recorded symptom_names
    for name in ${saved_names[@]}
    do
        if [[ $symptom_name == $name ]]
        then
            found=true
        fi
    done

    #If not found, save full file name
    if [[ $found == false ]]
    then 
        #Save full file name
        most_recent[$n]=${file%.txt}
        ((n++))
    fi

    #Save short name
    saved_names[$i]=$symptom_name

    ((i++))

done

echo "${most_recent[@]}" | xargs printf "symptoms/%s\n" | sort -n

