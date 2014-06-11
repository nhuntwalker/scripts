"""
The purpose of this code is to create a color-magnitude relationship for AGB stars in the LMC.
The relationship shall be linear in 3 colors.

Procedure:
- Load in data from SIMBAD, MACHO, OGLE
- Isolate LMC stars in each
- Calculate E(B-V) for selected stars of each chemical species
- Derive A_\lambda from E(B-V) for each star
- Plot RMS for each band against each color for each species
- Plot color-mag diagrams for each species in de-reddened
	W1 vs color space.

Last Modified: 6/5/2014
"""

import numpy as np
import matplotlib.pyplot as plt
import writeup_figures as w
import os
import rms_extinction_calc as ext
# import sklearn.svm import SVR

os.chdir('/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/scripts')

def read_agb(infile):
	outdir = "/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/selected_known_agbs/"
	data = open(outdir+infile).readlines()
	n = len(data)

	catid = np.zeros(n, int)
	ra = np.zeros(n)
	decl = np.zeros(n)
	gall = np.zeros(n)
	galb = np.zeros(n)
	w1 = np.zeros(n)
	w2 = np.zeros(n)
	w3 = np.zeros(n)
	w4 = np.zeros(n)
	w1err = np.zeros(n)
	w2err = np.zeros(n)
	w3err = np.zeros(n)
	w4err = np.zeros(n)
	w1snr = np.zeros(n)
	w2snr = np.zeros(n)
	w3snr = np.zeros(n)
	w4snr = np.zeros(n)
	j = np.zeros(n)
	h = np.zeros(n)
	k = np.zeros(n)
	jerr = np.zeros(n)
	herr = np.zeros(n)
	kerr = np.zeros(n)
	mrad = np.zeros(n)
	stype = np.zeros(n, dtype="S8")

	for i in range(n):
		line = data[i].split()

		catid[i] = eval(line[0])
		ra[i] = eval(line[1])
		decl[i] = eval(line[2])
		gall[i] = eval(line[3])
		galb[i] = eval(line[4])
		w1[i] = eval(line[5])
		w2[i] = eval(line[6])
		w3[i] = eval(line[7])
		w4[i] = eval(line[8])
		w1err[i] = eval(line[9])
		w2err[i] = eval(line[10])
		w3err[i] = eval(line[11])
		w4err[i] = eval(line[12])
		w1snr[i] = eval(line[13])
		w2snr[i] = eval(line[14])
		w3snr[i] = eval(line[15])
		w4snr[i] = eval(line[16])
		j[i] = eval(line[17])
		h[i] = eval(line[18])
		k[i] = eval(line[19])
		jerr[i] = eval(line[20])
		herr[i] = eval(line[21])
		kerr[i] = eval(line[22])
		mrad[i] = eval(line[23])
		stype[i] = line[24]

	return catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,stype

def select_lmc_agbs(sample, composition, nostype=False):
	lmc_ra = 80.8917
	lmc_dec = -69.7561
	n_deg = 5.

	smc_ra = 13.187
	smc_dec = -72.829

	if nostype == True:
		catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad = sample
	else:
		catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,stype = sample

	col12 = w1-w2
	col23 = w2-w3
	col34 = w3-w4

	rad = ((ra - lmc_ra)/3.5)**2 + ((decl - lmc_dec)/1.5)**2

	if composition=='O-rich':
	## This will be the C-rich cut from Nikutta et al 2014
		fullcut = np.where((col12 < 1.3) & (col12 > 0) & (col23 > 0.4) & (col23 < 2.2) & (col34 > 0) &
				(col34 < 1.3) & (col34 > 0.722*col23 - 0.289) & (w1snr > 10) & (rad < 5))[0]# &
				 # (jerr > -9999)  & (herr > -9999) & (kerr > -9999) & (w1err > -9999) & (w2err > -9999) & (w3err > -9999) & (w4err > -9999))[0]

	if composition=='C-rich':
		fullcut = np.where((col12 > 0.629*col23 - 0.198) & (col12 < 0.629*col23 + 0.359) &
				(col34 > 0.722*col23 - 0.911) & (col34 < 0.722*col23 - 0.289) & (w1snr > 10) & (rad < 5))[0]# &
				 # (jerr > -9999)  & (herr > -9999) & (kerr > -9999) & (w1err > -9999) & (w2err > -9999) & (w3err > -9999) & (w4err > -9999))[0]

	if composition=='None':
		fullcut = np.where(rad < 5)[0]
	return fullcut

##############################################
## Read in data from SIMBAD, MACHO, and OGLE
##############################################
simdata = read_agb("SIMBAD_selected.dat")
machodata = read_agb("MACHO_selected.dat")
ogledata = read_agb("OGLE3_selected.dat")

##############################################
## Select LMC sample
##############################################
# # w.galactic_plot(simdata, ogledata, machodata)
sim_lmc = select_lmc_agbs(simdata, composition='None')
macho_lmc = select_lmc_agbs(machodata, composition='None')
ogle_lmc = select_lmc_agbs(ogledata, composition='None')

##############################################
## Divide into O-rich and C-rich populations
##############################################
sim_lmc_orich = select_lmc_agbs(simdata, composition='O-rich')
macho_lmc_orich = select_lmc_agbs(machodata, composition='O-rich')
ogle_lmc_orich = select_lmc_agbs(ogledata, composition='O-rich')

sim_lmc_crich = select_lmc_agbs(simdata, composition='C-rich')
macho_lmc_crich = select_lmc_agbs(machodata, composition='C-rich')
ogle_lmc_crich = select_lmc_agbs(ogledata, composition='C-rich')

##############################################
## Set LMC distance modulus
##############################################
DM_lmc = 18.32
DMsig = 0.09
lmc_rad = 2.15 #kpc

##############################################
## Separate data into variables
##############################################
catid_1,ra_1,decl_1,gall_1,galb_1 = simdata[:5]
w1_1,w2_1,w3_1,w4_1,w1err_1,w2err_1,w3err_1,w4err_1 = simdata[5:13]
w1snr_1,w2snr_1,w3snr_1,w4snr_1 = simdata[13:17]
j_1,h_1,k_1,jerr_1,herr_1,kerr_1,mrad_1,stype_1 = simdata[17:]

catid_2,ra_2,decl_2,gall_2,galb_2 = machodata[:5]
w1_2,w2_2,w3_2,w4_2,w1err_2,w2err_2,w3err_2,w4err_2 = machodata[5:13]
w1snr_2,w2snr_2,w3snr_2,w4snr_2 = machodata[13:17]
j_2,h_2,k_2,jerr_2,herr_2,kerr_2,mrad_2,stype_2 = machodata[17:]

catid_3,ra_3,decl_3,gall_3,galb_3 = ogledata[:5]
w1_3,w2_3,w3_3,w4_3,w1err_3,w2err_3,w3err_3,w4err_3 = ogledata[5:13]
w1snr_3,w2snr_3,w3snr_3,w4snr_3 = ogledata[13:17]
j_3,h_3,k_3,jerr_3,herr_3,kerr_3,mrad_3,stype_3 = ogledata[17:]

# #################################################
# ## Calculate E(B-V) color excess for LMC objects
# ## Note, don't need to separate into O- and C-
# ## rich populations because we know the distance modulus.
# #################################################
coeffs = [0.34,0.21,0.15,0.11,0.09,0.13] #J,H,K,W1,W2,W3,W4
# ebvs1 = ext.return_ebv(ra_1[sim_lmc], decl_1[sim_lmc], np.ones(len(ra_1[sim_lmc]))*DM_lmc)
# ebvs2 = ext.return_ebv(ra_2[macho_lmc], decl_2[macho_lmc], np.ones(len(ra_2[macho_lmc]))*DM_lmc)
# ebvs3 = ext.return_ebv(ra_3[ogle_lmc], decl_3[ogle_lmc], np.ones(len(ra_3[ogle_lmc]))*DM_lmc)

# # ####################################################
# # ## Calculate extinction coefficients for each band
# # ## Note that A_w4 = A_w3 here
# # ## Again, ONLY LMC STARS!
# # ####################################################
# jlmc_1 = j_1[sim_lmc] - coeffs[0]*2.751*ebvs1; jlmc_2 = j_2[macho_lmc] - coeffs[0]*2.751*ebvs2; jlmc_3 = j_3[ogle_lmc] - coeffs[0]*2.751*ebvs3
# hlmc_1 = h_1[sim_lmc] - coeffs[1]*2.751*ebvs1; hlmc_2 = h_2[macho_lmc] - coeffs[1]*2.751*ebvs2; hlmc_3 = h_3[ogle_lmc] - coeffs[1]*2.751*ebvs3
# klmc_1 = k_1[sim_lmc] - coeffs[2]*2.751*ebvs1; klmc_2 = k_2[macho_lmc] - coeffs[2]*2.751*ebvs2; klmc_3 = k_3[ogle_lmc] - coeffs[2]*2.751*ebvs3
# w1lmc_1 = w1_1[sim_lmc] - coeffs[3]*2.751*ebvs1; w1lmc_2 = w1_2[macho_lmc] - coeffs[3]*2.751*ebvs2; w1lmc_3 = w1_3[ogle_lmc] - coeffs[3]*2.751*ebvs3
# w2lmc_1 = w2_1[sim_lmc] - coeffs[4]*2.751*ebvs1; w2lmc_2 = w2_2[macho_lmc] - coeffs[4]*2.751*ebvs2; w2lmc_3 = w2_3[ogle_lmc] - coeffs[4]*2.751*ebvs3
# w3lmc_1 = w3_1[sim_lmc] - coeffs[5]*2.751*ebvs1; w3lmc_2 = w3_2[macho_lmc] - coeffs[5]*2.751*ebvs2; w3lmc_3 = w3_3[ogle_lmc] - coeffs[5]*2.751*ebvs3
# w4lmc_1 = w4_1[sim_lmc] - coeffs[5]*2.751*ebvs1; w4lmc_2 = w4_2[macho_lmc] - coeffs[5]*2.751*ebvs2; w4lmc_3 = w4_3[ogle_lmc] - coeffs[5]*2.751*ebvs3


# ###########################################################
# ### MAKE SURE YOU OUTPUT THE EXTINCTION COEFFICIENTS!!! ###
# ###########################################################
# # Columns: catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,stype

# f = open('../dereddened_known_agbs/known_lmc_agbs.dat','w')
# fmt = '%g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %s\n'
# for i in range(len(jlmc_1)):
# 	f.write(fmt % (catid_1[sim_lmc][i],ra_1[sim_lmc][i],decl_1[sim_lmc][i],gall_1[sim_lmc][i],galb_1[sim_lmc][i],w1_1[sim_lmc][i],w2_1[sim_lmc][i],w3_1[sim_lmc][i],w4_1[sim_lmc][i],w1err_1[sim_lmc][i],w2err_1[sim_lmc][i],w3err_1[sim_lmc][i],w4err_1[sim_lmc][i],w1snr_1[sim_lmc][i],w2snr_1[sim_lmc][i],w3snr_1[sim_lmc][i],w4snr_1[sim_lmc][i],j_1[sim_lmc][i],h_1[sim_lmc][i],k_1[sim_lmc][i],jerr_1[sim_lmc][i],herr_1[sim_lmc][i],kerr_1[sim_lmc][i],mrad_1[sim_lmc][i],ebvs1[i],stype_1[sim_lmc][i]))

# for i in range(len(jlmc_2)):
# 	f.write(fmt % (catid_2[macho_lmc][i],ra_2[macho_lmc][i],decl_2[macho_lmc][i],gall_2[macho_lmc][i],galb_2[macho_lmc][i],w1_2[macho_lmc][i],w2_2[macho_lmc][i],w3_2[macho_lmc][i],w4_2[macho_lmc][i],w1err_2[macho_lmc][i],w2err_2[macho_lmc][i],w3err_2[macho_lmc][i],w4err_2[macho_lmc][i],w1snr_2[macho_lmc][i],w2snr_2[macho_lmc][i],w3snr_2[macho_lmc][i],w4snr_2[macho_lmc][i],j_2[macho_lmc][i],h_2[macho_lmc][i],k_2[macho_lmc][i],jerr_2[macho_lmc][i],herr_2[macho_lmc][i],kerr_2[macho_lmc][i],mrad_2[macho_lmc][i],ebvs2[i],stype_2[macho_lmc][i]))

# for i in range(len(jlmc_3)):
# 	f.write(fmt % (catid_3[ogle_lmc][i],ra_3[ogle_lmc][i],decl_3[ogle_lmc][i],gall_3[ogle_lmc][i],galb_3[ogle_lmc][i],w1_3[ogle_lmc][i],w2_3[ogle_lmc][i],w3_3[ogle_lmc][i],w4_3[ogle_lmc][i],w1err_3[ogle_lmc][i],w2err_3[ogle_lmc][i],w3err_3[ogle_lmc][i],w4err_3[ogle_lmc][i],w1snr_3[ogle_lmc][i],w2snr_3[ogle_lmc][i],w3snr_3[ogle_lmc][i],w4snr_3[ogle_lmc][i],j_3[ogle_lmc][i],h_3[ogle_lmc][i],k_3[ogle_lmc][i],jerr_3[ogle_lmc][i],herr_3[ogle_lmc][i],kerr_3[ogle_lmc][i],mrad_3[ogle_lmc][i],ebvs3[i],stype_3[ogle_lmc][i]))
# f.close()

###########################################################
### THIS ENDS THE FIRST PART OF THE CODE. 				###
### THE COLOR EXCESS HAS BEEN CALCULATED AND SAVED. 	###
### NOW FOR THE DERIVATIONS AND PLOTTING! 				###
###########################################################
cols = np.arange(25)
infile = '../dereddened_known_agbs/known_lmc_agbs.dat'
data = np.loadtxt(infile, usecols=cols, unpack=True)

catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,ebvs = data

###########################################################
## Turning apparent magnitiudes into absolute magnitudes ##
## using the LMC distance modulus of 18.32 				 ##
###########################################################

w1,w2,w3,w4 = w1 - DM_lmc - coeffs[3]*2.751*ebvs, w2 - DM_lmc - coeffs[4]*2.751*ebvs, w3 - DM_lmc - coeffs[5]*2.751*ebvs, w4 - DM_lmc - coeffs[5]*2.751*ebvs
j,h,k = j - DM_lmc - coeffs[0]*2.751*ebvs, h - DM_lmc - coeffs[1]*2.751*ebvs, k - DM_lmc - coeffs[2]*2.751*ebvs

orich = select_lmc_agbs(data[:-1],'O-rich', nostype=True)
crich = select_lmc_agbs(data[:-1],'C-rich', nostype=True)

###########################################################
## Assigning colors
###########################################################
colk3 = k-w3
col12 = w1-w2
col23 = w2-w3

def regress(xvals,yvals,deg=1):
	## For n-degree regression
	ordered = sorted(range(len(xvals)), key=lambda k: xvals[k])
	X = xvals[ordered]
	if deg == 1:
		M = np.column_stack((np.ones((len(X))),X)) # design matrix
	if deg == 2:
		M = np.column_stack((np.ones((len(X))),X,X**2)) # design matrix
	if deg == 3:
		M = np.column_stack((np.ones((len(X))),X,X**2,X**3)) # design matrix

	Y = yvals[ordered]

	A = np.dot(M.transpose(),M)
	B = np.dot(M.transpose(),Y)

	theta = np.dot(np.linalg.pinv(A),B)

	if deg == 1:
		Y_model = theta[0] + theta[1]*X
	if deg == 2:
		Y_model = theta[0] + theta[1]*X + theta[2]*X*X
	if deg == 3:
		Y_model = theta[0] + theta[1]*X + theta[2]*X*X + theta[3]*X*X*X

	return X, Y_model, theta

def regress_svr(attributes, yvals):
	"""
	Attributes need to be 
	"""

def rms_error(xvals, yvals):
	X, Y_model, theta = regress(xvals, yvals)
	errors = yvals - Y_model
	rms = np.sqrt(np.sum(errors**2)/len(xvals))
	return rms

xvals1_c = colk3[crich]
xvals1_o = colk3[orich]

xvals2_c = col12[crich]
xvals2_o = col12[orich]

xvals3_c = col23[crich]
xvals3_o = col23[orich]

yvalsj_c = j[crich]
yvalsh_c = h[crich]
yvalsk_c = k[crich]
yvals1_c = w1[crich]
yvals2_c = w2[crich]
yvals3_c = w3[crich]
yvals4_c = w4[crich]

yvalsj_o = j[orich]
yvalsh_o = h[orich]
yvalsk_o = k[orich]
yvals1_o = w1[orich]
yvals2_o = w2[orich]
yvals3_o = w3[orich]
yvals4_o = w4[orich]


###########################################################
## create an array of rms values to iterate over		 ##
## for plotting 										 ##
###########################################################
rmsarr1_c = [rms_error(xvals1_c, yvalsj_c), rms_error(xvals1_c, yvalsh_c), rms_error(xvals1_c, yvalsk_c), rms_error(xvals1_c, yvals1_c), rms_error(xvals1_c, yvals2_c), rms_error(xvals1_c, yvals3_c), rms_error(xvals1_c, yvals4_c)]
rmsarr1_o = [rms_error(xvals1_o, yvalsj_o), rms_error(xvals1_o, yvalsh_o), rms_error(xvals1_o, yvalsk_o), rms_error(xvals1_o, yvals1_o), rms_error(xvals1_o, yvals2_o), rms_error(xvals1_o, yvals3_o), rms_error(xvals1_o, yvals4_o)]

rmsarr2_c = [rms_error(xvals2_c, yvalsj_c), rms_error(xvals2_c, yvalsh_c), rms_error(xvals2_c, yvalsk_c), rms_error(xvals2_c, yvals1_c), rms_error(xvals2_c, yvals2_c), rms_error(xvals2_c, yvals3_c), rms_error(xvals2_c, yvals4_c)]
rmsarr2_o = [rms_error(xvals2_o, yvalsj_o), rms_error(xvals2_o, yvalsh_o), rms_error(xvals2_o, yvalsk_o), rms_error(xvals2_o, yvals1_o), rms_error(xvals2_o, yvals2_o), rms_error(xvals2_o, yvals3_o), rms_error(xvals2_o, yvals4_o)]

rmsarr3_c = [rms_error(xvals3_c, yvalsj_c), rms_error(xvals3_c, yvalsh_c), rms_error(xvals3_c, yvalsk_c), rms_error(xvals3_c, yvals1_c), rms_error(xvals3_c, yvals2_c), rms_error(xvals3_c, yvals3_c), rms_error(xvals3_c, yvals4_c)]
rmsarr3_o = [rms_error(xvals3_o, yvalsj_o), rms_error(xvals3_o, yvalsh_o), rms_error(xvals3_o, yvalsk_o), rms_error(xvals3_o, yvals1_o), rms_error(xvals3_o, yvals2_o), rms_error(xvals3_o, yvals3_o), rms_error(xvals3_o, yvals4_o)]

fig = plt.figure(figsize=(10,3))
fig.subplots_adjust(left=0.07, right=0.97, bottom=0.15, top=0.95, wspace=0.3)

ax = plt.subplot(131)
ax.plot(np.arange(len(rmsarr1_c)), rmsarr1_c, markersize=5, marker='o', c='r')
ax.plot(np.arange(len(rmsarr1_o)), rmsarr1_o, markersize=10, marker='x', c='b')
ax.text(0.9,0.9,'K-W3',horizontalalignment='right',transform=ax.transAxes)
ax.grid()
ax.set_xticklabels(['','J','H','K','W1','W2','W3','W4'])
ax.set_ylabel('RMS err')
ax.set_xlabel('M$_\lambda$')
ax.set_xlim(-0.5,6.5)
ax.set_ylim(0.25, 2.5)


ax = plt.subplot(132)
ax.plot(np.arange(len(rmsarr2_c)), rmsarr2_c, markersize=5, marker='o', c='r')
ax.plot(np.arange(len(rmsarr2_o)), rmsarr2_o, markersize=10, marker='x', c='b')
ax.text(0.9,0.9,'W1-W2',horizontalalignment='right',transform=ax.transAxes)
ax.grid()
ax.set_xticklabels(['','J','H','K','W1','W2','W3','W4'])
ax.set_ylabel('RMS err')
ax.set_xlabel('M$_\lambda$')
ax.set_xlim(-0.5,6.5)
ax.set_ylim(0.25, 2.5)


ax = plt.subplot(133)
ax.plot(np.arange(len(rmsarr3_c)), rmsarr3_c, markersize=5, marker='o', c='r')
ax.plot(np.arange(len(rmsarr3_o)), rmsarr3_o, markersize=10, marker='x', c='b')
ax.text(0.9,0.9,'W2-W3',horizontalalignment='right',transform=ax.transAxes)
ax.grid()
ax.set_xticklabels(['','J','H','K','W1','W2','W3','W4'])
ax.set_ylabel('RMS err')
ax.set_xlabel('M$_\lambda$')
ax.set_xlim(-0.5,6.5)
ax.set_ylim(0.25, 2.5)

figout = '/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/writeup/plots/rms_color_mag.pdf'
plt.savefig(figout)
# plt.show()


w.lmc_colormag_resids(xvals1_c, yvals1_c, 'k', 'r', 'K - W3', 'lmcagbs_relations_kw3_crich.pdf')
w.lmc_colormag_resids(xvals1_o, yvals1_o, 'g', 'b', 'K - W3', 'lmcagbs_relations_kw3_orich.pdf')

w.lmc_colormag_resids(xvals2_c, yvals1_c, 'k', 'r', 'W1 - W2', 'lmcagbs_relations_w12_crich.pdf')
w.lmc_colormag_resids(xvals2_o, yvals1_o, 'g', 'b', 'W1 - W2', 'lmcagbs_relations_w12_orich.pdf')

w.lmc_colormag_resids(xvals3_c, yvals1_c, 'k', 'r', 'W2 - W3', 'lmcagbs_relations_w23_crich.pdf')
w.lmc_colormag_resids(xvals3_o, yvals1_o, 'g', 'b', 'W2 - W3', 'lmcagbs_relations_w23_orich.pdf')





