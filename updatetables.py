import MySQLdb
import numpy as np
import os

db = MySQLdb.connect(host='localhost', user='root', passwd='root')
cursor = db.cursor()

os.chdir('/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/fromdb')

sql = "SELECT machoid,p0,p1,sequence FROM agbtables.macho_lpvs;"
# sql = "SELECT ogle3cnt,spectr FROM agbtables.ogle3_agbs;"
cursor.execute(sql)
results = cursor.fetchall()
n = len(results)

catid = np.zeros(n)
p0 = np.zeros(n)
p1 = np.zeros(n)
stype = np.zeros(n,dtype=str)

outfile = open('macho_idtype.txt','w')
fmt = "UPDATE macho_allwise_allmags SET sequence='%s',p0=%.3f,p1=%.3f WHERE machoid=%i;\n"
# outfile = open('ogle_idtype.txt','w')
# fmt = "UPDATE ogle3_allwise_allmags SET startype='%s' WHERE ogleid=%i;\n"
for i in range(1,n):
	catid[i] = results[i][0]
	p0 = results[i][1]
	p1 = results[i][2]
	stype[i] = results[i][3]
	outfile.write(fmt % (results[i][3],results[i][1],results[i][2],results[i][0]))
outfile.close()


os.chdir('/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/scripts')

