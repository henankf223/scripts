# 2D DVR (need to clean!)

import xlrd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

workbook = xlrd.open_workbook('CO_NaCl_renew.xlsx', on_demand=True)
bdr_1 = workbook.sheet_by_index(26)
r = np.array(bdr_1.col_values(0, 30, 43))
R = np.array(bdr_1.row_values(29, 1, 17))
energy_ori = []
for i in range(16):
    energy_ori.append(bdr_1.col_values(i+1, 30, 43))

energy = np.array(energy_ori) # Select input blocks here
#print(r)
#print(R)
#print(energy)

convert_to_bohr(r)
convert_to_bohr(R)

# Define a test harmonic potential
r_h = np.linspace(-5, 5, 20)
R_h = np.linspace(-10, 10, 40)
E_h = np.zeros(shape=(40, 20))

omega = 2
             
def potential_harmonic(r_h, R_h):
    return 0.5 * omega**2 * r_h**2 + 0.5 * R_h**2

for i in range(40):
    for j in range(20):
        E_h[i][j] = potential_harmonic(r_h[j], R_h[i])

N = 30 # number of x, will have N-1 basis, and N+1 independent points
#m = 6.85714 * 1822.88839 # C12 O16
m = 7.54839 * 1822.88839 # C13 O18
m_R = 31 * 1822.88839
#m = 1
hbar = 1
#std_ref_bar = -5675.30640072032

# Build numerical grids
#r_ab = np.linspace(r_h.min(), r_h.max(), N+1)
#R_ab = np.linspace(R_h.min(), R_h.max(), N+1)
r_ab = np.linspace(r.min(), r.max(), N+1)
R_ab = np.linspace(R.min(), R.max(), N+1)

# Build boundaries
ra = r_ab[0]
rb = r_ab[N]
Ra = R_ab[0]
Rb = R_ab[N]

# Build Hamiltonian:
H = np.zeros(shape=((N-1)**2,(N-1)**2))
#f = interpolate.interp2d(r_h, R_h, E_h, kind='cubic')
f = interpolate.interp2d(r, R, energy, kind='cubic')

# Assume r and R are decoupled !
def TpV(ri, rj, Ri, Rj):
    value1 = 0.0 # r kinetic
    value2 = 0.0 # R kinetic
    potential = 0.0
    
    if ri == rj:
        if Ri != Rj:
            value2 = hbar**2 / (2 * m_R) * (-1.0)**(Ri-Rj)/(Rb-Ra)**2 * (np.pi)**2 / 2.0 \
            * (1/(np.sin(np.pi*(Ri-Rj)/(2*N)))**2 - 1/(np.sin(np.pi*(Ri+Rj+2)/(2*N)))**2)
        if Ri == Rj:
            value2 = hbar**2 / (2*m_R) * 1.0 / (Rb-Ra)**2 * (np.pi)**2 / 2 \
            * ((2*N**2+1)/3 - 1/(np.sin(np.pi*(Ri+1)/N))**2) 
    if Ri == Rj:
        if ri != rj:
            value1 = hbar**2 / (2 * m) * (-1.0)**(ri-rj)/(rb-ra)**2 * (np.pi)**2 / 2.0 \
            * (1/(np.sin(np.pi*(ri-rj)/(2*N)))**2 - 1/(np.sin(np.pi*(ri+rj+2)/(2*N)))**2)
        if ri == rj:
            value1 = hbar**2 / (2*m) * 1.0 / (rb-ra)**2 * (np.pi)**2 / 2 \
            * ((2*N**2+1)/3 - 1/(np.sin(np.pi*(ri+1)/N))**2) 
            
    
    #if ri != rj:
    #    value1 = hbar**2 / (2 * m) * (-1.0)**(ri-rj)/(rb-ra)**2 * (np.pi)**2 / 2.0 \
    #    * (1/(np.sin(np.pi*(ri-rj)/(2*N)))**2 - 1/(np.sin(np.pi*(ri+rj+2)/(2*N)))**2)
    #if ri == rj:
    #    value1 = hbar**2 / (2*m) * 1.0 / (rb-ra)**2 * (np.pi)**2 / 2 \
    #        * ((2*N**2+1)/3 - 1/(np.sin(np.pi*(ri+1)/N))**2) 
    #if Ri != Rj:
    #    value1 = 0.0
    #    value2 = 0.0
        #value2 = hbar**2 / (2 * m) * (-1.0)**(Ri-Rj)/(Rb-Ra)**2 * (np.pi)**2 / 2.0 \
        #* (1/(np.sin(np.pi*(Ri-Rj)/(2*N)))**2 - 1/(np.sin(np.pi*(Ri+Rj+2)/(2*N)))**2)
    #if Ri == Rj:
        
    #    value2 = 0.0
        #value2 = hbar**2 / (2*m) * 1.0 / (Rb-Ra)**2 * (np.pi)**2 / 2 \
        #    * ((2*N**2+1)/3 - 1/(np.sin(np.pi*(Ri+1)/N))**2) 
    if Ri == Rj and ri == rj:
        potential = f(r_ab[ri], R_ab[Ri])
        
    return value1 + value2 + potential
            
# Evaluate H elements
for ri in range(N-1):
    for rj in range(N-1):
        for Ri in range(N-1):
            for Rj in range(N-1):
                H[Ri*(N-1)+ri][Rj*(N-1)+rj] = TpV(ri, rj, Ri, Rj)

#print(H)
eigs, eigv = np.linalg.eig(H)

idx = eigs.argsort()[::1]
eigs = eigs[idx] # ordered eigenvalues
eigv = eigv[:,idx] # ordered eigenvectors

#print(eigs)

# Extract vibrational eigs
print('Base frequency (0->1):')
print((eigs[1]-eigs[0])*219474.63)

print('Test frequency (0->2):')
print((eigs[2]-eigs[0])*219474.63)

print('Test frequency (0->5):')
print((eigs[4]-eigs[0])*219474.63)

freq = []
for i in range(N):
    freq.append((eigs[i]-eigs[0])*219474.63)
    
plt.figure(figsize=(1,8))
for i in range(N):
    plt.hlines(freq[i], 0, 1)
plt.ylabel('vib level (cm$^{-1}$)')
plt.legend()
plt.show()

k = 5
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

#print(Y.shape[0])
#print(X.shape[0], X.shape[1])

Xt = np.transpose(X)
#X = np.c_[X, np.ones(X.shape[0])] # Add a C term
#print(Xt.shape[0], Xt.shape[1])
beta_hat = np.linalg.lstsq(Xt, Y)[0]

#sigma = np.linalg.lstsq(X, Y)[1]
print('Vibrational Constant:')
print(beta_hat)
