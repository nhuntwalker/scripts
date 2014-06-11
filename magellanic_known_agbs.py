import numpy as np
import os
import writeup_figures as w


## The purpose of this script is to select known agb stars in the
## magellanic clouds, for the purpose of producing absolute color-mag
## relations.

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

def select_lmc_agbs(sample, composition):
	lmc_ra = 80.8917
	lmc_dec = -69.7561
	n_deg = 5.

	smc_ra = 13.187
	smc_dec = -72.829
	catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,stype = sample

	col12 = w1-w2
	col23 = w2-w3
	col34 = w3-w4

	# rad = ((ra - lmc_ra)/3.5)**2 + ((decl - lmc_dec)/1.5)**2
	rad = ((ra - smc_ra)/3.5)**2 + ((decl - smc_dec)/1.5)**2

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


simdata = read_agb("SIMBAD_selected.dat")
machodata = read_agb("MACHO_selected.dat")
ogledata = read_agb("OGLE3_selected.dat")

# w.galactic_plot(simdata, ogledata, machodata)
sim_lmc = select_lmc_agbs(simdata, composition='None')
macho_lmc = select_lmc_agbs(machodata, composition='None')
ogle_lmc = select_lmc_agbs(ogledata, composition='None')

sim_lmc_orich = select_lmc_agbs(simdata, composition='O-rich')
macho_lmc_orich = select_lmc_agbs(machodata, composition='O-rich')
ogle_lmc_orich = select_lmc_agbs(ogledata, composition='O-rich')

sim_lmc_crich = select_lmc_agbs(simdata, composition='C-rich')
macho_lmc_crich = select_lmc_agbs(machodata, composition='C-rich')
ogle_lmc_crich = select_lmc_agbs(ogledata, composition='C-rich')

## w.lmc_color_mag_plot(simdata, machodata, ogledata, sim_lmc, macho_lmc, ogle_lmc)

# w.lmc_color_mag_plot_both(simdata, machodata, ogledata, sim_lmc_crich, macho_lmc_crich, ogle_lmc_crich, sim_lmc_orich, macho_lmc_orich, ogle_lmc_orich)

