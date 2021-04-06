# A simple CO on NaCl charge-dipole interaction calculator
# Using simple columb equations and a layer-by-layer extensive cluster model

import numpy as np

# Import charge point data
import xlrd
workbook = xlrd.open_workbook('CO_NaCl.xlsx', on_demand=True)
charge_xyz = workbook.sheet_by_index(18)

# Define constants
z_center_of_mass = 6.1368 * 1.8897259886
z_center_of_charge = 6.056 * 1.8897259886 # center of C and O atom
n_layer = 7
dipole = 0.0718 # BPW91 DFT: C->O C- O+
#dipole = 0.0782 # # DSRG-MRPT2 C->O C- O+

# Build n-layer lattice
x = charge_xyz.col_values(1, 1, 19)
y = charge_xyz.col_values(2, 1, 19)
z = charge_xyz.col_values(3, 1, 19)
c = charge_xyz.col_values(4, 1, 19)

# Use Na-Cl a=2.82 as the unit lattice index
xy_shift = 8.46 * 1.8897259886
z_shift = -5.64 * 1.8897259886

def convert_to_bohr(x):
    for i in range(len(x)):
        x[i] *= 1.8897259886

def shift_xyz(a, shift_val):
    b = []
    for i in range(len(a)):
        b.append(a[i]+shift_val)
    return b

def flip_charge(c):
    c_flip = []
    for i in range(len(c)):
        c_flip.append(-c[i])
    return c_flip

convert_to_bohr(x)
convert_to_bohr(y)
convert_to_bohr(z)

x_list = []
y_list = []
z_list = []
c_list = []

# For single layer, do n_layer-1, n_layer
for i in range(0, n_layer):
    # Build z bulks:
    #x_list.extend(x)
    #y_list.extend(y)
    #z_list.extend(shift_xyz(z, z_shift*(i+1)))
    #c_list.extend(c)
    
    n = i+1
    # Build extended layers:
    for j in range(n+1):
        # jth bottom layer, 0, 1, ...
        for a in range(2*n+1):
            p = a - n
            if (abs(p) != n) and (j != n):
                x_list.extend(shift_xyz(x, xy_shift*p))
                y_list.extend(shift_xyz(y, xy_shift*n))
                z_list.extend(shift_xyz(z, z_shift*j))
                k = int(p + n)
                if (k % 2) == 0:
                    c_list.extend(c)
                else:
                    c_list.extend(flip_charge(c))
                #print(j, p, n)
                
                x_list.extend(shift_xyz(x, xy_shift*p))
                y_list.extend(shift_xyz(y, -xy_shift*n))
                z_list.extend(shift_xyz(z, z_shift*j))
                if (k % 2) == 0:
                    c_list.extend(c)
                else:
                    c_list.extend(flip_charge(c))
                #print(j, p, -n)
            
            else:
                for b in range(2*n+1):
                    q = b - n
                    x_list.extend(shift_xyz(x, xy_shift*p))
                    y_list.extend(shift_xyz(y, xy_shift*q))
                    z_list.extend(shift_xyz(z, z_shift*j))
                    k = p+q
                    if (k % 2 == 0):
                        c_list.extend(c)
                    else:
                        c_list.extend(flip_charge(c))
                    #print(j, p, q)
                    
def coulomb_dipole(x, y, z, c, xd, yd, zd, dip, theta):
    vec_dip = np.array([np.sin(np.deg2rad(theta)), 0.0, np.cos(np.deg2rad(theta))]) # The dipole vector, rotated on xz plane
    vec_charge = np.array([xd-x, yd-y, zd-z]) # the vector from charge to dipole center
    cos_angle = np.dot(vec_dip, vec_charge)/(np.linalg.norm(vec_dip) * np.linalg.norm(vec_charge)) # The cos(angle)
    return -c * dip * cos_angle / ((x - xd)**2 + (y - yd)**2 + (z - zd)**2) # Charge-dipole interaction in a.u.

def compute_interaction(theta):
    Ec_sum = 0.0
    for i in range(len(x_list)):
        Ec_sum += coulomb_dipole(x_list[i], y_list[i], z_list[i], c_list[i], 0.0, 0.0, z_center_of_charge, dipole, theta)
    return Ec_sum
  
# Usage for any diatomics on NaCl surface:
# 1. set up z_center_of_mass, z_center_of_charge, n_layer, and dipole.
# 2. run compute_interaction(theta) to return electronstatic interaction energy in Eh. Theta is the tilt angle of diatomics on the surface.
# 3. for serious computations, incrementing n_layer to converge the results.
