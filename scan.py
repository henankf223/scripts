import os
import numpy as np

# This script generates the coordinates (6-d) of diatom molecules on a surface following a cyclidrical-spherical coordinates.
# Leave terms rx1=, ry1=, rz1=, rx2=, ry2=, rz2= in input.dat for the script to work
# Leave a psi4_script.sh in the folder, then the job will be automatically submitted to PBS
# The preset atom1_nu, atom2_nu is for CO, modify them to other values according to reduced mass if you are using other molecule.
# modify r, R, l, az, tilt, phi to the value list you want to scan, EVALUATE THE COST BEFORE SUBMITTING !!!

r = [0.872, 0.932, 1.032, 1.132, 1.232, 1.332, 1.432, 1.532, 1.632, 1.732, 1.832] # C-O bond length
R = [2.83, 2.93, 3.03, 3.13, 3.23, 3.33, 3.43, 3.53, 3.63, 3.73, 3.93, 4.13, 4.33, 4.53, 4.73, 4.93] # C-O center of mass to NaCl surface distances
l = [0.0]  # Center-of-mass in-plane displacement
az = [45] # center-of-mass xy rotation
tilt = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144, 156, 168, 180] # C-O z tilt
phi = [0] # C-O xy free rotation
atom1_mu = 0.5712 # O center-of-mass partition of r
atom2_mu = 0.4288 # C center-of-mass partition of r
lattice_a = 2.82 # NaCl lattice parameter

for azi in az:
    for ri in r:
        for Ri in R:
            for li in l:
                for tilt_i in tilt:
                    for phi_i in phi:
                        z_center_of_mass = Ri + lattice_a
                        x_center_of_mass = li * np.cos(np.deg2rad(azi))
                        y_center_of_mass = li * np.sin(np.deg2rad(azi))
                        dO = ri * atom2_nu
                        dC = ri * atom1_nu
                        O_rz = dO * np.cos(np.deg2rad(tilt_i)) + z_center_of_mass
                        O_rx = dO * np.sin(np.deg2rad(tilt_i)) * np.cos(np.deg2rad(azi + phi_i)) + x_center_of_mass
                        O_ry = dO * np.sin(np.deg2rad(tilt_i)) * np.sin(np.deg2rad(azi + phi_i)) + y_center_of_mass
                        C_rz = z_center_of_mass - dC * np.cos(np.deg2rad(tilt_i))
                        C_rx = x_center_of_mass - dC * np.sin(np.deg2rad(tilt_i)) * np.cos(np.deg2rad(azi + phi_i))
                        C_ry = y_center_of_mass - dC * np.sin(np.deg2rad(tilt_i)) * np.sin(np.deg2rad(azi + phi_i))
                        name = str(ri) + '_' + str(Ri) + '_' + str(li) + '_' + str(tilt_i) + '_' + str(azi) + '_' + str(phi_i)
                        str1 = "mkdir %s" % name
                        str2 = "sed -i 's/rz2=.*/rz2=%8.8f/g' input.dat" % O_rz
                        str3 = "sed -i 's/rx2=.*/rx2=%8.8f/g' input.dat" % O_rx
                        str4 = "sed -i 's/ry2=.*/ry2=%8.8f/g' input.dat" % O_ry
                        str5 = "sed -i 's/rz1=.*/rz1=%8.8f/g' input.dat" % C_rz
                        str6 = "sed -i 's/rx1=.*/rx1=%8.8f/g' input.dat" % C_rx
                        str7 = "sed -i 's/ry1=.*/ry1=%8.8f/g' input.dat" % C_ry
                        str_inp = "sed -i 's/nacl_.*/nacl_%s/g' psi4_script.sh" % name
                        str_sub_1 = "cp psi4_script.sh %s/" % name
                        str_sub_2 = "cp input.dat %s/" % name
                        os.system(str1)
                        os.system(str2)
                        os.system(str3)
                        os.system(str4)
                        os.system(str5)
                        os.system(str6)
                        os.system(str7)
                        os.system(str_inp)
                        os.system(str_sub_1)
                        os.system(str_sub_2)
                        os.chdir("./%s" % name)
                        os.system("qsub psi4_script.sh")
                        print("Point %s submitted" % name)
                        os.chdir("./../")
