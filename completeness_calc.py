import numpy as np
import matplotlib.pyplot as plt
import MySQLdb
import colorbounds as co
import writeup_figures as w
import os

db = MySQLdb.connect(host='localhost', user='root', passwd='root')
cursor = db.cursor()

os.chdir('/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/scripts')
outdir = "/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/selected_known_agbs/"

# Compute a sample's completeness and nothing else.
# Leave room for plots

def completeness(sample, samplename, return_objects=False, extra_cuts = 'None'):
	## Calculate the completeness for a given sample
	## after applying color cuts
	##
	## Columns are...
	## catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,stype
	catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,stype = sample

	coljk = j-k
	colk3 = k-w3
	col12 = w1-w2
	col23 = w2-w3
	col34 = w3-w4

	fullcut = np.where( (coljk > 1.1) & (col23 > 0.3) & (col34 < -0.83*(col23) + 3.37 )) #& (col34 < 1.5))

	if extra_cuts.lower() == 'nikutta o-rich':
		fullcut = np.where((col12 < 1.3) & (col12 > 0) & (col23 > 0.4) & (col23 < 2.2) & (col34 > 0) &
			(col34 < 1.3) & (col34 > 0.722*col23 - 0.289))

	if extra_cuts.lower() == 'nikutta c-rich':
		fullcut = np.where((col12 > 0.629*col23 - 0.198) & (col12 < 0.629*col23 + 0.359) &
			(col34 > 0.722*col23 - 0.911) & (col34 < 0.722*col23 - 0.289))

	if extra_cuts.lower() == 'tuwang zone 1':
		fullcut = np.where( (coljk > 0.8*colk3 + 0.42) & (coljk < 1.66*colk3 + 0.72) & 
			(colk3 > 0.35) & (colk3 < 1.45))

	if extra_cuts.lower() == 'tuwang zone 2':
		fullcut = np.where( (coljk > 0.6*colk3 + 0.71) & (coljk < 0.6*colk3 + 2.25) &
			(colk3 > 1.45))

	if extra_cuts.lower() == 'tuwang zone 3':
		fullcut = np.where( (coljk > 0.2*colk3 + 1.29) & (coljk < 0.6*colk3 + 0.71) & 
			(colk3 > 1.45))


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

	coljk = coljk[fullcut]
	colk3 = colk3[fullcut]
	col12 = col12[fullcut]
	col23 = col23[fullcut]
	col34 = col34[fullcut]


	if return_objects == True:
		print "%s:\n\tOriginal: \t\t%i\n\tAfter Cut: \t\t%i" % (samplename,len(sample[0]), len(fullcut[0]))
		print "\t|b| < 10 deg (%%): \t%.2f" % (len(np.where(abs(galb) < 10.)[0])/float(len(galb)) * 100.)
		print "\tCompleteness (%%): \t%.2f\n" % (float(len(fullcut[0]))/len(sample[0]) * 100.)
		for star in set(sample[-1]):
			print "\t\t%s: %i \t%i \t%.3f%%" % (star, len(sample[-1][np.where(sample[-1] == star)]), len(stype[np.where(stype == star)]), len(np.where(stype == star)[0])/float(len(np.where(sample[-1] == star)[0])) * 100.)
		print "________________________________________________________________________"

		return catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,coljk, colk3, col12, col23, col34, stype

	elif return_objects == 'test':
		outfile = open(outdir+samplename+"_c_rich_testset.dat",'w')
		fmt = "%i %g %g %g %g %g %s 1\n"
		for q in range(len(catid)):
			outfile.write(fmt % (catid[q],coljk[q],colk3[q],col12[q],col23[q],col34[q],stype[q]))
		outfile.close()

	else:
		print "%s:\n\tOriginal: \t\t%i\n\tAfter Cut: \t\t%i" % (samplename,len(sample[0]), len(fullcut[0]))
		print "\t|b| < 10 deg (%%): \t%.2f" % (len(np.where(abs(galb) < 10.)[0])/float(len(galb)) * 100.)
		print "\tCompleteness (%%): \t%.2f\n" % (float(len(fullcut[0]))/len(sample[0]) * 100.)
		for star in set(sample[-1]):
			print "\t\t%s: %i \t%i \t%.3f%%" % (star, len(sample[-1][np.where(sample[-1] == star)]), len(stype[np.where(stype == star)]), len(np.where(stype == star)[0])/float(len(np.where(sample[-1] == star)[0])) * 100.)
		print "________________________________________________________________________"

		outfile = open(outdir+samplename+"_selected.dat",'w')
		fmt = "%i %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %s\n"
		for q in range(len(catid)):
			outfile.write(fmt % (catid[q],ra[q],decl[q],gall[q],galb[q],w1[q],w2[q],w3[q],w4[q],w1err[q],w2err[q],w3err[q],w4err[q],w1snr[q],w2snr[q],w3snr[q],w4snr[q],j[q],h[q],k[q],jerr[q],herr[q],kerr[q],mrad[q],stype[q]))
		outfile.close()

		return len(fullcut[0])

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


## Get SIMBAD objects
simdata = read_agb("simbad_output.dat")
simcomplete = completeness(simdata, 'SIMBAD', return_objects=True)

machodata = read_agb("macho_output.dat")
machocomplete = completeness(machodata, 'MACHO', return_objects=True)

ogledata = read_agb("ogle_output.dat")
oglecomplete = completeness(ogledata, 'OGLE3', return_objects=True)

# total_completeness = (simcomplete + machocomplete + oglecomplete)/float(len(simdata[0]) + len(machodata[0]) + len(ogledata[0])) * 100.
# print 'Total Completeness: %.2f%%' % total_completeness

# ## Plots
# w.plot_bounded_samples(simdata, ogledata, machodata, title_str="AGBs")
# w.plot_nikutta_bounds(simdata, ogledata, machodata)

## Outputting all candidates
outfile = open(outdir+"known_agbs_selected.dat",'w')
fmt = "%i %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %s\n"
for ii in range(len(simcomplete[0])):
	outfile.write(fmt % (simcomplete[0][ii],simcomplete[1][ii],simcomplete[2][ii],simcomplete[3][ii],simcomplete[4][ii],simcomplete[5][ii],simcomplete[6][ii],
		simcomplete[7][ii],simcomplete[8][ii],simcomplete[9][ii],simcomplete[10][ii],simcomplete[11][ii],simcomplete[12][ii],simcomplete[13][ii],
		simcomplete[14][ii],simcomplete[15][ii],simcomplete[16][ii],simcomplete[17][ii],simcomplete[18][ii],simcomplete[19][ii],simcomplete[20][ii],
		simcomplete[21][ii],simcomplete[22][ii],simcomplete[23][ii],simcomplete[24][ii],simcomplete[25][ii],simcomplete[26][ii],simcomplete[27][ii],
		simcomplete[28][ii],simcomplete[29][ii]))

for ii in range(len(machocomplete[0])):
	outfile.write(fmt % (machocomplete[0][ii],machocomplete[1][ii],machocomplete[2][ii],machocomplete[3][ii],machocomplete[4][ii],machocomplete[5][ii],machocomplete[6][ii],
		simcomplete[7][ii],simcomplete[8][ii],simcomplete[9][ii],simcomplete[10][ii],simcomplete[11][ii],simcomplete[12][ii],simcomplete[13][ii],
		simcomplete[14][ii],simcomplete[15][ii],simcomplete[16][ii],simcomplete[17][ii],simcomplete[18][ii],simcomplete[19][ii],simcomplete[20][ii],
		simcomplete[21][ii],simcomplete[22][ii],simcomplete[23][ii],simcomplete[24][ii],simcomplete[25][ii],simcomplete[26][ii],simcomplete[27][ii],
		simcomplete[28][ii],simcomplete[29][ii]))

for ii in range(len(oglecomplete[0])):
	outfile.write(fmt % (oglecomplete[0][ii],oglecomplete[1][ii],oglecomplete[2][ii],oglecomplete[3][ii],oglecomplete[4][ii],oglecomplete[5][ii],oglecomplete[6][ii],
		simcomplete[7][ii],simcomplete[8][ii],simcomplete[9][ii],simcomplete[10][ii],simcomplete[11][ii],simcomplete[12][ii],simcomplete[13][ii],
		simcomplete[14][ii],simcomplete[15][ii],simcomplete[16][ii],simcomplete[17][ii],simcomplete[18][ii],simcomplete[19][ii],simcomplete[20][ii],
		simcomplete[21][ii],simcomplete[22][ii],simcomplete[23][ii],simcomplete[24][ii],simcomplete[25][ii],simcomplete[26][ii],simcomplete[27][ii],
		simcomplete[28][ii],simcomplete[29][ii]))

outfile.close()

