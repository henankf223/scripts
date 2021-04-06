# 1D-DVR examples
# Compute vib constants omega_0, and plot 5 vibrational eigenfunctions

import xlrd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

def convert_to_bohr(x):
    for i in range(len(x)):
        x[i] *= 1.8897259886

# Import 1-D PES data
workbook = xlrd.open_workbook('CO_NaCl_renew.xlsx', on_demand=True)
bdr_0 = workbook.sheet_by_index(23)
dist = np.array(bdr_0.col_values(0, 2, 15)) # R data
energy = np.array(bdr_0.col_values(7, 2, 15)) # Energy data corresponding to R

convert_to_bohr(dist)

N = 100 # number of x, will have N-1 basis, and N+1 independent points

# Intrapolate original PES to N points
x_ab = np.linspace(dist.min(), dist.max(), N+1) 
spl = make_interp_spline(dist, energy, k=3)  # type: BSpline
energy_intp = spl(x_ab)

a = x_ab[0]
b = x_ab[N]

# Define the reduced mass
#m = 6.85714 * 1822.88839 # C12 O16
m = 7.54839 * 1822.88839 # C13 O18
hbar = 1

def basis_func(x, n):
    # Use plain wave basis
    return np.sqrt(2/(b-a)) * np.sin((n*np.pi*(x-a))/(b-a))

# Build Hamiltonian:
H = np.zeros(shape=(N-1,N-1))

for i in range(N-1):
    for j in range(N-1):
        if i != j:
            H[i][j] = hbar**2 / (2 * m) * (-1.0)**(i-j)/(b-a)**2 * (np.pi)**2 / 2.0 \
            * (1/(np.sin(np.pi*(i-j)/(2*N)))**2 - 1/(np.sin(np.pi*(i+j+2)/(2*N)))**2)
        else:
            H[i][j] = hbar**2 / (2*m) * 1.0 / (b-a)**2 * (np.pi)**2 / 2 \
            * ((2*N**2+1)/3 - 1/(np.sin(np.pi*(i+1)/N))**2) \
            + energy_intp[i+1]

#print(H)
eigs, eigv = np.linalg.eig(H)

idx = eigs.argsort()[::1]
eigs = eigs[idx] # ordered eigenvalues
eigv = eigv[:,idx] # ordered eigenvectors

print('Base frequency (0->1):')
print((eigs[1]-eigs[0])*219474.6)

k = 5 # number of points to fit vib constants
ylist = []
Xlist = []
x1 = []
x2 = []
x3 = []
for i in range(k-2):
    ylist.append((eigs[i+2]-eigs[i])*219474.63)
    x1.append(2)
    x2.append(-4*i - 6)
    x3.append(6*(i+2)**2 - 6*(i+2) + 3.5)
    
Xlist.append(x1)
Xlist.append(x2)
Xlist.append(x3)

X = np.array(Xlist)
Y = np.array(ylist)

Xt = np.transpose(X)
#X = np.c_[X, np.ones(X.shape[0])] # Add a constant term (if needed)
#print(Xt.shape[0], Xt.shape[1])
beta_hat = np.linalg.lstsq(Xt, Y)[0]

#sigma = np.linalg.lstsq(X, Y)[1]
print('Vibrational Constants:')
print(beta_hat)

def vib_wave(v, amplifier):
    # v: vibrational level, amplifier: scaling the image
    wave = np.zeros(N+1)
    wave[0] = eigs[v]
    wave[N] = eigs[v]

    for k in range(N-1):
        wave[k+1] = -eigv[k][v]
        wave[k+1] *= amplifier
        wave[k+1] += eigs[v]
    
    return wave

# Just select 5 vibrational eigenfunctions to take a look!
wave1 = vib_wave(0, 0.03)
wave2 = vib_wave(5, 0.03)
wave3 = vib_wave(10, 0.03)
wave4 = vib_wave(15, 0.03)
wave5 = vib_wave(30, 0.03)

x_ab *= 0.529177249

plt.figure(figsize=(8,5))
plt.plot(x_ab, energy_intp)
plt.plot(x_ab, wave1, label='v=0')
plt.plot(x_ab, wave2, label='v=5')
plt.plot(x_ab, wave3, label='v=10')
plt.plot(x_ab, wave4, label='v=15')
plt.plot(x_ab, wave5, label='v=30')
plt.xlabel('R ($\AA$)')
plt.ylabel('energy, Eh')
plt.legend()
plt.show()
