"""
Author: Nicholas Hunt-Walker
Created: Aug 6, 2014

This script is solely for combining all the data retrieved from ALLWISE for 
the relaxed sample criteria, and ensuring that it adheres to my candidate 
criteria:

cut1 = J-K > 1.1
cut2 = W3-W4 < -0.83*(W2-W3) + 3.37
cut3 = W2-W3 > 0.3

fntlim = [16.83,15.6,11.32,8.0,16.5,16.0,15.5] # All 5-sig faint limits
brtlim = [2.0,1.5,-3.0,-4.0] # PSF estimation limits from the Explanatory Supplement
snr limit  = 3

The faint limits and color cuts 
have already been handled by GATOR. All we have to do here is get the valuable data out
and make sure to take the CC Flags into account

The 2MASS faint limits are coming from
http://www.ipac.caltech.edu/2mass/releases/allsky/doc/sec6_1a.html

Outputting the results to the file
	agbcandidates_ALLWISE_relaxed.dat

"""
import numpy as np
import os

os.chdir('/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/scripts')

infile_dir = '/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/allwise_relaxed/'
## Reading in all the downloaded files from GATOR.
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
        alldata.append(data[jj])

        if data[jj][-9] == "0000": # confusion/contamination flags == 0
            if data[jj][-8] == 0: # extended source flags == 0
                if data[jj][-7] == 1: #number of 2MASS matches == 1
                    alldata.append(data[jj])

alldata = np.array(alldata)

nobj = len(alldata)
## Data collected into the alldata array

fntlim = [12.0,12.0,11.32,8.0,16.5,16.0,15.5] # custom faint limits
#brtlim = [2.0,1.5,-3.0,-4.0] # PSF estimation limits from the Explanatory Supplement
#snrlim = 3

## Set up arrays for putting data into
wid = np.zeros(nobj,dtype='S20')
ra = np.zeros(nobj,dtype=float)
decl = np.zeros(nobj,dtype=float)
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
ccflags = np.zeros(nobj,dtype='S4')
extflag = np.zeros(nobj,dtype=int)
n_2mass = np.zeros(nobj,dtype=int)
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
	decl[ii] = data[2]
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
	ccflags[ii] = data[21]
	extflag[ii] = data[22]
	n_2mass[ii] = data[23]
	j[ii] = data[24]
	jerr[ii] = data[25]
	h[ii] = data[26]
	herr[ii] = data[27]
	k[ii] = data[28]
	kerr[ii] = data[29]

### WE ARE NOT DOING SIGMA CUTS YET
#### Need to ensure that J, H, and K are at least 3 sigma detections
##jsnr = 1/jerr
##hsnr = 1/herr
##ksnr = 1/kerr
##snrcut = np.where((jsnr > snrlim) & (hsnr > snrlim) & (ksnr > snrlim))
##nobj = len(snrcut[0])
#
#def cleaner(wid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,pmra,pmdec,sigpmra,sigpmdec,j,h,k,jerr,herr,kerr):
#
#    thecut = np.where((w1 < fntlim[0]) & (w2 < fntlim[1]) & 
#        (w3 < fntlim[2]) & (w4 < fntlim[3]) &
#        (j < fntlim[4]) & (h < fntlim[5]) & (k < fntlim[6]) &
#        ((w2-w3) > 0.2))
#    return thecut[0]    
#
#snrcut = cleaner(wid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,pmra,pmdec,sigpmra,sigpmdec,j,h,k,jerr,herr,kerr)
#nobj = len(snrcut)
#
### Now re-allocate data.
#wid = wid[snrcut]
#ra = ra[snrcut]
#decl = decl[snrcut]
#gall = gall[snrcut]
#galb = galb[snrcut]
#w1 = w1[snrcut]
#w1err = w1err[snrcut]
#w1snr = w1snr[snrcut]
#w2 = w2[snrcut]
#w2err = w2err[snrcut]
#w2snr = w2snr[snrcut]
#w3 = w3[snrcut]
#w3err = w3err[snrcut]
#w3snr = w3snr[snrcut]
#w4 = w4[snrcut]
#w4err = w4err[snrcut]
#w4snr = w4snr[snrcut]
#pmra = pmra[snrcut]
#sigpmra = sigpmra[snrcut]
#pmdec = pmdec[snrcut]
#sigpmdec = sigpmdec[snrcut]
#j = j[snrcut]
#jerr = jerr[snrcut]
#h = h[snrcut]
#herr = herr[snrcut]
#k = k[snrcut]
#kerr = kerr[snrcut]
#
#
#fout = open(infile_dir+'agbcandidates_ALLWISE_relaxed.dat','w')
#fmt = '%s %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n'
#
#for ii in range(nobj):
#	fout.write(fmt % (wid[ii],ra[ii],decl[ii],gall[ii],galb[ii],w1[ii],w2[ii],w3[ii],w4[ii],w1err[ii],w2err[ii],w3err[ii],w4err[ii],w1snr[ii],w2snr[ii],w3snr[ii],w4snr[ii],pmra[ii],pmdec[ii],sigpmra[ii],sigpmdec[ii],j[ii],h[ii],k[ii],jerr[ii],herr[ii],kerr[ii]))
#fout.close()
#
### =====================================
#
#def get_orich_stars(w1,w2,w3,w4):
#    col12 = w1-w2
#    col23 = w2-w3
#    col34 = w3-w4
#    
#    fullcut = np.where((col12 < 2.) & (col12 > 0.2) & (col23 > 0.4) & (col23 < 2.2) & (col34 > 0) &
#				(col34 < 1.3) & (col34 > 0.722*col23 - 0.289))[0]
#    
#    return fullcut
#
#def get_crich_stars(w1,w2,w3,w4):
#    col12 = w1-w2
#    col23 = w2-w3
#    col34 = w3-w4
#
#    fullcut = np.where((col12 > 0.629*col23 - 0.198) & (col12 < 0.629*col23 + 0.359) &
#				(col34 > 0.722*col23 - 0.911) & (col34 < 0.722*col23 - 0.289))[0]
#
#    return fullcut
#    
#def spectype_relation(colk3,col12,col23,spec_class):
#    absw1 = np.zeros((len(colk3),3))
#
#    orich = np.array([[-9.15,0.02],[-9.13,0.05],[-9.00,0.09]])
#    crich = np.array([[-9.16,0.03],[-9.46,0.42],[-9.33,0.18]])
#
#    xvars = np.array([colk3,col12,col23])
#    
#    for ii in range(3):
#        for jj in range(len(colk3)):
#            if spec_class == "orich":
#                absw1[jj,ii] = orich[ii,0] + orich[ii,1]*xvars[ii,jj]## w1 vs colk3
#                
#            elif spec_class == "crich":
#                absw1[jj,ii] = crich[ii,0] + crich[ii,1]*xvars[ii,jj]## w1 vs colk3
#            
#    return absw1
#
#coljk = j-k
#colk3 = k-w3
#col12 = w1-w2
#col23 = w2-w3
#col34 = w3-w4
#
#orich = get_orich_stars(w1,w2,w3,w4)
#crich = get_crich_stars(w1,w2,w3,w4)
#
#absw1_orich = spectype_relation(colk3[orich],col12[orich],col23[orich],"orich").mean(axis=1)
#absw1_crich = spectype_relation(colk3[crich],col12[crich],col23[crich],"crich").mean(axis=1)
#
#outfile_dir = infile_dir + 'candidates_relaxed/'
#outfile1 = outfile_dir + 'agbcandidates_ALLWISE_nikutta_relaxed_orich.dat'
#outfile2 = outfile_dir + 'agbcandidates_ALLWISE_nikutta_relaxed_crich.dat'
#
#
## column titles: ra,decl,gall,galb
##                w1,w2,w3,w4
##                w1err,w2err,w3err,w4err
##                w1snr,w2snr,w3snr,w4snr
##                pmra,pmdec,sigpmra,sigpmdec
##                j,h,k,jerr,herr,kerr,abs_w1
#fmt = "%i %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n"
#
#fout = open(outfile1,'w')
#for ii in range(len(absw1_orich)):
#    fout.write(fmt % (ii,ra[orich][ii],decl[orich][ii],gall[orich][ii],galb[orich][ii],w1[orich][ii],w2[orich][ii],w3[orich][ii],w4[orich][ii],w1err[orich][ii],w2err[orich][ii],w3err[orich][ii],w4err[orich][ii],w1snr[orich][ii],w2snr[orich][ii],w3snr[orich][ii],w4snr[orich][ii],pmra[orich][ii],pmdec[orich][ii],sigpmra[orich][ii],sigpmdec[orich][ii],j[orich][ii],h[orich][ii],k[orich][ii],jerr[orich][ii],herr[orich][ii],kerr[orich][ii],coljk[orich][ii], colk3[orich][ii], col12[orich][ii], col23[orich][ii], col34[orich][ii], absw1_orich[ii]))
#fout.close()
#
#fout = open(outfile2,'w')
#for ii in range(len(absw1_crich)):
#    fout.write(fmt % (ii,ra[crich][ii],decl[crich][ii],gall[crich][ii],galb[crich][ii],w1[crich][ii],w2[crich][ii],w3[crich][ii],w4[crich][ii],w1err[crich][ii],w2err[crich][ii],w3err[crich][ii],w4err[crich][ii],w1snr[crich][ii],w2snr[crich][ii],w3snr[crich][ii],w4snr[crich][ii],pmra[crich][ii],pmdec[crich][ii],sigpmra[crich][ii],sigpmdec[crich][ii],j[crich][ii],h[crich][ii],k[crich][ii],jerr[crich][ii],herr[crich][ii],kerr[crich][ii],coljk[crich][ii], colk3[crich][ii], col12[crich][ii], col23[crich][ii], col34[crich][ii], absw1_crich[ii]))
#fout.close()
#
