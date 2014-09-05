import os 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.ticker import NullFormatter
import pandas as pd
from pandas import DataFrame as df
import scipy.stats.mstats as sp
from scipy import linalg
from scipy.stats import norm
from scipy.optimize import curve_fit
import locale
locale.setlocale(locale.LC_ALL, 'en_US')

# %matplotlib inline

matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['text.usetex'] = True

font = {'family':'normal', 'size':10}
axes = {'titlesize':14}
matplotlib.rc('font', **font)
matplotlib.rc('axes', **axes)


crich_indir = '/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/allwise_relaxed/candidates_relaxed/candidate_outs_crich/'
orich_indir = '/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/allwise_relaxed/candidates_relaxed/candidate_outs_orich/'

crich_files = [crich_indir+f for f in os.listdir(crich_indir) if f.endswith('.dat')]
orich_files = [orich_indir+f for f in os.listdir(orich_indir) if f.endswith('.dat')]

crich_df = pd.io.parsers.read_table(crich_files[0], sep='\t')
orich_df = pd.io.parsers.read_table(orich_files[0], sep='\t')

for ii in range(1,len(crich_files)):
    newdf = pd.io.parsers.read_table(crich_files[ii], sep='\t')
    crich_df = pd.concat([crich_df,newdf])

for ii in range(1,len(orich_files)):
    newdf = pd.io.parsers.read_table(orich_files[ii], sep='\t')
    orich_df = pd.concat([orich_df,newdf])

coeff = [0.34,0.21,0.15,0.11,0.09,0.13,0.13] # j,h,k,w1,w2,w3,w4

## Extinction and distances
crich_df['Av'] = 3.1*crich_df.ebvs
crich_df['Ar'] = 2.751*crich_df.ebvs
crich_df['Aj'] = coeff[0]*2.751*crich_df.ebvs
crich_df['Ah'] = coeff[1]*2.751*crich_df.ebvs
crich_df['Ak'] = coeff[2]*2.751*crich_df.ebvs
crich_df['Aw1'] = coeff[3]*2.751*crich_df.ebvs
crich_df['Aw2'] = coeff[4]*2.751*crich_df.ebvs
crich_df['Aw3'] = coeff[5]*2.751*crich_df.ebvs
crich_df['Aw4'] = coeff[6]*2.751*crich_df.ebvs
crich_df['DM'] = crich_df.w1 - crich_df.absw1 - crich_df.Aw1
crich_df['dist'] = 10**((crich_df['DM']+5.)/5.)/1E3 #kpc

## De-reddened colors
crich_df['J-H'] = (crich_df.j - crich_df.h) - (crich_df.Aj - crich_df.Ah)
crich_df['H-K'] = (crich_df.h - crich_df.k) - (crich_df.Ah - crich_df.Ak)
crich_df['K-W1'] = (crich_df.k - crich_df.w1) - (crich_df.Ak - crich_df.Aw1)
crich_df['W1-W2'] = (crich_df.w1 - crich_df.w2) - (crich_df.Aw1 - crich_df.Aw2)
crich_df['W2-W3'] = (crich_df.w2 - crich_df.w3) - (crich_df.Aw2 - crich_df.Aw3)
crich_df['W3-W4'] = (crich_df.w3 - crich_df.w4) - (crich_df.Aw3 - crich_df.Aw4)
crich_df['J-K'] = (crich_df.j - crich_df.k) - (crich_df.Aj - crich_df.Ak)
crich_df['K-W3'] = (crich_df.k - crich_df.w3) - (crich_df.Ak - crich_df.Aw3)

## Extinction and distances
orich_df['Av'] = 3.1*orich_df.ebvs
orich_df['Ar'] = 2.751*orich_df.ebvs
orich_df['Aj'] = coeff[0]*2.751*orich_df.ebvs
orich_df['Ah'] = coeff[1]*2.751*orich_df.ebvs
orich_df['Ak'] = coeff[2]*2.751*orich_df.ebvs
orich_df['Aw1'] = coeff[3]*2.751*orich_df.ebvs
orich_df['Aw2'] = coeff[4]*2.751*orich_df.ebvs
orich_df['Aw3'] = coeff[5]*2.751*orich_df.ebvs
orich_df['Aw4'] = coeff[6]*2.751*orich_df.ebvs
orich_df['DM'] = orich_df.w1 - orich_df.absw1 - orich_df.Aw1
orich_df['dist'] = 10**((orich_df['DM']+5.)/5.)/1E3 #kpc

## De-reddened colors
orich_df['J-H'] = (orich_df.j - orich_df.h) - (orich_df.Aj - orich_df.Ah)
orich_df['H-K'] = (orich_df.h - orich_df.k) - (orich_df.Ah - orich_df.Ak)
orich_df['K-W1'] = (orich_df.k - orich_df.w1) - (orich_df.Ak - orich_df.Aw1)
orich_df['W1-W2'] = (orich_df.w1 - orich_df.w2) - (orich_df.Aw1 - orich_df.Aw2)
orich_df['W2-W3'] = (orich_df.w2 - orich_df.w3) - (orich_df.Aw2 - orich_df.Aw3)
orich_df['W3-W4'] = (orich_df.w3 - orich_df.w4) - (orich_df.Aw3 - orich_df.Aw4)
orich_df['J-K'] = (orich_df.j - orich_df.k) - (orich_df.Aj - orich_df.Ak)
orich_df['K-W3'] = (orich_df.k - orich_df.w3) - (orich_df.Ak - orich_df.Aw3)

## W3-W4 modified by removing slope
#orich_df['W3-W4cor'] = orich_df['W3-W4'] - 0.722*orich_df['W2-W3']
the_slope = np.polyfit(orich_df['W2-W3'],orich_df['W3-W4'],deg=1)
orich_df['W3-W4cor'] = orich_df['W3-W4'] - the_slope[0]*orich_df['W2-W3']

glon = crich_df.gall*np.pi/180.
glat = crich_df.galb*np.pi/180.

dbulge = 8.0 #kpc

the_sun = df({'X':[dbulge], 'Y':[0.], 'Z':[0.], 'R':[dbulge]})

crich_df['X'] = dbulge - crich_df.dist*np.cos(glon)*np.cos(glat)
crich_df['Y'] = -crich_df.dist*np.sin(glon)*np.cos(glat)
crich_df['Z'] = crich_df.dist*np.sin(glat)
crich_df['R'] = np.sqrt(crich_df.X**2 + crich_df.Y**2)

glon = orich_df.gall*np.pi/180.
glat = orich_df.galb*np.pi/180.

orich_df['X'] = dbulge - orich_df.dist*np.cos(glon)*np.cos(glat)
orich_df['Y'] = -orich_df.dist*np.sin(glon)*np.cos(glat)
orich_df['Z'] = orich_df.dist*np.sin(glat)
orich_df['R'] = np.sqrt(orich_df.X**2 + orich_df.Y**2)

def plot_xy(dataframe, cut=None, title=None, scatter='no', savename=None, contours=False):
    if type(cut) != type(None):
        dataframe = dataframe[cut]
    
    x = dataframe.X
    y = dataframe.Y
    
    fig = plt.figure(figsize=(8,8))
    fig.subplots_adjust(wspace=0,hspace=0)
    if title != None:
        plt.suptitle(title)

    ## If contours are enabled or if the plot is a histogram, they'll still use the same gridding
    if contours != False or scatter=='no':
        dlev = 0.75
        levs = np.arange(0,3.5+dlev,dlev)
        dh = 401
        
        xbins = np.linspace(-100,100,dh)
        ybins = np.linspace(-100,100,dh)
        zbins = np.linspace(-100,100,dh)
        H, xedges, yedges = np.histogram2d(x,y,bins=(xbins,ybins))
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    ax = plt.subplot(111)
    ## In the event of scatter, use this!
    if scatter == 'yes':
        ax.scatter(x,y,s=5,edgecolor='None',c='k')
       
    ## If it's not a scatter plot, it's a 2d histogram
    else:        
        ax.imshow(np.log10(H.T), extent=extent, aspect='auto', interpolation='nearest', origin='lower', cmap=plt.cm.cubehelix_r, vmax=3.5)

    ## If we want to put contours on it...
    if contours != False:
        im = ax.contour(np.log10(H.T), extent=extent, cmap=plt.cm.Reds_r, levels=levs)
        
    ax.scatter(the_sun.X,the_sun.Y,s=50,c='y')
    radii = np.linspace(5,60,6)
    circlist = []
    for i in range(len(radii)):
        circlist.append(plt.Circle((0,0),radii[i], fill=False, color="grey",alpha=0.5))
    ax1 = plt.gca()
    for i in range(len(radii)):
        fig.gca().add_artist(circlist[i])
    ax.plot([-1E5,1E5],[0,0],linestyle='--', color='grey')
    ax.plot([0,0],[-1E5,1E5],linestyle='--', color='grey')

    ax.text(0.9,0.9,'# Objects: %i' % len(x),
            horizontalalignment='right',verticalalignment='top',transform=ax.transAxes)    

    ax.set_xlim(-39,39)
    ax.set_ylim(-39,39)
    ax.set_xlabel('X (kpc)')
    ax.set_ylabel('Y (kpc)')
    ax.minorticks_on()
    
    if savename != None:
        plt.savefig(savename)

    plt.show()

def plot_vertical_cross_section(dataframe, horizontal_axis='X', cut=None, title=None, scatter='no', savename=None, contours=False):
    if type(cut) != type(None):
        dataframe = dataframe[cut]
    
    horizontal_axis = horizontal_axis.upper()
    
    h_axis = dataframe[horizontal_axis]
    z = dataframe.Z
    
    fig = plt.figure(figsize=(8,3))
    fig.subplots_adjust(wspace=0,hspace=0,right=0.9)
    if title != None:
        plt.suptitle(title)
    
    ax = plt.subplot(111)

    ## If contours are enabled or if the plot is a histogram, they'll still use the same gridding
    if contours != False or scatter=='no':
        dlev = 0.75
        levs = np.arange(0,3.5+dlev,dlev)
        dh = 0.1
        
        xbins = np.arange(-40,40+dh,dh)
        zbins = np.arange(-20,20+0.1,0.1)
        H, xedges, yedges = np.histogram2d(h_axis,z,bins=(xbins,zbins))
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    ## In the event of scatter, use this!
    if scatter == 'yes':
        ax.scatter(h_axis,z,s=5,edgecolor='None',c='k')
       
    ## If it's not a scatter plot, it's a 2d histogram
    else:        
        im = ax.imshow(np.log10(H.T), extent=extent, aspect='auto', interpolation='nearest', origin='lower', cmap=plt.cm.Greys)
        cax = fig.add_axes([0.91,0.125,0.03,0.775])
        cbar = fig.colorbar(im, cax=cax)
        cbar.ax.set_ylabel('log$_{10}$(N)')

    ## If we want to put contours on it...
    if contours != False:
        ax.contour(np.log10(H.T), extent=extent, cmap=plt.cm.Reds_r, levels=levs)
        
    ax.scatter(the_sun[horizontal_axis],the_sun.Z,s=50,c='y')
    radii = np.linspace(20,60,3)

    for ii in np.arange(-100,101,20):
        ax.plot([ii,ii],[-100,100],color='#40FF00')
    
    ax.plot([-1E5,1E5],[0,0],linestyle='--', color='grey')
    ax.plot([0,0],[-1E5,1E5],linestyle='--', color='grey')
    
    if horizontal_axis.upper() == 'R':
        ax.set_xlim(0,15)
    else:
        ax.set_xlim(-15,15)
    ax.set_ylim(-2,2)
    ax.set_yticks(np.arange(-3,3.1,0.5))
    ax.set_xlabel(horizontal_axis+' (kpc)')
    ax.set_ylabel('Z (kpc)')
    ax.minorticks_on()
        
    if savename != None:
        plt.savefig(savename)

    plt.show()

def plot_vertical_slices(dataframe, cut=None, title=None, scatter='no', savename=None, contours=False):
    #pieces of Z:
    # 0->0.3, 0.3->0.5, 0.5->1.0, 1.0->2.0, 2.0->5.0
    zarray = [-5.0,-2.0,-1.0,-0.5,-0.3,0.0,0.3,0.5,1.0,2.0,5.0]
    
    if type(cut) != type(None):
        dataframe = dataframe[cut]

    x = dataframe.X
    y = dataframe.Y
    z = dataframe.Z
    
    dlev = 0.75
    levs = np.arange(0,3.5+dlev,dlev)
    dh = 401
    
    xbins = np.linspace(-100,100,dh)
    ybins = np.linspace(-100,100,dh)
    zbins = np.linspace(-100,100,dh)

    fig = plt.figure(figsize=(14,6))
    fig.subplots_adjust(hspace=0, wspace=0, top=0.95, left=0.05, right=0.9, bottom=0.1)
    if title != None:
        plt.suptitle(title)
    
    for ii in range(len(zarray)-1):
        zhi = zarray[ii+1]
        zlo = zarray[ii]
        select = (z < zhi) & (z >= zlo)
        
        ax = plt.subplot(2,5,ii+1)
        H, xedges, yedges = np.histogram2d(x[select],y[select],bins=(xbins,ybins))
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    
        ## sample
        ax.scatter(x[select], y[select],s=1,edgecolor='None',c='k')
        ax.scatter(the_sun.X,the_sun.Y,s=50,c='y')
        
        ## contours
        if contours == True:
            im = ax.contour(np.log10(H.T), extent=extent, cmap=plt.cm.Reds_r, levels=levs)
        
        ## crosshairs on (0,0)
        ax.plot([-1E5,1E5],[0,0],linestyle='--', color='grey'); plt.plot([0,0],[-1E5,1E5],linestyle='--', color='grey')
        ax.text(0.9,0.1,'%.1f $\le$ z $<$ %.1f kpc' % (zlo, zhi), horizontalalignment='right', transform=ax.transAxes)
        
        ax.set_xlim(-39,39)
        ## Flip the Y-axis
        ax.set_ylim(39,-39)
        if ii > 4:
            ax.set_xlabel('X (kpc)')
        if ii in [0,5]:
            ax.set_ylabel('Y (kpc)')
        else:
            ax.yaxis.set_major_formatter(NullFormatter())
        ax.minorticks_on()
    
    if savename != None:
        plt.savefig(savename)
        
    plt.show()

def plot_xy_with_subregions(dataframe, cut=None, slopes=None, title=None, savename=None, contours=False):
    if type(cut) != type(None):
        dataframe = dataframe[cut]

    x = dataframe.X
    y = dataframe.Y
    z = dataframe.Z
    
    if slopes == None:
        slopes = [-np.inf,-1,1,np.inf]
    
    dlev = 0.75
    levs = np.arange(0,3.5+dlev,dlev)

    ## Plot to confirm
    dh = 401
    xbins = np.linspace(-100,100,dh)
    ybins = np.linspace(-100,100,dh)
    
    fig = plt.figure(figsize=(6,6))
    if title != None:
        plt.suptitle(title)

    ## contours
    if contours == True:
        H, xedges, yedges = np.histogram2d(x,y,bins=(xbins,ybins))
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        im = plt.contour(np.log10(H.T), extent=extent, cmap=plt.cm.Reds_r, levels=levs)

    plt.subplot(111)
    plt.scatter(x,y,s=1,edgecolor='None',c='k')
    
    the_colors = ['#00FF40','b','r','y','orange','#00FF40','b','r','y','orange']
    for ii in range(len(slopes)-1):
    
        slope1 = slopes[ii]
        slope2 = slopes[ii+1]

        select = (y > slope1*x) & (y < slope2*x)
    
        ## sample
        plt.scatter(x[select], y[select],s=1,edgecolor='None',c=the_colors[ii])
        plt.scatter(the_sun.X,the_sun.Y,s=50,c='y')
        
    ## crosshairs on (0,0)
    plt.plot([-1E5,1E5],[0,0],linestyle='--', color='grey'); plt.plot([0,0],[-1E5,1E5],linestyle='--', color='grey')
    
    plt.xlim(-39,39)
    ## Flip the Y-axis
    plt.ylim(39,-39)
    plt.xlabel('X (kpc)'); plt.ylabel('Y (kpc)')
    plt.minorticks_on()
    
    if savename != None:
        plt.savefig(savename)
    
    plt.show()


def plot_three_sections(dataframe, cut=None, slopes=None, title=None, savename=None, contours=False):    
    if type(cut) != type(None):
        dataframe = dataframe[cut]

    ## Plot 2D histograms of height vs radius
    x = dataframe.X
    y = dataframe.Y
    z = dataframe.Z
    r = dataframe.R

    select1 = (y < -1*x) & (x > 0) ## green
    select2 = (y < 1*x) & (y > -1*x) ## blue
    select3 = (y > 1*x) & (x > 0) ## red

    ## Setup for the histo
    dr = 0.2 # steps of 0.1 kpc or 100 pc in galactocentric radius
    dz = 0.1 # steps of 0.05 kpc or 50 pc in height
    vmax = 2.5
    
    radbins = np.arange(0,30+dr,dr)
    zbins = np.arange(-20,20+dz,dz)
    
    H1, xed, yed = np.histogram2d(r[select1], z[select1], bins=(radbins,zbins))
    H2, xed, yed = np.histogram2d(r[select2], z[select2], bins=(radbins,zbins))
    H3, xed, yed = np.histogram2d(r[select3], z[select3], bins=(radbins,zbins))
    extent = [xed[0],xed[-1],yed[0],yed[-1]]
    
    ## The plot
    fig = plt.figure(figsize=(6,8))
    fig.subplots_adjust(hspace=0, right=0.85)
    ax = plt.subplot(311)
    im = ax.imshow(np.log10(H1.T), extent=extent, origin='lower',aspect='auto',interpolation='nearest',cmap=plt.cm.Greens, vmax=vmax)
    ax.minorticks_on()
    
    ax.plot([0,15],[0,0],color='k',linestyle='--')
    ax.set_xlabel('Radius (kpc)'); ax.set_ylabel('Z (kpc)')
    ax.set_xlim(0,15); ax.set_ylim(-2,2)
    ax.xaxis.set_major_formatter(NullFormatter())
    
    cax = fig.add_axes([0.86,0.67,0.03,0.2])
    cbar = fig.colorbar(im, cax=cax)
    cbar.ax.set_ylabel('log$_{10}$(N)')
    ax.minorticks_on()
    
    ax = plt.subplot(312)
    im = ax.imshow(np.log10(H2.T), extent=extent, origin='lower',aspect='auto',interpolation='nearest',cmap=plt.cm.Blues, vmax=vmax)
    ax.minorticks_on()
    
    ax.scatter(the_sun.X, the_sun.Y, s=50,c='y')
    ax.plot([0,15],[0,0],color='k',linestyle='--')
    ax.set_xlabel('Radius (kpc)'); ax.set_ylabel('Z (kpc)')
    ax.set_xlim(0,15); ax.set_ylim(-2,2)
    ax.xaxis.set_major_formatter(NullFormatter())
    
    cax = fig.add_axes([0.86,0.41,0.03,0.2])
    cbar = fig.colorbar(im, cax=cax)
    cbar.ax.set_ylabel('log$_{10}$(N)')
    ax.minorticks_on()
    
    ax = plt.subplot(313)
    im = ax.imshow(np.log10(H3.T), extent=extent, origin='lower',aspect='auto',interpolation='nearest',cmap=plt.cm.Reds, vmax=vmax)
    ax.minorticks_on()
    
    ax.plot([0,15],[0,0],color='k',linestyle='--')
    ax.set_xlabel('Radius (kpc)'); ax.set_ylabel('Z (kpc)')
    ax.set_xlim(0,15); ax.set_ylim(-2,2)
    
    cax = fig.add_axes([0.86,0.15,0.03,0.2])
    cbar = fig.colorbar(im, cax=cax)
    cbar.ax.set_ylabel('log$_{10}$(N)')
    ax.minorticks_on()
    
    if savename != None:
        plt.savefig(savename)
    
    plt.show()


def plot_radial_vertical_profile(dataframe, cut=None, title=None, savename=None):
    if type(cut) != type(None):
        dataframe = dataframe[cut]
    
    x = dataframe.X
    y = dataframe.Y
    z = dataframe.Z
    r = dataframe.R

    ## Plot histogram of radii in steps of 1 kpc; all radii
    fig = plt.figure(figsize=(14,10))
    fig.subplots_adjust(hspace=0)
    ax = plt.subplot(221)
    dr = 0.25
    radbins = np.arange(0,30+dr,dr)
    
    H, edges = np.histogram(r, bins=radbins)
    xvals = edges[:-1] + dr/2.
    
    ax.plot(xvals, H, marker='_', markersize=10)
    ax.text(0.9,0.9,'For all $|Z|$\nin the blue region', transform=ax.transAxes, 
            horizontalalignment='right')
    ax.set_xlabel('Radius (kpc)')
    ax.set_ylabel('N/N$_{tot}$')
    ax.set_yscale('log')
    ax.minorticks_on()
    
    ## Same as above, but for 4 vertical bins
    ax = plt.subplot(223)
    dz = 0.2
    ntimes = 5
    zcut = np.linspace(0,ntimes*dz,ntimes)
    legendlist = []
    
    for ii in range(len(zcut)-1):
        smallrange = (abs(z) < zcut[ii+1]) & (abs(z) > zcut[ii])
        H, edges = np.histogram(r[smallrange], bins=radbins)
        xvals = edges[:-1] + dr/2.
        
        ax.plot(xvals, H, markersize=5)
        legendlist.append('%.2f $< |Z| <$ %.2f' % (zcut[ii], zcut[ii+1]))
        
    ax.legend(legendlist)
    ax.set_xlabel('Radius (kpc)')
    ax.set_ylabel('N')
    ax.set_yscale('log')
    ax.minorticks_on()
    
    ## Plot histogram of height in steps of 0.2 kpc
    ax = plt.subplot(222)
    dz = 0.2
    zbins = np.arange(0,20+dz,dz)
    
    H, edges = np.histogram(abs(z), bins=zbins)
    xvals = edges[:-1] + dz/2.
    
    ax.plot(xvals, H, marker='_', markersize=10, markerfacecolor='k')
    ax.text(0.9,0.9,'For all radii',
            horizontalalignment='right',transform=ax.transAxes)
    ax.set_xlabel('$|Z|$ (kpc)')
    ax.set_ylabel('N')
    ax.set_xlim(0,5)
    ax.set_yscale('log')
    ax.minorticks_on()
    
    ## Same as above, but for 5 radial bins
    ax = plt.subplot(224)
    dr = 5
    ntimes = 6
    radcut = np.linspace(0,15,ntimes)
    legendlist = []
    
    for ii in range(len(zcut)):
        smallrange = (r < radcut[ii+1]) & (r > radcut[ii])
        H, edges = np.histogram(abs(z)[smallrange], bins=zbins)
        xvals = edges[:-1] + dz/2.
        
        ax.plot(xvals, H, marker='_', markersize=10, markerfacecolor='k')
        legendlist.append('%.2f $< R <$ %.2f kpc' % (radcut[ii], radcut[ii+1]))
        
    ax.legend(legendlist)
    ax.set_xlabel('$|Z|$ (kpc)')
    ax.set_ylabel('N')
    ax.set_xlim(0,5)
    ax.set_yscale('log')
    ax.minorticks_on()
    
    plt.show()

def plot_photometry(dataframe,xlabels,ylabels,cut=None,histo=True,contours=False,yaxismag=True,cmap=plt.cm.Greys):
    if type(cut) != type(None):
        dataframe = dataframe[cut]
    
    xdata = dataframe[xlabels]
    ydata = dataframe[ylabels]
    
    fig = plt.figure(figsize=(4,4))
    ax = plt.subplot(111)
    xspan = sp.mquantiles(np.array(xdata),[0.001,0.999])
    yspan = sp.mquantiles(np.array(ydata),[0.001,0.999])

    if histo == False:
        ax.scatter(xdata,ydata,s=1,edgecolor='None',c='k')
    else:
        xbins = np.linspace(np.round(xspan[0],1), np.round(xspan[1],1) + 0.1,101)
        ybins = np.linspace(np.round(yspan[0],1), np.round(yspan[1],1) + 0.1,101)
        H, xed, yed = np.histogram2d(xdata,ydata,bins=(xbins,ybins))
        extent=[xed[0],xed[-1],yed[0],yed[-1]]
        ax.imshow(np.log10(H.T), extent=extent, interpolation='nearest', aspect='auto', origin='lower', cmap=cmap)
    
    if contours != False:
        xbins = np.linspace(np.round(xspan[0],1), np.round(xspan[1],1) + 0.1,101)
        ybins = np.linspace(np.round(yspan[0],1), np.round(yspan[1],1) + 0.1,101)
        H, xed, yed = np.histogram2d(xdata,ydata,bins=(xbins,ybins))
        allquants = np.log10(H.ravel())
        #levels = np.linspace(0,max(allquants),7)[1:-1]
        levels = [0.5,1.0,1.5,2.0,2.5]
        extent=[xed[0],xed[-1],yed[0],yed[-1]]
        im = ax.contour(np.log10(H.T), extent=extent, interpolation='nearest', aspect='auto', origin='lower', colors='r',levels=levels)            
        
        cax = fig.add_axes([0.925, 0.125, 0.05, 0.775]) 
        cbar = plt.colorbar(im, cax = cax)  
        cbar.ax.set_ylabel('log$_{10}$(N)')
    
    ax.set_xlim(np.round(xspan[0],1), np.round(xspan[1],1) + 0.1)
    if yaxismag == True:
        ax.set_ylim(np.round(yspan[1],1) + 0.1,np.round(yspan[0],1))
    else:
        ax.set_ylim(np.round(yspan[0],1), np.round(yspan[1],1) + 0.1)
    ax.set_xlabel(xlabels)
    ax.set_ylabel(ylabels)
    ax.minorticks_on()
                
    plt.show()

def plot_xy_with_color_color(dataframe,xlabels,ylabels,cut=None,histo=True,contours=False,scatter='no',title=None,cmap=plt.cm.Greys,savename='None',xbounds='auto',ybounds='auto'):
    original_df = dataframe
    
    if type(cut) != type(None):
        dataframe = dataframe[cut]
    
    x = dataframe.X
    y = dataframe.Y
    
    fig = plt.figure(figsize=(12,5))
    fig.subplots_adjust(wspace=0.2,hspace=0)
    if title != None:
        plt.suptitle(title)

    ## If contours are enabled or if the plot is a histogram, they'll still use the same gridding
    if contours != False or scatter=='no':
        dlev = 0.75
        levs = np.arange(0,3.5+dlev,dlev)
        dh = 401
        
        xbins = np.linspace(-100,100,dh)
        ybins = np.linspace(-100,100,dh)
        zbins = np.linspace(-100,100,dh)
        H, xedges, yedges = np.histogram2d(x,y,bins=(xbins,ybins))
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    ax = plt.subplot(121)
    ## In the event of scatter, use this!
    if scatter == 'yes':
        ax.scatter(x,y,s=5,edgecolor='None',c='k')
       
    ## If it's not a scatter plot, it's a 2d histogram
    else:        
        ax.imshow(np.log10(H.T), extent=extent, aspect='auto', interpolation='nearest', origin='lower', cmap=plt.cm.cubehelix_r, vmax=3.5)

    ## If we want to put contours on it...
    if contours != False:
        im = ax.contour(np.log10(H.T), extent=extent, cmap=plt.cm.Reds_r, levels=levs)
        
    ax.scatter(the_sun.X,the_sun.Y,s=50,c='y')
    radii = np.linspace(20,60,3)
    circlist = []
    for i in range(len(radii)):
        circlist.append(plt.Circle((0,0),radii[i], color='#40FF00', fill=False))
    ax1 = plt.gca()
    for i in range(len(radii)):
        fig.gca().add_artist(circlist[i])
    ax.plot([-1E5,1E5],[0,0],linestyle='--', color='grey')
    ax.plot([0,0],[-1E5,1E5],linestyle='--', color='grey')

    ax.text(0.9,0.9,'# Objects: %i' % len(x),
            horizontalalignment='right',verticalalignment='top',transform=ax.transAxes)    

    ax.set_xlim(-14,14)
    ax.set_ylim(-14,14)
    ax.set_xlabel('X (kpc)')
    ax.set_ylabel('Y (kpc)')
    ax.minorticks_on()
    

    xdata = dataframe[xlabels]
    ydata = dataframe[ylabels]
    
    ax = plt.subplot(122)
    xspan = sp.mquantiles(np.array(xdata),[0.001,0.999])
    yspan = sp.mquantiles(np.array(ydata),[0.001,0.999])

    xspan_orig = sp.mquantiles(np.array(original_df[xlabels]),[0.001,0.999])
    yspan_orig = sp.mquantiles(np.array(original_df[ylabels]),[0.001,0.999])
    
    if histo == False:
        ax.scatter(xdata,ydata,s=1,edgecolor='None',c='k')
    else:
        xbins_orig = np.linspace(np.round(xspan_orig[0],1), np.round(xspan_orig[1],1) + 0.1,101)
        ybins_orig = np.linspace(np.round(yspan_orig[0],1), np.round(yspan_orig[1],1) + 0.1,101)
        H_orig, xed_orig, yed_orig = np.histogram2d(original_df[xlabels], original_df[ylabels], bins=(xbins_orig,ybins_orig))
        extent_orig = [xed_orig[0],xed_orig[-1],yed_orig[0],yed_orig[-1]]
        ax.imshow(np.log10(H_orig.T), extent=extent_orig, interpolation='nearest', aspect='auto', origin='lower', cmap=plt.cm.Greys)

        xbins = np.linspace(np.round(xspan[0],1), np.round(xspan[1],1) + 0.1,101)
        ybins = np.linspace(np.round(yspan[0],1), np.round(yspan[1],1) + 0.1,101)
        H, xed, yed = np.histogram2d(xdata,ydata,bins=(xbins,ybins))
        extent=[xed[0],xed[-1],yed[0],yed[-1]]
        ax.imshow(np.log10(H.T), extent=extent, interpolation='nearest', aspect='auto', origin='lower', cmap=cmap)
    
    if contours != False:
        xbins = np.linspace(np.round(xspan[0],1), np.round(xspan[1],1) + 0.1,101)
        ybins = np.linspace(np.round(yspan[0],1), np.round(yspan[1],1) + 0.1,101)
        H, xed, yed = np.histogram2d(xdata,ydata,bins=(xbins,ybins))
        allquants = np.log10(H.ravel())
        #levels = np.linspace(0,max(allquants),7)[1:-1]
        levels = [0.5,1.0,1.5,2.0,2.5]
        extent=[xed[0],xed[-1],yed[0],yed[-1]]
        im = ax.contour(np.log10(H.T), extent=extent, interpolation='nearest', aspect='auto', origin='lower', colors='r',levels=levels)            
        
        cax = fig.add_axes([0.925, 0.125, 0.05, 0.775]) 
        cbar = plt.colorbar(im, cax = cax)  
        cbar.ax.set_ylabel('log$_{10}$(N)')
    
    if xbounds=='auto':
        ax.set_xlim(np.round(xspan[0],1), np.round(xspan[1],1) + 0.1)
    else:
        ax.set_xlim(xbounds[0], xbounds[1])
    if ybounds=='auto':
        ax.set_ylim(np.round(yspan[0],1), np.round(yspan[1],1) + 0.1)
    else:
        ax.set_ylim(ybounds[0], ybounds[1])
    
    ax.set_xlabel(xlabels)
    ax.set_ylabel(ylabels)
    ax.minorticks_on()


    if savename != None:
        plt.savefig(savename)

    plt.show()

# plot_xy(orich_df,title="O-rich AGB Stars", contours=True)
# plot_xy(crich_df,title="C-rich AGB Stars", contours=True)

# plot_vertical_cross_section(orich_df, horizontal_axis='r', contours=True, title='O-rich AGB Stars')
# plot_vertical_cross_section(crich_df, horizontal_axis='r', contours=True, title='C-rich AGB Stars')

# plot_vertical_slices(orich_df,contours=True)

# plot_xy_with_subregions(orich_df,contours=True,title="O-rich AGB Stars")

select1 = (orich_df.Y < -orich_df.X) & (orich_df.X > 0) ## green
select2 = (orich_df.Y < orich_df.X) & (orich_df.Y > -orich_df.X) ## blue
select3 = (orich_df.Y > orich_df.X) & (orich_df.X > 0) ## red

# plot_three_sections(orich_df)

# plot_radial_vertical_profile(orich_df[select2])

# plot_xy_with_color_color(orich_df,xlabels='W2-W3',ylabels='W3-W4',cut=(orich_df['W3-W4'] < 0.3) & (orich_df.Z > 0.3) & (orich_df.Z < 3), xbounds=[0,3], ybounds=[-0.2,1.4], cmap=plt.cm.Reds, savename=None)
# plot_xy_with_color_color(orich_df,xlabels='W2-W3',ylabels='W3-W4',cut=(orich_df['W3-W4'] > 0.3) & (orich_df['W3-W4'] < 0.6) & (orich_df.Z > 0.3) & (orich_df.Z < 3), xbounds=[0,3], ybounds=[-0.2,1.4], cmap=plt.cm.Reds, savename=None)
# plot_xy_with_color_color(orich_df,xlabels='W2-W3',ylabels='W3-W4',cut=(orich_df['W3-W4'] > 0.6) & (orich_df['W3-W4'] < 0.9) & (orich_df.Z > 0.3) & (orich_df.Z < 3), xbounds=[0,3], ybounds=[-0.2,1.4], cmap=plt.cm.Reds, savename=None)
# plot_xy_with_color_color(orich_df,xlabels='W2-W3',ylabels='W3-W4',cut=(orich_df['W3-W4'] > 0.9) & (orich_df.Z > 0.3) & (orich_df.Z < 3), xbounds=[0,3], ybounds=[-0.2,1.4], cmap=plt.cm.Reds, savename=None)

# plot_vertical_cross_section(orich_df,horizontal_axis='Y',cut=(orich_df['W3-W4cor'] < 0.25))
# plot_vertical_cross_section(orich_df,horizontal_axis='Y',cut=(orich_df['W3-W4cor'] > 0.25) & (orich_df['W3-W4cor'] < 0.5))
# plot_vertical_cross_section(orich_df,horizontal_axis='Y',cut=(orich_df['W3-W4cor'] > 0.5) & (orich_df['W3-W4cor'] < 0.75))
# plot_vertical_cross_section(orich_df,horizontal_axis='Y',cut=(orich_df['W3-W4cor'] > 0.75))

# plot_vertical_cross_section(orich_df,horizontal_axis='X',cut=(orich_df['W3-W4cor'] < 0.25))
# plot_vertical_cross_section(orich_df,horizontal_axis='X',cut=(orich_df['W3-W4cor'] > 0.25) & (orich_df['W3-W4cor'] < 0.5))
# plot_vertical_cross_section(orich_df,horizontal_axis='X',cut=(orich_df['W3-W4cor'] > 0.5) & (orich_df['W3-W4cor'] < 0.75))
# plot_vertical_cross_section(orich_df,horizontal_axis='X',cut=(orich_df['W3-W4cor'] > 0.75))

def linear_func(x,a,b):
    ## Takes the linear coefficients 
    ## from the fit below and puts them 
    ## into an exponential function
    return np.exp(a*x + b)

def exponential_fit_coeffs(zvals, zcut=0.5):
    zvals = abs(zvals)
    
    ## Declare the z value to cut at, then declare two different populations of sources
    zabove = zvals > zcut
    zbelow = zvals <= zcut
    
    ## Histogram for objects above 0.5 kpc from the plane
    zbins = np.linspace(0.5,3.0,11)
    H1, ed1 = np.histogram(zvals[zabove], bins=zbins)
    dx1 = (ed1[1]-ed1[0])/2.
    mask = np.where(H1 != 0)
    if zcut == 0.5:
        the_first_fit = np.polyfit(ed1[:-1][mask]+dx1, np.log(H1[mask]/4.), deg=1)
    else:
        the_first_fit = np.polyfit(ed1[:-1][mask]+dx1, np.log(H1[mask]), deg=1)

    
    ## Histogram for objects below 0.5 kpc from the plane
    zbins = np.linspace(0,0.5,6)
    H2, ed2 = np.histogram(zvals[zbelow], bins=zbins) 
    dx2 = (ed2[1]-ed2[0])/2.
    mask = np.where(H2 != 0)
    if zcut == 0.5:
        the_second_fit = np.polyfit(ed2[:-1][mask]+dx2, np.log(H2[mask]/2.), deg=1)
    else:
        the_second_fit = np.polyfit(ed2[:-1][mask]+dx2, np.log(H2[mask]), deg=1)
    
    coeffs = [the_first_fit[0], the_first_fit[1], the_second_fit[0], the_second_fit[1]]
    
    ## Note, the coefficients returned are NOT scale height and normalization
    ## The coefficients are related, but aren't directly those values.
    ## scale heights are -1/coeffs[0] and -1/coeffs[2]
    ## normalizations are np.exp(coeffs[1]) and np.exp(coeffs[3]
    return coeffs

def plot_double_exponential_fit(dataframe, radialbin=7, cut=None, title=None, savename=None):
    ## Calculate vertical exponential fit for each radius bin and plot it up
    ## Can't do uniform bins for this sample because the sample size is just too small.
    ## Need to do separate fits for Z < 0.5 and Z > 0.5

    if type(cut) != type(None):
        dataframe = dataframe[cut]
    
    z = dataframe.Z
    r = dataframe.R

    dr = 1 #1 kpc radial bins
    radbins = np.arange(0,30+dr,dr)
    ii = radialbin
    
    radius_bin = (r > radbins[ii]) & (r < radbins[ii+1])
    zvals = z[radius_bin]
    rvals = r[radius_bin]
    
    dz = 0.1
    zbins = np.arange(0,5+dz,dz)
    H, ed = np.histogram(abs(zvals), bins=zbins)
    
    if ii >= 9:
        coeffs = exponential_fit_coeffs(zvals, zcut=1.0)
    else:
        coeffs = exponential_fit_coeffs(zvals)
    
    line1 = linear_func(zbins[:-1] + dz/2., coeffs[0], coeffs[1])
    line2 = linear_func(zbins[:-1] + dz/2., coeffs[2], coeffs[3])
    resultant = line1 + line2
    
    fig = plt.figure(figsize=(6,3))
    ax = plt.subplot(111)
    ax.scatter(zbins[:-1] + dz/2., H, marker='o',s=25) ## Plot the histogrammed values
    ax.plot(zbins[:-1] + dz/2., line1, color='r')
    ax.plot(zbins[:-1] + dz/2., line2, color='g')
    ax.plot(zbins[:-1] + dz/2., resultant, color ='k',linewidth=2) # the resultant line
    ax.text(0.9,0.8,'$%.2f < R < %.2f$ kpc\nThe Fit: z$_{h1}$ = %.2f kpc\nz$_{h2}$ = %.2f kpc' % (radbins[ii],radbins[ii+1],abs(1/coeffs[0]),abs(1/coeffs[2])), 
            transform=ax.transAxes, horizontalalignment='right',fontsize=8)
    ax.set_xlim(0,3); ax.set_ylim(1.0E0)
    ax.set_yscale('log')
    ax.set_xlabel('$|Z|$ (kpc)'); ax.set_ylabel('N')
    ax.minorticks_on()
    
    if savename != None:
        plt.savefig(savename)
    
    plt.show()

## produce megaplot of Z distributions for each radial bin
def plot_megaplot_radialbins(dataframe, title=None, savename=None):
    df1 = dataframe[select1]
    df2 = dataframe[select2]
    df3 = dataframe[select3]
    
    radii_1 = df1.R
    radii_2 = df2.R
    radii_3 = df3.R
    
    z_1 = df1.Z
    z_2 = df2.Z
    z_3 = df3.Z
    
    dr1 = 1.0
    dz = 0.1
    scalerads = np.arange(dr1,20+dr1,dr1)
    
    fig = plt.figure(figsize=(10,12))
    fig.subplots_adjust(hspace=0,left=0.05,right=0.95)
    
    for ii in range(len(scalerads)-1):
        zbins = np.arange(0,3+dz,dz)
        
        cut1 = (radii_1 > scalerads[ii]) & (radii_1 < scalerads[ii+1])
        zvals1 = z_1[cut1]
        
        cut2 = (radii_2 > scalerads[ii]) & (radii_2 < scalerads[ii+1])
        zvals2 = z_2[cut2]
     
        cut3 = (radii_3 > scalerads[ii]) & (radii_3 < scalerads[ii+1])
        zvals3 = z_3[cut3]
     
        H1, ed = np.histogram(zvals1, bins=zbins)
        H2, ed = np.histogram(zvals2, bins=zbins)
        H3, ed = np.histogram(zvals3, bins=zbins)
        
        insuff_counts = 0
        iters = 0
        
        if (0 in H1[:int(len(H1)*(2./3))]) or (0 in H2[:int(len(H2)*(2./3))]) or (0 in H3[:int(len(H3)*(2./3))]):
            insuff_counts = 1
            dz_new = dz
            iters += 1
        else:
            dz_new = dz
        
        if insuff_counts == 1:
            while (insuff_counts == 1) or (dz_new <= 0.5):
                iters += 1
                dz_new += 0.025
                zbins = np.arange(0,3+dz_new,dz_new)
                
                H1, ed = np.histogram(zvals1, bins=zbins)
                H2, ed = np.histogram(zvals2, bins=zbins)
                H3, ed = np.histogram(zvals3, bins=zbins)
                
                if (0 in H1[:int(len(H1)*(2./3))]) or (0 in H2[:int(len(H2)*(2./3))]) or (0 in H3[:int(len(H3)*(2./3))]):
                    insuff_counts = 1
                else:
                    insuff_counts = 0
                    
                
        ax = plt.subplot(len(scalerads)/4,4,ii+1)
        ax.plot(ed[:-1], np.log10(H1), color='#00FF40')
        ax.plot(ed[:-1], np.log10(H2), color='b')
        ax.plot(ed[:-1], np.log10(H3), color='r')
        
        ax.text(0.9,0.9,'R$_0$: %.2f kpc' % (scalerads[ii]), 
                horizontalalignment='right', verticalalignment='top', transform = ax.transAxes)
        ax.text(0.9,0.8,'dz: %.3f' % dz_new,
                horizontalalignment='right', verticalalignment='top', transform = ax.transAxes)
        ax.text(0.9,0.7,'N$_{tot}$: %i' % (len(zvals1)+len(zvals2)+len(zvals3)),
                horizontalalignment='right', verticalalignment='top', transform = ax.transAxes)
        ax.set_xlim(0.05,2.95)
        ax.set_ylim(0.01,3.4)
        if ii == 8:
            ax.set_ylabel('Log$_{10}$(N)')
        #ax.yaxis.set_major_formatter(NullFormatter())
        ax.minorticks_on()
    
    if savename != None:
        plt.savefig(savename)
    plt.show() 

# for ii in range(10):
#     plot_double_exponential_fit(orich_df[select2], radialbin=ii)

# for ii in range(10):
#     plot_double_exponential_fit(orich_df[select1], radialbin=ii)

# plot_megaplot_radialbins(orich_df)

def plot_scale_height_distribution(dataframe, cut=None, title=None, histcolor=plt.cm.Blues, savename=None):
    if type(cut) != type(None):
        dataframe = dataframe[cut]

    ## calculate and store scale heights for a given selection of stars
    dz = 0.1
    dr1 = 0.5
    dr2 = 1.0
    dr3 = 2.0
    dr4 = 5.0
    rbins1 = np.arange(0.0,7,dr1)
    rbins2 = np.arange(7,10,dr2)
    rbins3 = np.arange(10,20,dr3)
    rbins4 = np.arange(20,40+dr4,dr4)
    
    scalerads = np.concatenate((rbins1,rbins2,rbins3,rbins4))
    
    zbins = np.arange(0,3+dz,dz)
    
    scaleheights1 = np.zeros(len(scalerads)-1)
    scaleheights2 = np.zeros(len(scalerads)-1)
    norms1 = np.zeros(len(scalerads)-1)
    norms2 = np.zeros(len(scalerads)-1)
    err_array = np.zeros(len(scalerads)-1)
    
    for ii in range(len(scalerads)-1):
    
        cut = (dataframe.R > scalerads[ii]) & (dataframe.R < scalerads[ii+1])
        err_array[ii] = (scalerads[ii+1]-scalerads[ii])/2.
    
        zvals = dataframe.Z[cut]
        
        coeffs = exponential_fit_coeffs(zvals)
        
        scaleheights1[ii] = coeffs[0]
        scaleheights2[ii] = coeffs[2]
        norms1[ii] = coeffs[1]
        norms2[ii] = coeffs[3]
    
    for ii in range(len(scaleheights1)):
        if str(scaleheights1[ii]) == 'nan':
            scaleheights1[ii] = 0
        else:
            scaleheights1[ii] = 1./abs(scaleheights1[ii])
        if str(scaleheights2[ii]) == 'nan':
            scaleheights2[ii] = 0
        else:
            scaleheights2[ii] = 1./abs(scaleheights2[ii])

    ## plot scale height distribution
    dr = 0.25
    dz = 0.1
    radbins = np.arange(0,40+dr,dr)
    zbins = np.arange(0,5+dz,dz)
    
    fig = plt.figure(figsize=(12,6))
    H, xed, yed = np.histogram2d(dataframe.R, abs(dataframe.Z), bins=(radbins,zbins))
    extent = [xed[0],xed[-1],yed[0],yed[-1]]
    
    ax = plt.subplot(111)
    im = plt.imshow(np.log10(H.T), extent=extent, origin='lower',
               aspect='auto',interpolation='nearest',
               cmap=histcolor)
    
    plt.scatter(scalerads[6:-1] + err_array[6:], scaleheights1[6:], c='r')
    plt.errorbar(scalerads[6:-1] + err_array[6:], scaleheights1[6:], xerr=err_array[6:], linewidth=0, ecolor='r', elinewidth=1)
    
    plt.scatter(scalerads[6:-1] + err_array[6:], scaleheights2[6:], c='#00FF40')
    plt.errorbar(scalerads[6:-1] + err_array[6:], scaleheights2[6:], xerr=err_array[6:], linewidth=0, ecolor='#00FF40', elinewidth=1)
    
    plt.fill_between([0,3],[-1,-1],[3,3],color='k',alpha=0.75)
    
    plt.minorticks_on()
    
    plt.xlabel('Radius (kpc)')
    plt.ylabel('Z (kpc)')
    plt.xlim(0,40)
    plt.ylim(-0.05,3.)
    
    cax = fig.add_axes([0.91,0.125,0.03,0.775])
    cbar = fig.colorbar(im, cax=cax)
    cbar.ax.set_ylabel('log$_{10}$(N)')
    ax.minorticks_on()
    
    if savename != None:
        plt.savefig(savename)
    
    plt.show()

# plot_scale_height_distribution(orich_df, cut=select2)

# plot_scale_height_distribution(orich_df, cut=select1, histcolor=plt.cm.Greens)

# plot_scale_height_distribution(orich_df, cut=select3, histcolor=plt.cm.Reds)



