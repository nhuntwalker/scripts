# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 18:23:34 2014

@author: Nick

Purpose: Put files in the damn database!
"""

import os
import numpy as np
#import MySQLdb
#
#db = MySQLdb.connect(host='localhost',user='root',passwd='root')
#cursor = db.cursor()

os.chdir('/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/scripts')

infile_dir = '/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/allwise_relaxed/'

# files = [infile_dir+f for f in os.listdir(infile_dir) if f.endswith('.tbl')]

files = [infile_dir+'IpacTableFromSource_8666.tbl',infile_dir+'IpacTableFromSource_22790.tbl']
n = len(files)
totobjs = []

alldata = [] ## This is going to be the variable holding all the data after initial cutting

prelimra = []
prelimdec = []
# f2out = open(infile_dir+'fromgator_cut/allfiles.txt','w')

for ii in range(n):
#for ii in range(1,3):
    readin = open(files[ii],'r').readlines()
    nlines = len(readin) # number of lines in the read file
    ndata = eval(readin[3].split()[-1]) # number of lines of actual data
    skiplines = nlines-ndata # number of lines to skip for the header
    
    fmt = 'S20,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,int,int,int,int,S4,int,int,float,float,float,float,float,float'
    data = np.genfromtxt(files[ii], skip_header = skiplines, dtype=fmt) ##reading data
    totobjs.append(ndata) ##keeping track of the total number of objects before cutting
    nobj = len(data)
    
    
    f1out = open(infile_dir+'fromgator_cut/tmp_%i.dat' % (ii+647),'w')
    fmt = '%s\n'
    for jj in range(nobj):
        datastring = str(data[jj])[1:-1]
        datastring = datastring.replace("'","")
        f1out.write(fmt % datastring)
        
    f1out.close()
    
    #f2out.write("LOAD DATA LOCAL INFILE 'tmp_%i.dat' INTO TABLE agbtables.agbs_relaxed_limits FIELDS TERMINATED BY ',' (wiseid, ra, decl, gall, galb, w1, w2, w3, w4, w1err, w2err, w3err, w4err, w1snr, w2snr, w3snr, w4snr, pmra, pmdec, sigpmra, sigpmdec, ccflag, extflag, n2mass, j, h, k, jerr, herr, kerr);\n" % (ii+647))

# f2out.close()

#wid = []
#ra = []
#decl = []
#gall = []
#galb = []
#w1 = []
#w1err = []
#w1snr = []
#w2 = []
#w2err = []
#w2snr = []
#w3 = []
#w3err = []
#w3snr = []
#w4 = []
#w4err = []
#w4snr = []
#pmra = []
#sigpmra = []
#pmdec = []
#sigpmdec = []
#ccflags = []
#extflag = []
#n_2mass = []
#j = []
#jerr = []
#h = []
#herr = []
#k = []
#kerr = []
#
#for jj in range(nobj):
#	wid.append(data[jj][0])
#	ra.append(data[jj][1])
#	decl.append(data[jj][2])
#	gall.append(data[jj][3])
#	galb.append(data[jj][4])
#	w1.append(data[jj][5])
#	w1err.append(data[jj][6])
#	w1snr.append(data[jj][7])
#	w2.append(data[jj][8])
#	w2err.append(data[jj][9])
#	w2snr.append(data[jj][10])
#	w3.append(data[jj][11])
#	w3err.append(data[jj][12])
#	w3snr.append(data[jj][13])
#	w4.append(data[jj][14])
#	w4err.append(data[jj][15])
#	w4snr.append(data[jj][16])
#	pmra.append(data[jj][17])
#	sigpmra.append(data[jj][18])
#	pmdec.append(data[jj][19])
#	sigpmdec.append(data[jj][20])
#	ccflags.append(data[jj][21])
#	extflag.append(data[jj][22])
#	n_2mass.append(data[jj][23])
#	j.append(data[jj][24])
#	jerr.append(data[jj][25])
#	h.append(data[jj][26])
#	herr.append(data[jj][27])
#	k.append(data[jj][28])
#	kerr.append(data[jj][29])


