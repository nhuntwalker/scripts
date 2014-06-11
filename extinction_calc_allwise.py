import numpy as np
import galfastDust as ext
import os
import pickle
import sys

f = 'known_agbs_with_absmags.p'
alldata = pickle.load(open(f))

n = 4246

X = np.zeros(len(alldata.keys()), dtype=np.ndarray)
for i in range(len(alldata.keys())):
	X[i] = alldata[np.sort(alldata.keys())[i]]

absw1, catid, col12, col23, col34, coljk, colk3, decl, galb, gall, h, herr, j, jerr, k, kerr, mrad, ra, w1, w1err, w1snr, w2, w2err, w2snr, w3, w3err, w3snr, w4, w4err, w4snr = X
ra = ra*np.pi/180.
decl = decl*np.pi/180.

dataset = eval(sys.argv[1])
lo = n*dataset
hi = n*(dataset + 1)

def calc_ebvs(ra,decl,w1,absw1):
    absw1 = absw1.mean()
    sig = w1 - absw1
    
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

for ii in range(lo,hi):
    ebvs[ii-lo] = calc_ebvs(ra[ii], decl[ii], w1[ii], absw1[ii])

alldata = {'catid':catid[lo:hi], 'ra':ra[lo:hi], 'decl':decl[lo:hi],
               'gall':gall[lo:hi], 'galb':galb[lo:hi], 'w1':w1[lo:hi], 'w2':w2[lo:hi],
               'w3':w3[lo:hi], 'w4':w4[lo:hi], 'w1err':w1err[lo:hi], 'w2err':w2err[lo:hi],
               'w3err':w3err[lo:hi], 'w4err':w4err[lo:hi], 'w1snr':w1snr[lo:hi],
               'w2snr':w2snr[lo:hi], 'w3snr':w3snr[lo:hi], 'w4snr':w4snr[lo:hi],
               'j':j[lo:hi], 'h':h[lo:hi], 'k':k[lo:hi], 'jerr':jerr[lo:hi], 'herr':herr[lo:hi],
               'kerr':kerr[lo:hi], 'mrad':mrad[lo:hi], 'coljk':coljk[lo:hi],
               'colk3':colk3[lo:hi], 'col12':col12[lo:hi], 'col23':col23[lo:hi],
               'col34':col34[lo:hi], 'absw1':absw1[lo:hi], 'ebvs':ebvs}

pickle.dump(alldata, open('ebvs_out%i.dat' % dataset, 'w'))

