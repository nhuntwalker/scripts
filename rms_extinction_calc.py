import numpy as np
import galfastDust as ext

def return_ebv(ra,decl,DMarry):

  ra_arry = ra*np.pi/180.
  dec_arry = decl*np.pi/180.

  dist_arry = 10**((DMarry+5.)/5.)/1E3 #convert DM to kpc

  glats, glons = ext.eqToGal(ra_arry, dec_arry)
  ebvs = np.array(ext.getDustValue(glats, glons, dist_arry))

  return ebvs
