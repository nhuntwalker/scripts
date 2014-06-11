import numpy as np
import MySQLdb
import matplotlib.pyplot as plt
import os

os.chdir('/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/matchedbygator')

db = MySQLdb.connect(host='localhost', user='root', passwd='root')
cursor = db.cursor()

## AGBs
# infile = 'wise_allwise.wise_allwise_p3as_psd22838.tbl' ## MACHO
# infile = 'wise_allwise.wise_allwise_p3as_psd23245.tbl' ## OGLE3
# infile = 'wise_allwise.wise_allwise_p3as_psd23447.tbl' ## SIMBAD

## Contaminants
# infile = 'wise_allwise.wise_allwise_p3as_psd13176.tbl' ## LRGs
# infile = 'wise_allwise.wise_allwise_p3as_psd27059.tbl' ## VAGC
infile = 'wise_allwise.wise_allwise_p3as_psd14475.tbl' ## DR9_SSPP

f = open(infile).readlines()

## ==================================================
## Line [3] should have the number of rows retrieved.
## Line [20] should have the column headers
## Data should start at i = nlines - ndata.
## ==================================================

nlines = len(f)
ndata = eval(f[3].split()[2])
dstart = nlines - ndata

## ==================================================
## Declare fields
## ==================================================

mrad,catid,catra,catdec,wname = [],[],[],[],[]
wra,wdec,wglon,wglat = [],[],[],[]
w1,w1err,w1snr = [],[],[]
w2,w2err,w2snr = [],[],[]
w3,w3err,w3snr = [],[],[]
w4,w4err,w4snr = [],[],[]
ccflg,ext_flg,var_flg = [],[],[]
n2mass,jm,jerr,hm,herr,km,kerr = [],[],[],[],[],[],[]

for i in range(dstart,nlines):
	f[i] = f[i].replace("null","-9999")
	line = f[i].split()
	mrad.append(eval(line[1])),catid.append(eval(line[3])),catra.append(eval(line[4])),catdec.append(eval(line[5])),wname.append(line[6])
	wra.append(eval(line[7])),wdec.append(eval(line[8])),wglon.append(eval(line[12])),wglat.append(eval(line[13]))
	w1.append(eval(line[14])),w1err.append(eval(line[15])),w1snr.append(eval(line[16]))
	w2.append(eval(line[17])),w2err.append(eval(line[18])),w2snr.append(eval(line[19]))
	w3.append(eval(line[20])),w3err.append(eval(line[21])),w3snr.append(eval(line[22]))
	w4.append(eval(line[23])),w4err.append(eval(line[24])),w4snr.append(eval(line[25]))
	ccflg.append(line[26]),ext_flg.append(line[27]),var_flg.append(line[28])
	n2mass.append(eval(line[29])),jm.append(eval(line[30])),jerr.append(eval(line[31]))
	hm.append(eval(line[32])),herr.append(eval(line[33])),km.append(eval(line[34])),kerr.append(eval(line[35]))



## ==================================================
## Query for inserting sources into databases
## ==================================================
# outfile = open("macho_into_db.dat",'w')
# outfile = open("ogle_into_db.dat",'w')
# outfile = open("simbad_into_db.dat",'w')
# outfile = open('lrgs_into_db.dat','w')
# outfile = open('vagc_into_db.dat','w')
outfile = open('dr9_sspp_into_db.dat','w')


for i in range(len(w1)):
	out = "%i,%s,%.6f,%.6f,%.6f," % (catid[i],wname[i],mrad[i],wra[i],wdec[i])
	out += "%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f," % (wglon[i],wglat[i],w1[i],w1err[i],w1snr[i],w2[i],w2err[i],w2snr[i],w3[i],w3err[i])
	out += "%.6f,%.6f,%.6f,%.6f,%s,%s,%s," % (w3snr[i],w4[i],w4err[i],w4snr[i],ccflg[i],ext_flg[i],var_flg[i])
	out += "%i,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f" % (n2mass[i],jm[i],jerr[i],hm[i],herr[i],km[i],kerr[i],catra[i],catdec[i])
	out += "\n"

	outfile.write(out)

outfile.close()
print "Job's done"

os.chdir('/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/scripts')


