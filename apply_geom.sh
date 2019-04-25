#!/bin/bash

# a script to apply all geometry (geom_*) to input and run calculation
inputname="input.dat"

counter=1
startline=$(grep -n '[A-Z]\ .*' $inputname | cut -d : -f 1 | head -1)
for filename in ./geom_*; do
    mkdir $counter
    count_match=1
    grep -r '[A-Z]' $filename | while read line
    do
        linenum=$((startline + count_match - 1))
        echo $linenum
        sed -i "${linenum}s/.*/${line}/" $inputname
        ((++count_match))
    done
    cp $inputname $counter
    cp psi4_script.sh $counter
    cd $counter
    qsub psi4_script.sh
    cd ..
    ((++counter))
done
