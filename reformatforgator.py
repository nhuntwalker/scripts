import numpy as np
import MySQLdb
import os

os.chdir('/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/')

db = MySQLdb.connect(host="localhost", user="root", passwd="root")
cursor = db.cursor()

# infile = './fromdb/agbs/macho_idpos.dat'
# infile = './fromdb/agbs/ogle3_idpos.dat'
# infile = './fromdb/agbs/simbad_idpos.dat'

# infile = '../DENIS/denis_agb.tab'

# infile = './fromdb/contaminants/lrg_objects_nohead.dat'
# infile = './fromdb/contaminants/vagc_objects_nohead.dat'
infile = './fromdb/contaminants/dr9_sspp_nohead.dat'

f = open(infile).readlines()

## ================================
## Build header with column names
## and data types
## ================================

# n = len(f[0].split())
n = len(f[2].split())
# head1 = "|"
# head1 += "id    |ra      |dec        |\n"
# head2 = "|int   |double  |double     |\n"

# head1 = "|"
# head1 += "id    |ra         |dec         |imag      |jmag       |kmag\n"
# head2 = "|int   |double     |double      |double    |double     |double\n"

head1 = "|"
head1 += "id     |ra       |dec              |\n"
head2 = "|int    |double   |double           |\n"

## ================================
## Outputting IPAC-compliant table
## ================================

# outfile = open('./submittogator/macho_idpos_ipactable.dat','w')
# outfile = open('./submittogator/ogle3_idpos_ipactable.dat','w')
# outfile = open('./submittogator/simbad_idpos_ipactable.dat','w')

# outfile = open('../DENIS/denis_togator.dat','w')

# outfile = open('./submittogator/lrg_idpos_ipactable.dat','w')
# outfile = open('./submittogator/vagc_idpos_ipactable.dat','w')
outfile = open('./submittogator/dr9_sspp_idpos_ipactable.dat','w')

# fmt1 = " %s      %.4f   %.4f\n"
# fmt2 = " %s     %.4f   %.4f\n"
# fmt3 = " %s    %.4f   %.4f\n"
# fmt4 = " %s   %.4f   %.4f\n"
# fmt5 = " %s  %.4f   %.4f\n"

# fmt1 = " %i      %s   %s   %s     %s      %s\n"
# fmt2 = " %i     %s   %s   %s     %s      %s\n"
# fmt3 = " %i    %s   %s   %s     %s      %s\n"
# fmt4 = " %i   %s   %s   %s     %s      %s\n"
# fmt5 = " %i  %s   %s   %s     %s      %s\n"

fmt1 =  " %i       %.3f  %s\n"
fmt1a = " %i       %.3f     %s\n"
fmt1b = " %i       %.3f       %s\n"

fmt2 =  " %i      %.3f  %s\n"
fmt2a = " %i      %.3f     %s\n"
fmt2b = " %i      %.3f       %s\n"

fmt3 =  " %i     %.3f  %s\n"
fmt3a = " %i     %.3f     %s\n"
fmt3b = " %i     %.3f       %s\n"

fmt4 =  " %i    %.3f  %s\n"
fmt4a = " %i    %.3f     %s\n"
fmt4b = " %i    %.3f       %s\n"

fmt5 =  " %i   %.3f  %s\n"
fmt5a = " %i   %.3f     %s\n"
fmt5b = " %i   %.3f       %s\n"

fmt6 =  " %i  %.3f  %s\n"
fmt6a = " %i  %.3f     %s\n"
fmt6b = " %i  %.3f       %s\n"

fmt7 =  " %i %.3f  %s\n"
fmt7a = " %i %.3f     %s\n"
fmt7b = " %i %.3f       %s\n"


outfile.write('\ \n')
outfile.write(head1)
outfile.write(head2)
j = 1
# for i in range(1,len(f)-1):
# 	if len(f[i].split()[0]) == 1:
# 		outfile.write(fmt1 % (f[i].split()[0],eval(f[i].split()[1]),eval(f[i].split()[2])))
# 	if len(f[i].split()[0]) == 2:
# 		outfile.write(fmt2 % (f[i].split()[0],eval(f[i].split()[1]),eval(f[i].split()[2])))
# 	if len(f[i].split()[0]) == 3:
# 		outfile.write(fmt3 % (f[i].split()[0],eval(f[i].split()[1]),eval(f[i].split()[2])))
# 	if len(f[i].split()[0]) == 4:
# 		outfile.write(fmt4 % (f[i].split()[0],eval(f[i].split()[1]),eval(f[i].split()[2])))
# 	if len(f[i].split()[0]) == 5:
# 		outfile.write(fmt5 % (f[i].split()[0],eval(f[i].split()[1]),eval(f[i].split()[2])))

# for i in range(2,len(f)-1):
# 	if len(str(j)) == 1:
# 		outfile.write(fmt1 % (j,f[i].split()[0],f[i].split()[1],f[i].split()[2],f[i].split()[3],f[i].split()[4]))
# 	if len(str(j)) == 2:
# 		outfile.write(fmt2 % (j,f[i].split()[0],f[i].split()[1],f[i].split()[2],f[i].split()[3],f[i].split()[4]))
# 	if len(str(j)) == 3:
# 		outfile.write(fmt3 % (j,f[i].split()[0],f[i].split()[1],f[i].split()[2],f[i].split()[3],f[i].split()[4]))
# 	if len(str(j)) == 4:
# 		outfile.write(fmt4 % (j,f[i].split()[0],f[i].split()[1],f[i].split()[2],f[i].split()[3],f[i].split()[4]))
# 	if len(str(j)) == 5:
# 		outfile.write(fmt5 % (j,f[i].split()[0],f[i].split()[1],f[i].split()[2],f[i].split()[3],f[i].split()[4]))
# 	j += 1

raind = 159
decind = 160

for i in range(len(f)):
	f[i] = f[i].replace('NULL','-9999')
	if len(str(j)) == 1:
		if len(f[i].split()[raind].split('.')) == 3:
			outfile.write(fmt1 % (j,eval(f[i].split()[raind]),f[i].split()[decind]))
		elif len(f[i].split()[raind].split('.')) == 2:
			outfile.write(fmt1a % (j,eval(f[i].split()[raind]),f[i].split()[decind]))
		elif len(f[i].split()[raind].split('.')) == 1:
			outfile.write(fmt1b % (j,eval(f[i].split()[raind]),f[i].split()[decind]))

	if len(str(j)) == 2:
		if len(f[i].split()[raind].split('.')) == 3:
			outfile.write(fmt2 % (j,eval(f[i].split()[raind]),f[i].split()[decind]))
		elif len(f[i].split()[raind].split('.')) == 2:
			outfile.write(fmt2a % (j,eval(f[i].split()[raind]),f[i].split()[decind]))
		elif len(f[i].split()[raind].split('.')) == 1:
			outfile.write(fmt2b % (j,eval(f[i].split()[raind]),f[i].split()[decind]))

	if len(str(j)) == 3:
		if len(f[i].split()[raind].split('.')) == 3:
			outfile.write(fmt3 % (j,eval(f[i].split()[raind]),f[i].split()[decind]))
		elif len(f[i].split()[raind].split('.')) == 2:
			outfile.write(fmt3a % (j,eval(f[i].split()[raind]),f[i].split()[decind]))
		elif len(f[i].split()[raind].split('.')) == 1:
			outfile.write(fmt3b % (j,eval(f[i].split()[raind]),f[i].split()[decind]))

	if len(str(j)) == 4:
		if len(f[i].split()[raind].split('.')) == 3:
			outfile.write(fmt4 % (j,eval(f[i].split()[raind]),f[i].split()[decind]))
		elif len(f[i].split()[raind].split('.')) == 2:
			outfile.write(fmt4a % (j,eval(f[i].split()[raind]),f[i].split()[decind]))
		elif len(f[i].split()[raind].split('.')) == 1:
			outfile.write(fmt4b % (j,eval(f[i].split()[raind]),f[i].split()[decind]))

	if len(str(j)) == 5:
		if len(f[i].split()[raind].split('.')) == 3:
			outfile.write(fmt5 % (j,eval(f[i].split()[raind]),f[i].split()[decind]))
		elif len(f[i].split()[raind].split('.')) == 2:
			outfile.write(fmt5a % (j,eval(f[i].split()[raind]),f[i].split()[decind]))
		elif len(f[i].split()[raind].split('.')) == 1:
			outfile.write(fmt5b % (j,eval(f[i].split()[raind]),f[i].split()[decind]))

	if len(str(j)) == 6:
		if len(f[i].split()[raind].split('.')) == 3:
			outfile.write(fmt6 % (j,eval(f[i].split()[raind]),f[i].split()[decind]))
		elif len(f[i].split()[raind].split('.')) == 2:
			outfile.write(fmt6a % (j,eval(f[i].split()[raind]),f[i].split()[decind]))
		elif len(f[i].split()[raind].split('.')) == 1:
			outfile.write(fmt6b % (j,eval(f[i].split()[raind]),f[i].split()[decind]))

	if len(str(j)) == 7:
		if len(f[i].split()[raind].split('.')) == 3:
			outfile.write(fmt7 % (j,eval(f[i].split()[raind]),f[i].split()[decind]))
		elif len(f[i].split()[raind].split('.')) == 2:
			outfile.write(fmt7a % (j,eval(f[i].split()[raind]),f[i].split()[decind]))
		elif len(f[i].split()[raind].split('.')) == 1:
			outfile.write(fmt7b % (j,eval(f[i].split()[raind]),f[i].split()[decind]))


	j += 1
outfile.close()


os.chdir('scripts')