import numpy as np
import matplotlib.pyplot as plt
import MySQLdb
import colorbounds as co
import writeup_figures as w
import os

db = MySQLdb.connect(host='localhost', user='root', passwd='root')
cursor = db.cursor()

os.chdir('/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/scripts')

# Compute a sample's contamination and nothing else.
# Leave room for plots

fntlims = [16.83,15.6,11.32,8.0]
brtlims = [2.0,1.5,-3.0,-4.0]

def contamination(sample1, contaminant, contamname, sample2=None, sample3=None, return_objects=False, extra_cuts='None'):
	## Calculate the contamination for a given sample
	## after applying color cuts
	##
	## Columns are...
	## catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,stype
	catid_1,ra_1,decl_1,gall_1,galb_1,w1_1,w2_1,w3_1,w4_1,w1err_1,w2err_1,w3err_1,w4err_1,w1snr_1,w2snr_1,w3snr_1,w4snr_1,j_1,h_1,k_1,jerr_1,herr_1,kerr_1,mrad_1,stype_1 = sample1
	catid = catid_1
	ra = ra_1
	decl = decl_1
	gall = gall_1
	galb = galb_1
	w1 = w1_1
	w2 = w2_1
	w3 = w3_1
	w4 = w4_1
	w1err = w1err_1
	w2err = w2err_1
	w3err = w3err_1
	w4err = w4err_1
	w1snr = w1snr_1
	w2snr = w2snr_1
	w3snr = w3snr_1
	w4snr = w4snr_1
	j = j_1 
	h = h_1 
	k = k_1 
	jerr = jerr_1
	herr = herr_1
	kerr = kerr_1
	mrad = mrad_1
	stype = stype_1

	if sample2 != None:
		catid_2,ra_2,decl_2,gall_2,galb_2,w1_2,w2_2,w3_2,w4_2,w1err_2,w2err_2,w3err_2,w4err_2,w1snr_2,w2snr_2,w3snr_2,w4snr_2,j_2,h_2,k_2,jerr_2,herr_2,kerr_2,mrad_2,stype_2 = sample2
		catid = np.concatenate([catid_1,catid_2])
		ra = np.concatenate([ra_1,ra_2])
		decl = np.concatenate([decl_1,decl_2])
		gall = np.concatenate([gall_1,gall_2])
		galb = np.concatenate([galb_1,galb_2])
		w1 = np.concatenate([w1_1,w1_2])
		w2 = np.concatenate([w2_1,w2_2])
		w3 = np.concatenate([w3_1,w3_2])
		w4 = np.concatenate([w4_1,w4_2])
		w1err = np.concatenate([w1err_1,w1err_2])
		w2err = np.concatenate([w2err_1,w2err_2])
		w3err = np.concatenate([w3err_1,w3err_2])
		w4err = np.concatenate([w4err_1,w4err_2])
		w1snr = np.concatenate([w1snr_1,w1snr_2])
		w2snr = np.concatenate([w2snr_1,w2snr_2])
		w3snr = np.concatenate([w3snr_1,w3snr_2])
		w4snr = np.concatenate([w4snr_1,w4snr_2])
		j = np.concatenate([j_1,j_2])
		h = np.concatenate([h_1,h_2])
		k = np.concatenate([k_1,k_2])
		jerr = np.concatenate([jerr_1,jerr_2])
		herr = np.concatenate([herr_1,herr_2])
		kerr = np.concatenate([kerr_1,kerr_2])
		mrad = np.concatenate([mrad_1,mrad_2])
		stype = np.concatenate([stype_1,stype_2])

	if sample3 != None:
		catid_3,ra_3,decl_3,gall_3,galb_3,w1_3,w2_3,w3_3,w4_3,w1err_3,w2err_3,w3err_3,w4err_3,w1snr_3,w2snr_3,w3snr_3,w4snr_3,j_3,h_3,k_3,jerr_3,herr_3,kerr_3,mrad_3,stype_3 = sample3
		catid = np.concatenate([catid_1,catid_2,catid_3])
		ra = np.concatenate([ra_1,ra_2,ra_3])
		decl = np.concatenate([decl_1,decl_2,decl_3])
		gall = np.concatenate([gall_1,gall_2,gall_3])
		galb = np.concatenate([galb_1,galb_2,galb_3])
		w1 = np.concatenate([w1_1,w1_2,w1_3])
		w2 = np.concatenate([w2_1,w2_2,w2_3])
		w3 = np.concatenate([w3_1,w3_2,w3_3])
		w4 = np.concatenate([w4_1,w4_2,w4_3])
		w1err = np.concatenate([w1err_1,w1err_2,w1err_3])
		w2err = np.concatenate([w2err_1,w2err_2,w2err_3])
		w3err = np.concatenate([w3err_1,w3err_2,w3err_3])
		w4err = np.concatenate([w4err_1,w4err_2,w4err_3])
		w1snr = np.concatenate([w1snr_1,w1snr_2,w1snr_3])
		w2snr = np.concatenate([w2snr_1,w2snr_2,w2snr_3])
		w3snr = np.concatenate([w3snr_1,w3snr_2,w3snr_3])
		w4snr = np.concatenate([w4snr_1,w4snr_2,w4snr_3])
		j = np.concatenate([j_1,j_2,j_3])
		h = np.concatenate([h_1,h_2,h_3])
		k = np.concatenate([k_1,k_2,k_3])
		jerr = np.concatenate([jerr_1,jerr_2,jerr_3])
		herr = np.concatenate([herr_1,herr_2,herr_3])
		kerr = np.concatenate([kerr_1,kerr_2,kerr_3])
		mrad = np.concatenate([mrad_1,mrad_2,mrad_3])
		stype = np.concatenate([stype_1,stype_2,stype_3])

	## Contamination sample
	cont_id,cont_ra,cont_decl,cont_gall,cont_galb,cont_w1,cont_w2,cont_w3,cont_w4,cont_w1err,cont_w2err,cont_w3err,cont_w4err,cont_w1snr,cont_w2snr,cont_w3snr,cont_w4snr,cont_j,cont_h,cont_k,cont_jerr,cont_herr,cont_kerr,cont_mrad = contaminant[:24]

	coljk = j - k
	colk3 = k - w3
	col12 = w1 - w2
	col23 = w2 - w3
	col34 = w3 - w4

	cont_coljk = cont_j - cont_k
	cont_colk3 = cont_k - cont_w3
	cont_col12 = cont_w1 - cont_w2
	cont_col23 = cont_w2 - cont_w3
	cont_col34 = cont_w3 - cont_w4

	fullcut = np.where( (coljk > 1.1) & (col23 > 0.3) & (col34 < -0.83*(col23) + 3.37 ))# & (col34 < 1.5))
	contamcut = np.where( (cont_coljk > 1.6) & (cont_col23 > 0.3) & (cont_col34 < -0.83*(cont_col23) + 3.37 ) )#& (cont_col34 < 1.5))

	if extra_cuts.lower() == 'nikutta o-rich':
		fullcut = np.where( (coljk > 1.1) & (col23 > 0.3) & (col34 < -0.83*(col23) + 3.37 ) & 
			(col12 < 1.3) & (col12 > 0) & (col23 > 0.4) & (col23 < 2.2) & (col34 > 0) &
			(col34 > 1.3) & (col34 > 0.722*col23 - 0.289))

	if extra_cuts.lower() == 'nikutta c-rich':
		fullcut = np.where( (coljk > 1.1) & (col23 > 0.3) & (col34 < -0.83*(col23) + 3.37 ) & 
			(col12 > 0.629*col23 - 0.198) & (col12 < 0.629*col23 + 0.359) &
			(col34 > 0.722*col23 - 0.911) & (col34 < 0.722*col23 - 0.289))

	if extra_cuts.lower() == 'tuwang zone 1':
		fullcut = np.where( (coljk > 0.8*colk3 + 0.42) & (coljk < 1.66*colk3 + 0.72) & 
			(colk3 > 0.35) & (colk3 < 1.45))
		contamcut = np.where( (cont_coljk > 0.8*cont_colk3 + 0.42) & (cont_coljk < 1.66*cont_colk3 + 0.72) & 
			(cont_colk3 > 0.35) & (cont_colk3 < 1.45))

	if extra_cuts.lower() == 'tuwang zone 2':
		fullcut = np.where( (coljk > 0.6*colk3 + 0.71) & (coljk < 0.6*colk3 + 2.25) & 
			(colk3 > 1.45))
		contamcut = np.where( (cont_coljk > 0.6*cont_colk3 + 0.71) & (cont_coljk < 0.6*cont_colk3 + 2.25) & 
			(cont_colk3 > 1.45))

	if extra_cuts.lower() == 'tuwang zone 3':
		fullcut = np.where( (coljk > 0.2*colk3 + 1.29) & (coljk < 0.6*colk3 + 0.71) & 
			(colk3 > 1.45))
		contamcut = np.where( (cont_coljk > 0.2*cont_colk3 + 1.29) & (cont_coljk < 0.6*cont_colk3 + 0.71) & 
			(cont_colk3 > 1.45))

	catid = catid[fullcut]
	ra = ra[fullcut]
	decl = decl[fullcut]
	gall = gall[fullcut]
	galb = galb[fullcut]
	w1 = w1[fullcut]
	w2 = w2[fullcut]
	w3 = w3[fullcut]
	w4 = w4[fullcut]
	w1err = w1err[fullcut]
	w2err = w2err[fullcut]
	w3err = w3err[fullcut]
	w4err = w4err[fullcut]
	w1snr = w1snr[fullcut]
	w2snr = w2snr[fullcut]
	w3snr = w3snr[fullcut]
	w4snr = w4snr[fullcut]
	j = j[fullcut]
	h = h[fullcut]
	k = k[fullcut]
	jerr = jerr[fullcut]
	herr = herr[fullcut]
	kerr = kerr[fullcut]
	mrad = mrad[fullcut]
	stype = stype[fullcut]

	cont_id = cont_id[contamcut]
	cont_ra = cont_ra[contamcut]
	cont_decl = cont_decl[contamcut]
	cont_gall = cont_gall[contamcut]
	cont_galb = cont_galb[contamcut]
	cont_w1 = cont_w1[contamcut] 
	cont_w2 = cont_w2[contamcut] 
	cont_w3 = cont_w3[contamcut] 
	cont_w4 = cont_w4[contamcut] 
	cont_w1err = cont_w1err[contamcut] 
	cont_w2err = cont_w2err[contamcut] 
	cont_w3err = cont_w3err[contamcut] 
	cont_w4err = cont_w4err[contamcut] 
	cont_w1snr = cont_w1snr[contamcut] 
	cont_w2snr = cont_w2snr[contamcut] 
	cont_w3snr = cont_w3snr[contamcut] 
	cont_w4snr = cont_w4snr[contamcut]
	cont_j = cont_j[contamcut]
	cont_h = cont_h[contamcut]
	cont_k = cont_k[contamcut]
	cont_jerr = cont_jerr[contamcut]
	cont_herr = cont_herr[contamcut]
	cont_kerr = cont_kerr[contamcut]
	cont_mrad = cont_mrad[contamcut] 

	if return_objects != False:
		print "%s:\n\tOriginal: \t\t%i\n\tAfter Cut: \t\t%i" % (contamname,len(contaminant[0]), len(contamcut[0]))
		print "\tContamination (%%): \t%.2f\n" % (float(len(contamcut[0]))/(len(contamcut[0]) + len(fullcut[0])) * 100.)

	else:
		print "%s: %i" % (contamname, len(contamcut[0]))


def read_contam(infile, contaminant='None'):
	outdir = "/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/refined_matches/"
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

	if contaminant.lower() == "star":
		colgr = np.zeros(n)
		colri = np.zeros(n)
		vmag = np.zeros(n)
		colbv = np.zeros(n)

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
			colgr[i] = eval(line[24])
			colri[i] = eval(line[25])
			vmag[i] = eval(line[26])
			colbv[i] = eval(line[27])

		return catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,colgr,colri,vmag,colbv

	else:
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

		return catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad


def read_agb(infile):
	outdir = "/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/refined_matches/"
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


simdata = read_agb("simbad_output.dat")
machodata = read_agb("macho_output.dat")
ogledata = read_agb("ogle_output.dat")

agndata = read_contam("agn_output.dat")
qsodata = read_contam("qso_output.dat")
lrgdata = read_contam("lrg_output.dat")
stardata = read_contam("dr9sspp_output.dat")
galdata = read_contam("galaxies_output.dat")

agncontaminated = contamination(sample1 = simdata, sample2 = ogledata, contaminant = agndata, contamname = 'AGN', return_objects = True)
qsocontaminated = contamination(sample1 = simdata, sample2 = ogledata, contaminant = qsodata, contamname = 'QSO', return_objects = True)
lrgcontaminated = contamination(sample1 = simdata, sample2 = ogledata, contaminant = lrgdata, contamname = 'LRG', return_objects = True)
starcontaminated = contamination(sample1 = simdata, sample2 = ogledata, contaminant = stardata, contamname = 'Stars', return_objects = True)
galcontaminated = contamination(sample1 = simdata, sample2 = ogledata, contaminant = galdata, contamname = 'Galaxies', return_objects = True)

w.plot_bounded_samples(stardata, galdata, qsodata, lrgdata, agndata, title_str="Contaminants")
# w.plot_tuwang_bounds(simdata, ogledata, machodata, stardata, galdata, qsodata, lrgdata, agndata)

# agncontaminated = contamination(sample1 = simdata, contaminant = agndata, contamname = 'AGN', return_objects = True)
# qsocontaminated = contamination(sample1 = simdata, contaminant = qsodata, contamname = 'QSO', return_objects = True)

# lrgcontaminated = contamination(sample1 = simdata, contaminant = lrgdata, contamname = 'LRG', return_objects = True)
# starcontaminated = contamination(sample1 = simdata, contaminant = stardata, contamname = 'Stars', return_objects = True)

# galcontaminated = contamination(sample1 = simdata, contaminant = galdata, contamname = 'Galaxies', return_objects = True)













