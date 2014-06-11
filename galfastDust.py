from scipy.interpolate import interp1d
from scipy.ndimage import map_coordinates
#import pyfits
from numpy import sin, cos, arcsin, sqrt, arctan2, degrees,\
                  log10, arange, radians, meshgrid, interp
from math import floor, ceil

from astropy import coordinates as coord
from astropy import units
from astropy.io import fits as pyfits
from numba import autojit

def read_dust_file(filename):
    hduList = pyfits.open(filename)
    hdr = hduList[0].header
    return hdr, hduList[0].data
    
def lambert_deproject(x, y, lat0, long0):
    r = sqrt(x*x + y*y)
    c = 2.*arcsin(0.5*r)
    phi = arcsin(cos(c)*sin(long0) + y*sin(c)*cos(long0)/r) if r != 0. else long0
    l = lat0 + (arctan2(x*sin(c), r*cos(long0)*cos(c) - y*sin(long0)*sin(c)) if r != 0. else 0.)
    return phi, l

def lambert_project(lat, long, lat0, long0):
    d = 1 + sin(lat0)*sin(lat) + cos(lat0)*cos(lat)*cos(long-long0)
    kp = sqrt(2./d)
    x = kp*cos(lat)*sin(long-long0)
    y = kp*(cos(lat0)*sin(lat) - sin(lat0)*cos(lat)*cos(long-long0))
    return x,y

def dist2Dm(dist_kpc):
    return 5.*log10(dist_kpc*1000.) - 5.

def dm2Dist(dm):
    return (10**((dm+5.)/5.))/1000.

def interpolate(x, y, z, data, hdr):
    ix = [floor(z), ceil(z)]
    if z > hdr['NAXIS3'] - 1:
        return map_coordinates(data[-1], [[y],[x]])[0]
    elif z < 1.:
        v1 = [0.,]
        v2 = map_coordinates(data[0], [[y],[x]])
    else:
        v1 = map_coordinates(data[floor(z)-1], [[y],[x]])
        v2 = map_coordinates(data[ceil(z)-1], [[y],[x]])
    return interp1d(ix, [v1[0],v2[0]])(z)

def getDustValue(glat, glong, dist, northMap=read_dust_file("dust_data/makeArTableForMarioanorth021810.fits"), 
                                    southMap=read_dust_file("dust_data/makeArTableForMarioasouth021710.fits")):
    """
    glat -- array of galactic latitudes in radians
    glong -- array of glactic longitudes in radians
    dist -- array of distances in kpc
    northMap -- data for the North Galactic cap
    southMap -- data for the South Galactic cap
    """
    retEbv = []
    i = 0
    for lat, long, d in zip(glat, glong, dist):
        dm = dist2Dm(d)

        if lat > 0:
            dustmap = northMap
        else:
            dustmap = southMap
        xdim = dustmap[0]['NAXIS1']
        ydim = dustmap[0]['NAXIS2']
        zdim = dustmap[0]['NAXIS3']
        dx = dustmap[0]['CDELT1']
        dy = dustmap[0]['CDELT2']
        dz = dustmap[0]['CDELT3']
        lat0 = dustmap[0]['PHI1']
        long0 = dustmap[0]['LAMBDA0']
        centx = xdim/2.
        centy = ydim/2.
        x, y = lambert_project(lat, long, radians(lat0), radians(long0))
        ix = x/dx + centx - 0.5
        iy = y/dy + centy - 0.5
        iz = dm/dz
        a_r = interpolate(ix, iy, iz, dustmap[1], dustmap[0])
        retEbv.append(a_r/2.751) #Convert to ebv
        i += 1
    return retEbv

def eqToGal(ras, decs):
    glons = []
    glats = []
    for ra, dec in zip(ras, decs):
        c = coord.ICRSCoordinates(ra=ra, dec=dec, unit=(units.radian, units.radian))
        g = c.galactic
        glons.append(g.l.radians)
        glats.append(g.b.radians)
    return glats, glons

if __name__ == "__main__":
    grid = meshgrid(arange(-90, 150, 60), arange(0,390,60))
    dist = arange(0.001, 150., 150./len(grid[0].flatten()))

    glats, glons = eqToGal(radians(grid[1].flatten()), radians(grid[0].flatten()))
    ebvs = getDustValue(glats, glons, dist)
    print "glat glon ra dec ebv dist"
    for x, y, r, de, e, d in zip(degrees(glats), degrees(glons), grid[1].flatten(), grid[0].flatten(), ebvs, dist):
        print x,y,r,de,e,d
