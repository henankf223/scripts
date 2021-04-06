# An example of 2-dimensional scan for relational structures

import os

R = ['1.5', '2.0', '2.5']
r = ['1.5', '1.6', '1.7', '1.8', '1.9', '2.0', '2.1', '2.2', '2.3', '2.4', '2.5']

for r_str in r:
    for R_str in R:
        print(r_str, R_str)
        r_abs = float(r_str)/2.0
        str_1 = "sed -i 's/R=.*/R=%s/g' input.dat" % R_str
        R1 = float(R_str) + 0.588 # Change to expressions needed
        str_1b = "sed -i 's/R1=.*/R1=%s/g' input.dat" % R1
        str_2 = "sed -i 's/r1=.*/r1=%s/g' input.dat" % r_abs
        str_3 = "sed -i 's/r2=-.*/r2=-%s/g' input.dat" % r_abs
        str_psi = "sed -i 's/Name_.*/Name_%s/g' psi4_script.sh" % (R_str+ '_' + r_str) # change to different jobnames and submission scripts
        os.system(str_1)
        os.system(str_1b)
        os.system(str_2)
        os.system(str_3)
        os.system(str_psi)
        os.mkdir(R_str+ '_' + r_str)
        os.chdir(R_str+ '_' + r_str)
        str_sub_1 = "cp ../psi4_script.sh ./"
        str_sub_2 = "cp ../input.dat ./"
        str_sub_3 = "qsub psi4_script.sh"
        os.system(str_sub_1)
        os.system(str_sub_2)
        os.system(str_sub_3)
        os.chdir("./../")
