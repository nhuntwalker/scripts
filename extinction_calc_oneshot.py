import numpy as np
import galfastDust as ext
import sys
import time

## Solely for one shot extinction calculations

tstart = time.time()
iteration_num = 0


f = 'agbcandidates_ALLWISE_nikutta_crich.dat'
alldata = np.loadtxt(f, unpack=True)
wid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,pmra,pmdec,sigpmra,sigpmdec,j,h,k,jerr,herr,kerr,coljk, colk3, col12, col23, col34, absw1 = alldata

ra = ra*np.pi/180.
decl = decl*np.pi/180.

n = len(ra)

def calc_ebvs(ra,decl,w1,absw1):
    sig = w1 - absw1
    # absw1 = absw1.mean()

    DMmax = sig
    deltaDM = 0.1
    DMarry = np.arange(deltaDM,DMmax + deltaDM, deltaDM)
    nsteps = len(DMarry) # number of steps in distance will vary

    dist_arry = 10**((DMarry+5.)/5.)/1E3 #convert DM to kpc
    ra_arry = np.ones(nsteps)*ra
    dec_arry = np.ones(nsteps)*decl

    glats, glons = ext.eqToGal(ra_arry, dec_arry)
    ebvs = np.array(ext.getDustValue(glats, glons, dist_arry))

    coeff = [0.34,0.21,0.15,0.11,0.09,0.13]

    A_w1 = coeff[3]*2.751*ebvs
    A_w1_tests = sig - DMarry
    diff = abs(A_w1 - A_w1_tests)

    if len(diff) > 0:
      magic = np.where(diff == min(diff))

      return ebvs[magic]

    else:
      return 0

ebvs = np.zeros(n)

for ii in range(n):
    ebvs[ii] = calc_ebvs(ra[ii], decl[ii], w1[ii], absw1[ii])

ra = ra*180./np.pi
decl = decl*180./np.pi

fout = open('candidate_outs_crich/ebvout_%i.dat' % iteration_num, 'w')

fmt = '%i %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n'
for ii in range(n):
    fout.write(fmt % (wid[ii], ra[ii], decl[ii], gall[ii], galb[ii],
        w1[ii], w2[ii], w3[ii], w4[ii], w1err[ii], w2err[ii], w3err[ii], w4err[ii],
        w1snr[ii], w2snr[ii], w3snr[ii], w4snr[ii], pmra[ii], pmdec[ii], sigpmra[ii], sigpmdec[ii],
        j[ii], h[ii], k[ii], jerr[ii], herr[ii], kerr[ii],
        coljk[ii], colk3[ii], col12[ii], col23[ii], col34[ii], absw1[ii], ebvs[ii]))
        
fout.close()

tend = time.time()
tot = tend-tstart

print "Elapsed: %f seconds" % tot





