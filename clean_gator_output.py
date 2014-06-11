"""
Author: Nicholas Hunt-Walker
Created: Jun 2, 2014
Last Modified: Jun 2, 2014

This script is solely for combining all the data retrieved from
ALLWISE, and ensuring that it adheres to my candidate criteria.

This is to replace my old sample that had the unnecessary W3-W4 < 1.5 cut
Hence, this will refer to the "allwise" directory, and not
the "allwise_old" directory

cut1 = J-K > 1.1
cut2 = W3-W4 < -0.83*(W2-W3) + 3.37
cut3 = W2-W3 > 0.3

fntlim = [16.83,15.6,11.32,8.0] # All 5-sig faint limits
brtlim = [2.0,1.5,-3.0,-4.0] # PSF estimation limits from the Explanatory Supplement
snr limit  = 3

The faint limits, brightness limits, saturation limits, color cuts 
have already been handled by GATOR. All we have to do here is get the valuable data out
and make sure to take the CC Flags into account

Outputting the results to the file
	agbcandidates_ALLWISE.dat

"""
import numpy as np
import os

os.chdir('/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/scripts')

infile_dir = '/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/allwise/'
## Reading in all the downloaded files from GATOR. 36 files in total
files = [infile_dir+f for f in os.listdir(infile_dir) if f.endswith('.tbl')]
n = len(files)
totobjs = []

alldata = [] ## This is going to be the variable holding all the data after initial cutting

prelimra = []
prelimdec = []

for ii in range(n):
    readin = open(files[ii],'r').readlines()
    nlines = len(readin) # number of lines in the read file
    ndata = eval(readin[3].split()[-1]) # number of lines of actual data
    skiplines = nlines-ndata # number of lines to skip for the header

    fmt = 'S20,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,int,int,int,int,S4,int,int,float,float,float,float,float,float'
    data = np.genfromtxt(files[ii], skip_header = skiplines, dtype=fmt) ##reading data
    totobjs.append(ndata) ##keeping track of the total number of objects before cutting
    for jj in range(len(data)):
    	prelimra.append(data[jj][1])
    	prelimdec.append(data[jj][2])

    	## Here we remove data with CC flags that aren't zero, and also
    	## objects that are not point sources
    	if data[jj][-9] == "0000":
    		if data[jj][-8] == 0:
    			if data[jj][-7] == 1:
		        	alldata.append(data[jj])

alldata = np.array(alldata)

nobj = len(alldata)
## Data collected into the alldata array

fntlim = [16.83,15.6,11.32,8.0] # All 5-sig faint limits
brtlim = [2.0,1.5,-3.0,-4.0] # PSF estimation limits from the Explanatory Supplement
snrlim = 3

## Set up arrays for putting data into
wid = np.zeros(nobj,dtype='S20')
ra = np.zeros(nobj,dtype=float)
dec = np.zeros(nobj,dtype=float)
gall = np.zeros(nobj,dtype=float)
galb = np.zeros(nobj,dtype=float)
w1 = np.zeros(nobj,dtype=float)
w1err = np.zeros(nobj,dtype=float)
w1snr = np.zeros(nobj,dtype=float)
w2 = np.zeros(nobj,dtype=float)
w2err = np.zeros(nobj,dtype=float)
w2snr = np.zeros(nobj,dtype=float)
w3 = np.zeros(nobj,dtype=float)
w3err = np.zeros(nobj,dtype=float)
w3snr = np.zeros(nobj,dtype=float)
w4 = np.zeros(nobj,dtype=float)
w4err = np.zeros(nobj,dtype=float)
w4snr = np.zeros(nobj,dtype=float)
pmra = np.zeros(nobj,dtype=float)
sigpmra = np.zeros(nobj,dtype=float)
pmdec = np.zeros(nobj,dtype=float)
sigpmdec = np.zeros(nobj,dtype=float)
# ccflags = np.zeros(nobj,dtype='S4')
# extflag = np.zeros(nobj,dtype=int)
# n_2mass = np.zeros(nobj,dtype=int)
j = np.zeros(nobj,dtype=float)
jerr = np.zeros(nobj,dtype=float)
h = np.zeros(nobj,dtype=float)
herr = np.zeros(nobj,dtype=float)
k = np.zeros(nobj,dtype=float)
kerr = np.zeros(nobj,dtype=float)

## The loop for allocating data appropriately
for ii in range(nobj):
	data = alldata[ii]
	wid[ii] = data[0]
	ra[ii] = data[1]
	dec[ii] = data[2]
	gall[ii] = data[3]
	galb[ii] = data[4]
	w1[ii] = data[5]
	w1err[ii] = data[6]
	w1snr[ii] = data[7]
	w2[ii] = data[8]
	w2err[ii] = data[9]
	w2snr[ii] = data[10]
	w3[ii] = data[11]
	w3err[ii] = data[12]
	w3snr[ii] = data[13]
	w4[ii] = data[14]
	w4err[ii] = data[15]
	w4snr[ii] = data[16]
	pmra[ii] = data[17]
	sigpmra[ii] = data[18]
	pmdec[ii] = data[19]
	sigpmdec[ii] = data[20]
	# ccflags[ii] = data[21]
	# extflag[ii] = data[22]
	# n_2mass[ii] = data[23]
	j[ii] = data[24]
	jerr[ii] = data[25]
	h[ii] = data[26]
	herr[ii] = data[27]
	k[ii] = data[28]
	kerr[ii] = data[29]

## Need to ensure that J, H, and K are at least 3 sigma detections
jsnr = 1/jerr
hsnr = 1/herr
ksnr = 1/kerr
snrcut = np.where((jsnr > snrlim) & (hsnr > snrlim) & (ksnr > snrlim))
nobj = len(snrcut[0])

## Now re-allocate data.
wid = wid[snrcut]
ra = ra[snrcut]
dec = dec[snrcut]
gall = gall[snrcut]
galb = galb[snrcut]
w1 = w1[snrcut]
w1err = w1err[snrcut]
w1snr = w1snr[snrcut]
w2 = w2[snrcut]
w2err = w2err[snrcut]
w2snr = w2snr[snrcut]
w3 = w3[snrcut]
w3err = w3err[snrcut]
w3snr = w3snr[snrcut]
w4 = w4[snrcut]
w4err = w4err[snrcut]
w4snr = w4snr[snrcut]
pmra = pmra[snrcut]
sigpmra = sigpmra[snrcut]
pmdec = pmdec[snrcut]
sigpmdec = sigpmdec[snrcut]
j = j[snrcut]
jerr = jerr[snrcut]
h = h[snrcut]
herr = herr[snrcut]
k = k[snrcut]
kerr = kerr[snrcut]


fout = open(infile_dir+'agbcandidates_ALLWISE.dat','w')
fmt = '%s %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n'

for ii in range(nobj):
	fout.write(fmt % (wid[ii],ra[ii],dec[ii],gall[ii],galb[ii],w1[ii],w2[ii],w3[ii],w4[ii],w1err[ii],w2err[ii],w3err[ii],w4err[ii],w1snr[ii],w2snr[ii],w3snr[ii],w4snr[ii],pmra[ii],pmdec[ii],sigpmra[ii],sigpmdec[ii],j[ii],h[ii],k[ii],jerr[ii],herr[ii],kerr[ii]))
fout.close()



