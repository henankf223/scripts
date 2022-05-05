import xlrd
import xlwt
import subprocess

# This script collect the 3-d PES scan data into an Excel file.

workbook = xlwt.Workbook()

# Modify those variable to your needs
excel_file_path = './PES_PT3.xls' # modify to your name and path
worksheet = workbook.add_sheet('init') 

# Turn this on if there are additional corrections. Please set 'correction_term' correctly to capture the correction.
external = True 

# This string tells the script where to look for energy results in output.dat
energy_term = 'DSRG-MRPT3 total energy' 
# which value (from the left) is the energy result in that line?
energy_loc = 5

# This string tells the script where to look for corrections in output.dat
correction_term = 'Additional nuclear repulsion'
# which value (from the left) is the additional correction in that line?
correction_loc = 5 

# Put in the lists you scanned using scan.py.
r = [0.872, 0.932, 1.032, 1.132, 1.232, 1.332, 1.432, 1.532, 1.632, 1.732, 1.832] # C-O bond length
R = [2.83, 2.93, 3.03, 3.13, 3.23, 3.33, 3.43, 3.53, 3.63, 3.73, 3.93, 4.13, 4.33, 4.53, 4.73, 4.93] # C-O center of mass to NaCl surface distances
tilt = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144, 156, 168, 180] # C-O z tilt

# loop over values to collect data
workbook.save(excel_file_path)
for r_idx, r_val in enumerate(r):
    sheetname = 'r='+str(r_val)
    print('Create sheet for ', sheetname)
    worksheet = workbook.add_sheet(sheetname)
    for tidx, tk in enumerate(tilt):
        worksheet.write(0, tidx+1, tk)
    for R_idx, R_val in enumerate(R):
        worksheet.write(R_idx+1, 0, R_val)
        for t_idx, t_val in enumerate(tilt):
            energystr = "grep -r '%s' %1.3f_%1.2f_0.0_%d_45_0/output.dat | awk {'print $%d'}" % (energy_term, r_val, R_val, t_val, energy_loc)
            ori = subprocess.check_output(energystr, shell=True)
            if len(ori) <= 4:
                print('Data point', r_val, R_val, t_val, 'missing !')
                continue
            data = float(ori)
            #print('string is: ', energystr, 'result is: ', data)
            if external:
                externalstr = "grep -r -m1 '%s' %1.3f_%1.2f_0.0_%d_45_0/output.dat | awk {'print $%d'}" % (correction_term, r_val, R_val, t_val, correction_loc)
                data += float(subprocess.check_output(externalstr, shell=True))
            worksheet.write(R_idx+1, t_idx+1, data)

workbook.save(excel_file_path)
workbook = xlrd.open_workbook(excel_file_path, on_demand=True)

def get_cellvalue(vr, vR, vt, nlist):
    curr = workbook.sheet_by_index(vr)
    cellvalue = curr.cell_value(vR, vt)
    if cellvalue:
        nlist.append(float(cellvalue))
    return
  
# Results verification. If the value is higher or lower than all its neighbor,
# then it is either a minimum/maximum or a wrong computation.
# Please check their output.dat and figure out.
for ver_r in range(1, len(r)+1):
    for ver_R in range(1, len(R)+1):
        for ver_t in range(1, len(tilt)+1):
            neighbor = []
            if ver_r > 1:
                get_cellvalue(ver_r-1, ver_R, ver_t, neighbor)
            if ver_r < len(r):
                get_cellvalue(ver_r+1, ver_R, ver_t, neighbor)
            if ver_R > 1:
                get_cellvalue(ver_r, ver_R-1, ver_t, neighbor)
            if ver_R < len(R):
                get_cellvalue(ver_r, ver_R+1, ver_t, neighbor)
            if ver_t > 1:
                get_cellvalue(ver_r, ver_R, ver_t-1, neighbor)
            if ver_t < len(tilt):
                get_cellvalue(ver_r, ver_R, ver_t+1, neighbor)
            if len(neighbor) <= 3:
                continue
            else:
                minval = min(neighbor)
                maxval = max(neighbor)
                get_cellvalue(ver_r, ver_R, ver_t, neighbor)
                thisval = neighbor[-1]
                if thisval < minval or thisval > maxval:
                    print('Note! point ', r[ver_r-1], R[ver_R-1], tilt[ver_t-1], 'is either min/max or problematic!')
