#!/bin/bash

# A script to generate geometries between reactant and product
# for reaction path scanning and transition states calculation

# Number of intermediate points one want to create
num_of_points=20

# Reactant cartesian coordinate file
react="geom_gen_r"

# Product cartesian coordinate file
prodt="geom_gen_p"

counter=1
grep -r '[A-Z]' $react | while read line
do
    label=$(echo $line | awk {'print $1'})
    x=$(echo $line | awk {'print $2'})
    y=$(echo $line | awk {'print $3'})
    z=$(echo $line | awk {'print $4'})
    xp=$(head -$((counter+1)) $prodt | tail -1 | grep '[A-Z]' | awk {'print $2'})
    yp=$(head -$((counter+1)) $prodt | tail -1 | grep '[A-Z]' | awk {'print $3'})
    zp=$(head -$((counter+1)) $prodt | tail -1 | grep '[A-Z]' | awk {'print $4'})
    ((counter++))
    divider=$(bc <<< "scale=10;$num_of_points+ 1")
    intx_diff=$(bc <<< "scale=10;$xp- $x")
    intx_incre=$(bc <<< "scale=10;$intx_diff/$divider")
    inty_diff=$(bc <<< "scale=10;$yp- $y")
    inty_incre=$(bc <<< "scale=10;$inty_diff/$divider")
    intz_diff=$(bc <<< "scale=10;$zp- $z")
    intz_incre=$(bc <<< "scale=10;$intz_diff/$divider")
    for (( i=1; i<=$num_of_points; i++ ))
    do
        add_diff_x=$(bc <<< "scale=10 ; $intx_incre*$i")
        x_this=$(bc <<< "scale=10;$x+$add_diff_x")
        add_diff_y=$(bc <<< "scale=10;$inty_incre*$i")
        y_this=$(bc <<< "scale=10;$y+$add_diff_y")
        add_diff_z=$(bc <<< "scale=10;$intz_incre*$i")
        z_this=$(bc <<< "scale=10;$z+$add_diff_z")
        echo $label $x_this $y_this $z_this >> "geom_${i}"
    done
done
