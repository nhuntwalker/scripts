import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import retrieve_samples as get

matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['text.usetex'] = True

def histogram_of_radii():
	simdata = get.sample_simbad()
	ogledata = get.sample_ogle3()
	machodata = get.sample_macho()
	qsodata = get.sample_qso()
	agndata = get.sample_agn()
	lrgdata = get.sample_lrgs()
	stardata = get.sample_dr9sspp()

	H1,edges = np.histogram(simdata[23],bins=np.linspace(0,3,20))
	H2,edges = np.histogram(ogledata[23],bins=np.linspace(0,3,20))
	H3,edges = np.histogram(machodata[23],bins=np.linspace(0,3,20))
	H4,edges = np.histogram(qsodata[23],bins=np.linspace(0,3,20))
	H5,edges = np.histogram(agndata[23],bins=np.linspace(0,3,20))
	H6,edges = np.histogram(lrgdata[23],bins=np.linspace(0,3,20))
	H7,edges = np.histogram(stardata[23],bins=np.linspace(0,3,20))

	dedges = edges[1]/2.

	plt.figure(figsize=(6,5))
	plt.plot(edges[:-1]+dedges,H1/float(sum(H1)),marker='o')
	plt.plot(edges[:-1]+dedges,H2/float(sum(H2)),marker='o')
	plt.plot(edges[:-1]+dedges,H3/float(sum(H3)),marker='o')
	plt.plot(edges[:-1]+dedges,H4/float(sum(H4)),marker='o')
	plt.plot(edges[:-1]+dedges,H5/float(sum(H5)),marker='o')
	plt.plot(edges[:-1]+dedges,H6/float(sum(H6)),marker='o')
	plt.plot(edges[:-1]+dedges,H7/float(sum(H7)),marker='o')

	plt.xlabel("Arc Seconds")
	plt.ylabel("N/N$_{tot}$")
	plt.xlim(0,2.5)
	plt.show()

def plot_bounded_samples(sample1, sample2=None, sample3=None, sample4=None, sample5=None, title_str=None):
	## Plot 1 is J-K vs W2-W3
	## [17]-[19] vs [6] - [7]

	tint = 0.2
	tintcol = 'k'
	thick = 1.5

	plt.figure(figsize=(4,6))
	plt.subplots_adjust(top=0.985, bottom=0.08, left=0.13, right=0.97, hspace=0)
	ax = plt.subplot(211)
	colw23_1 = sample1[6] - sample1[7]
	colw34_1 = sample1[7] - sample1[8]
	coljk_1 = sample1[17] - sample1[19]

	ax.scatter(colw23_1, coljk_1, s=1, edgecolor='None', color='k')
	ax.text(0.95, 0.9, title_str, transform = ax.transAxes, horizontalalignment='right')

	if sample2 != None:
		colw23_2 = sample2[6] - sample2[7]
		colw34_2 = sample2[7] - sample2[8]
		coljk_2 = sample2[17] - sample2[19]
		ax.scatter(colw23_2, coljk_2, s=1, edgecolor='None', color='r')

	if sample3 != None:
		colw23_3 = sample3[6] - sample3[7]
		colw34_3 = sample3[7] - sample3[8]
		coljk_3 = sample3[17] - sample3[19]
		ax.scatter(colw23_3, coljk_3, s=1, edgecolor='None', color='b')

	if sample4 != None:
		colw23_4 = sample4[6] - sample4[7]
		colw34_4 = sample4[7] - sample4[8]
		coljk_4 = sample4[17] - sample4[19]
		ax.scatter(colw23_4, coljk_4, s=1, edgecolor='None', color='g')

	if sample5 != None:
		colw23_5 = sample5[6] - sample5[7]
		colw34_5 = sample5[7] - sample5[8]
		coljk_5 = sample5[17] - sample5[19]
		ax.scatter(colw23_5, coljk_5, s=1, edgecolor='None', color='orange')

	#boundary limits
	ax.fill_between([-1.,5.],[-1.,-1.],[1.1,1.1],color=tintcol,alpha=tint,linestyle='--')
	ax.plot([-1,0.3], [1.1,1.1], color='gray', linestyle='--')
	ax.plot([0.3,4], [1.1,1.1], color='k', lw=thick)

	ax.fill_betweenx([1.1,4],[-1.,-1.],[0.3,0.3],color=tintcol,alpha=tint,linestyle='--')
	ax.plot([0.3,0.3], [-1,1.1], color='gray', linestyle='--')
	ax.plot([0.3,0.3], [1.1,4], color='k', lw=thick)
	ax.set_xlim(-0.4,3.9)
	ax.set_ylim(-0.4,3.9)
	ax.set_xlabel("W2-W3")
	ax.set_ylabel("J-K")
	ax.minorticks_on()


	ax = plt.subplot(212)
	ax.scatter(colw23_1, colw34_1, s=1, edgecolor='None', color='k')

	if sample2 != None:
		ax.scatter(colw23_2, colw34_2, s=1, edgecolor='None', color='r')
	if sample3 != None:
		ax.scatter(colw23_3, colw34_3, s=1, edgecolor='None', color='b')
	if sample4 != None:
		ax.scatter(colw23_4, colw34_4, s=1, edgecolor='None', color='g')
	if sample5 != None:
		ax.scatter(colw23_5, colw34_5, s=1, edgecolor='None', color='orange')

	#boundary limits
	# ax.fill_between([-1,4],[1.5,1.5],[4.,4.],color=tintcol,alpha=tint,linestyle='--')
	# ax.plot([-1,4], [1.5,1.5], color='gray', linestyle='--')
	# ax.plot([0.3,2.3], [1.5,1.5], color='k', lw=thick)

	ax.fill_betweenx([-1,4],[-1,-1],[0.3,0.3],color=tintcol,alpha=tint,linestyle='--')
	ax.plot([0.3,0.3], [3.121,4], color='gray', linestyle='--')
	ax.plot([0.3,0.3], [-0.5,3.121], color='k', lw=thick)

	ax.fill_between([0.3,4.],[-0.83*0.3 + 3.37,-0.83*4 + 3.37],[4,4],color=tintcol,alpha=tint,linestyle='--')
	ax.plot([-1,4], [-0.83*(-1.0) + 3.37,-0.83*4 + 3.37], color='gray', linestyle='--')
	ax.plot([0.3,4], [-0.83*0.3 + 3.37,-0.83*4 + 3.37], color='k', lw=thick)

	ax.set_xlim(-0.4,3.9)
	ax.set_ylim(-0.4,3.9)
	ax.set_xlabel("W2-W3")
	ax.set_ylabel("W3-W4")

	ax.minorticks_on()
	plt.show()

def plot_nikutta_bounds(sample1, sample2=None, sample3=None, sample4=None, sample5=None):
	## Plot 1 is W1-W2 vs W2-W3

	tint = 0.2
	tintcol = 'k'
	thick = 1.75

	plt.figure(figsize=(4,6))
	plt.subplots_adjust(top=0.985, bottom=0.08, left=0.13, right=0.97, hspace=0)
	ax = plt.subplot(211)
	colw12_1 = sample1[5] - sample1[6]
	colw23_1 = sample1[6] - sample1[7]
	colw34_1 = sample1[7] - sample1[8]
	coljk_1 = sample1[17] - sample1[19]

	ax.scatter(colw23_1, colw12_1, s=1, edgecolor='None', color='k')
	ax.text(0.05, 0.9, 'c', transform = ax.transAxes, horizontalalignment='right', fontweight='bold', fontsize='14')

	if sample2 != None:
		colw12_2 = sample2[5] - sample2[6]
		colw23_2 = sample2[6] - sample2[7]
		colw34_2 = sample2[7] - sample2[8]
		coljk_2 = sample2[17] - sample2[19]
		ax.scatter(colw23_2, colw12_2, s=1, edgecolor='None', color='r')

	if sample3 != None:
		colw12_3 = sample3[5] - sample3[6]
		colw23_3 = sample3[6] - sample3[7]
		colw34_3 = sample3[7] - sample3[8]
		coljk_3 = sample3[17] - sample3[19]
		ax.scatter(colw23_3, colw12_3, s=1, edgecolor='None', color='b')

	if sample4 != None:
		colw12_4 = sample4[5] - sample4[6]
		colw23_4 = sample4[6] - sample4[7]
		colw34_4 = sample4[7] - sample4[8]
		coljk_4 = sample4[17] - sample4[19]
		ax.scatter(colw23_4, colw12_4, s=1, edgecolor='None', color='g')

	if sample5 != None:
		colw12_5 = sample5[5] - sample5[6]
		colw23_5 = sample5[6] - sample5[7]
		colw34_5 = sample5[7] - sample5[8]
		coljk_5 = sample5[17] - sample5[19]
		ax.scatter(colw23_5, colw12_5, s=1, edgecolor='None', color='orange')

	#boundary limits
	# O-rich
	ax.plot([-1,4], [0.2,0.2], color='gray', linestyle='--')
	ax.plot([-1,4], [2,2], color='gray', linestyle='--')
	ax.plot([0.4,0.4], [-1,4], color='gray', linestyle='--')
	ax.plot([2.2,2.2], [-1,4], color='gray', linestyle='--')

	ax.fill_between([0.4,2.2],[0.2,0.2],[2,2], color='b', alpha=tint)
	ax.plot([0.4,2.2], [0.2,0.2], color='b', lw=thick)
	ax.plot([0.4,2.2], [2,2], color='b', lw=thick)
	ax.plot([0.4,0.4], [0.2,2], color='b', lw=thick)
	ax.plot([2.2,2.2], [0.2,2], color='b', lw=thick)

	# Beginning Cuts
	ax.plot([0,4], [0.2,0.2], color='k', lw=thick)
	ax.plot([0,0], [0.2,4], color='k', lw=thick)
	ax.plot([4,4], [0.2,4], color='k', lw=thick)

	# C-rich
	ax.fill_between([0,4], [0.629*(0) - 0.198,0.629*4 - 0.198], [0.629*(0) + 0.359,0.629*4 + 0.359], color='r', alpha=tint)
	ax.plot([0,4], [0.629*(0) - 0.198,0.629*4 - 0.198], color='r', lw=thick)
	ax.plot([0,4], [0.629*(0) + 0.359,0.629*4 + 0.359], color='r', lw=thick)

	ax.set_xlim(-0.4,3.9)
	ax.set_ylim(-0.4,3.9)
	ax.set_xlabel("W2-W3")
	ax.set_ylabel("W1-W2")
	ax.minorticks_on()


	ax = plt.subplot(212)
	ax.scatter(colw23_1, colw34_1, s=1, edgecolor='None', color='k')
	ax.text(0.05, 0.9, 'd', transform = ax.transAxes, horizontalalignment='right', fontweight='bold', fontsize='14')

	if sample2 != None:
		ax.scatter(colw23_2, colw34_2, s=1, edgecolor='None', color='r')
	if sample3 != None:
		ax.scatter(colw23_3, colw34_3, s=1, edgecolor='None', color='b')
	if sample4 != None:
		ax.scatter(colw23_4, colw34_4, s=1, edgecolor='None', color='g')
	if sample5 != None:
		ax.scatter(colw23_5, colw34_5, s=1, edgecolor='None', color='orange')

	# O-rich
	ax.plot([0.4,0.4], [-1,4], color='gray', linestyle='--')
	ax.plot([2.2,2.2], [-1,4], color='gray', linestyle='--')
	ax.plot([-1,4], [1.3,1.3], color='gray', linestyle='--')
	ax.plot([-1,4], [0,0], color='gray', linestyle='--')
	ax.plot([-1,4], [0.722*(-1)-0.289, 0.722*4-0.289], color='gray', linestyle='--')

	ax.fill_between([0.4,2.2],[0.722*0.4-0.289, 0.722*2.2-0.289],[1.3,1.3], color='b', alpha=tint)
	ax.plot([0.4,2.2], [1.3,1.3], color='b', lw=thick)
	ax.plot([0.4,0.4], [0,1.3], color='b', lw=thick)
	ax.plot([0.4,2.2], [0.722*0.4-0.289, 0.722*2.2-0.289], color='b', lw=thick)

	# Beginning Cuts
	ax.plot([0,0], [-1,4], color='k', lw=thick)
	ax.plot([4,4], [-1,4], color='k', lw=thick)

	# C-rich
	ax.fill_between([0,4], [0.722*(0) - 0.911,0.722*4 - 0.911], [0.722*(0) - 0.289,0.722*4 - 0.289], color='r', alpha=tint)
	ax.plot([0,4], [0.722*(0) - 0.289,0.722*4 - 0.289], color='r', lw=thick)
	ax.plot([0,4], [0.722*(0) - 0.911,0.722*4 - 0.911], color='r', lw=thick)

	ax.set_xlim(-0.4,3.9)
	ax.set_ylim(-0.4,3.9)
	ax.set_xlabel("W2-W3")
	ax.set_ylabel("W3-W4")

	ax.minorticks_on()
	plt.show()

def plot_tuwang_bounds(sample1, sample2=None, sample3=None, contam1=None, contam2=None, contam3=None, contam4=None, contam5=None):
	## Plot 1 is J-K vs K-W3

	tint = 0.2
	tintcol = 'k'
	thick = 1.75

	plt.figure(figsize=(4,6))
	plt.subplots_adjust(top=0.985, bottom=0.08, left=0.13, right=0.97, hspace=0)
	ax = plt.subplot(211)

	coljk_1 = sample1[17] - sample1[19]
	colk3_1 = sample1[19] - sample1[7]
	ax.scatter(colk3_1, coljk_1, s=1, edgecolor='None', color='k')
	ax.text(0.05, 0.9, 'a', transform = ax.transAxes, horizontalalignment='right', fontweight='bold', fontsize='14')

	if sample2 != None:
		coljk_2 = sample2[17] - sample2[19]
		colk3_2 = sample2[19] - sample2[7]
		ax.scatter(colk3_2, coljk_2, s=1, edgecolor='None', color='r')

	if sample3 != None:
		coljk_3 = sample3[17] - sample3[19]
		colk3_3 = sample3[19] - sample3[7]
		ax.scatter(colk3_3, coljk_3, s=1, edgecolor='None', color='b')

	#boundary limits
	# Zone 1
	ax.fill_between([0.35,1.45],[0.42 + 0.8*0.35, 0.42 + 0.8*1.45],[0.72 + 1.66*0.35, 0.72 + 1.66*1.45], color='k', alpha=tint)
	ax.plot([0.35,1.45], [0.42 + 0.8*0.35, 0.42 + 0.8*1.45], color='k', lw=2)
	ax.plot([0.35,1.45], [0.72 + 1.66*0.35, 0.72 + 1.66*1.45], color='k', lw=2)
	ax.plot([0.35,0.35], [0.42 + 0.8*0.35, 0.72 + 1.66*0.35], color='k', lw=2)
	ax.plot([1.45,1.45], [0.42 + 0.8*1.45, 0.72 + 1.66*1.45], color='k', lw=2)

	# Zone 2
	ax.fill_between([1.45,7.25],[0.71 + 0.6*1.45, 0.71 + 0.6*7.25],[2.25 + 0.6*1.45, 2.25 + 0.6*7.25], color='b', alpha=tint)
	ax.plot([1.45,7.25], [0.71 + 0.6*1.45, 0.71 + 0.6*7.25], color='b', lw=2)
	ax.plot([1.45,7.25], [2.25 + 0.6*1.45, 2.25 + 0.6*7.25], color='b', lw=2)
	ax.plot([1.45,1.45], [0.71 + 0.6*1.45, 2.25 + 0.6*1.45], color='b', lw=2)
	ax.plot([7.25,7.25], [0.71 + 0.6*7.25, 2.25 + 0.6*7.25], color='b', lw=2)

	# Zone 3
	ax.fill_between([1.45,7.25],[1.29 + 0.2*1.45, 1.29 + 0.2*7.25],[0.71 + 0.6*1.45, 0.71 + 0.6*7.25], color='r', alpha=tint)
	ax.plot([1.45, 7.25], [1.29 + 0.2*1.45, 1.29 + 0.2*7.25], color='r', lw=2)
	ax.plot([1.45, 7.25], [0.71 + 0.6*1.45, 0.71 + 0.6*7.25], color='r', lw=2)
	ax.plot([1.45, 1.45], [1.29 + 0.2*1.45, 0.71 + 0.6*1.45], color='r', lw=2)
	ax.plot([7.25, 7.25], [1.29 + 0.2*7.25, 0.71 + 0.6*7.25], color='r', lw=2)

	ax.set_xlim(-0.9,7.9)
	ax.set_ylim(-0.9,6.9)
	ax.set_xlabel("K$_s$-W3")
	ax.set_ylabel("J-K")
	ax.minorticks_on()


	ax = plt.subplot(212)
	ax.text(0.05, 0.9, 'b', transform = ax.transAxes, horizontalalignment='right', fontweight='bold', fontsize='14')

	if contam1 != None:
		coljk_1 = contam1[17] - contam1[19]
		colk3_1 = contam1[19] - contam1[7]
		ax.scatter(colk3_1, coljk_1, s=1, edgecolor='None', color='k')

	if contam2 != None:
		coljk_2 = contam2[17] - contam2[19]
		colk3_2 = contam2[19] - contam2[7]
		ax.scatter(colk3_2, coljk_2, s=1, edgecolor='None', color='r')

	if contam3 != None:
		coljk_3 = contam3[17] - contam3[19]
		colk3_3 = contam3[19] - contam3[7]
		ax.scatter(colk3_3, coljk_3, s=1, edgecolor='None', color='b')

	if contam4 != None:
		coljk_4 = contam4[17] - contam4[19]
		colk3_4 = contam4[19] - contam4[7]
		ax.scatter(colk3_4, coljk_4, s=1, edgecolor='None', color='g')

	if contam5 != None:
		coljk_5 = contam5[17] - contam5[19]
		colk3_5 = contam5[19] - contam5[7]
		ax.scatter(colk3_5, coljk_5, s=1, edgecolor='None', color='orange')

	#boundary limits
	# Zone 1
	ax.fill_between([0.35,1.45],[0.42 + 0.8*0.35, 0.42 + 0.8*1.45],[0.72 + 1.66*0.35, 0.72 + 1.66*1.45], color='k', alpha=tint)
	ax.plot([0.35,1.45], [0.42 + 0.8*0.35, 0.42 + 0.8*1.45], color='k', lw=2)
	ax.plot([0.35,1.45], [0.72 + 1.66*0.35, 0.72 + 1.66*1.45], color='k', lw=2)
	ax.plot([0.35,0.35], [0.42 + 0.8*0.35, 0.72 + 1.66*0.35], color='k', lw=2)
	ax.plot([1.45,1.45], [0.42 + 0.8*1.45, 0.72 + 1.66*1.45], color='k', lw=2)

	# Zone 2
	ax.fill_between([1.45,7.25],[0.71 + 0.6*1.45, 0.71 + 0.6*7.25],[2.25 + 0.6*1.45, 2.25 + 0.6*7.25], color='b', alpha=tint)
	ax.plot([1.45,7.25], [0.71 + 0.6*1.45, 0.71 + 0.6*7.25], color='b', lw=2)
	ax.plot([1.45,7.25], [2.25 + 0.6*1.45, 2.25 + 0.6*7.25], color='b', lw=2)
	ax.plot([1.45,1.45], [0.71 + 0.6*1.45, 2.25 + 0.6*1.45], color='b', lw=2)
	ax.plot([7.25,7.25], [0.71 + 0.6*7.25, 2.25 + 0.6*7.25], color='b', lw=2)

	# Zone 3
	ax.fill_between([1.45,7.25],[1.29 + 0.2*1.45, 1.29 + 0.2*7.25],[0.71 + 0.6*1.45, 0.71 + 0.6*7.25], color='r', alpha=tint)
	ax.plot([1.45, 7.25], [1.29 + 0.2*1.45, 1.29 + 0.2*7.25], color='r', lw=2)
	ax.plot([1.45, 7.25], [0.71 + 0.6*1.45, 0.71 + 0.6*7.25], color='r', lw=2)
	ax.plot([1.45, 1.45], [1.29 + 0.2*1.45, 0.71 + 0.6*1.45], color='r', lw=2)
	ax.plot([7.25, 7.25], [1.29 + 0.2*7.25, 0.71 + 0.6*7.25], color='r', lw=2)

	ax.set_xlim(-0.9,7.9)
	ax.set_ylim(-0.9,6.9)
	ax.set_xlabel("K$_s$-W3")
	ax.set_ylabel("J-K")
	ax.minorticks_on()

	plt.show()

def galactic_plot(sample1, sample2=None, sample3=None):
	## Indices 3 and 4 are gall and galb respectively

	ax = plt.subplot(111)

	sample1[3][np.where(sample1[3] > 180)] = sample1[3][np.where(sample1[3] > 180)] - 360.
	ax.scatter(sample1[3],sample1[4],s=1,edgecolor='None',c='k')

	if sample2 != None:
		sample2[3][np.where(sample2[3] > 180)] = sample2[3][np.where(sample2[3] > 180)] - 360.
		ax.scatter(sample2[3],sample2[4],s=1,edgecolor='None',c='b')

	if sample3 != None:
		sample3[3][np.where(sample3[3] > 180)] = sample3[3][np.where(sample3[3] > 180)] - 360.
		ax.scatter(sample3[3],sample3[4],s=1,edgecolor='None',c='r')

	ax.set_xlim(-180,180)
	ax.set_ylim(-90,90)
	ax.minorticks_on()

	plt.show()

def lmc_color_mag_plot(sample1, sample2, sample3, indices1, indices2, indices3):
	cut1 = indices1
	cut2 = indices2
	cut3 = indices3

	DM_lmc = 18.32

	catid_1,ra_1,decl_1,gall_1,galb_1,w1_1,w2_1,w3_1,w4_1,w1err_1,w2err_1,w3err_1,w4err_1,w1snr_1,w2snr_1,w3snr_1,w4snr_1,j_1,h_1,k_1,jerr_1,herr_1,kerr_1,mrad_1,stype_1 = sample1
	catid_2,ra_2,decl_2,gall_2,galb_2,w1_2,w2_2,w3_2,w4_2,w1err_2,w2err_2,w3err_2,w4err_2,w1snr_2,w2snr_2,w3snr_2,w4snr_2,j_2,h_2,k_2,jerr_2,herr_2,kerr_2,mrad_2,stype_2 = sample2
	catid_3,ra_3,decl_3,gall_3,galb_3,w1_3,w2_3,w3_3,w4_3,w1err_3,w2err_3,w3err_3,w4err_3,w1snr_3,w2snr_3,w3snr_3,w4snr_3,j_3,h_3,k_3,jerr_3,herr_3,kerr_3,mrad_3,stype_3 = sample3

	col12_1 = w1_1 - w2_1
	col12_2 = w1_2 - w2_2
	col12_3 = w1_3 - w2_3

	w1_1,w2_1,w3_1,w4_1,j_1,h_1,k_1 = w1_1 - DM_lmc,w2_1 - DM_lmc,w3_1 - DM_lmc,w4_1 - DM_lmc,j_1 - DM_lmc,h_1 - DM_lmc,k_1 - DM_lmc
	w1_2,w2_2,w3_2,w4_2,j_2,h_2,k_2 = w1_2 - DM_lmc,w2_2 - DM_lmc,w3_2 - DM_lmc,w4_2 - DM_lmc,j_2 - DM_lmc,h_2 - DM_lmc,k_2 - DM_lmc
	w1_3,w2_3,w3_3,w4_3,j_3,h_3,k_3 = w1_3 - DM_lmc,w2_3 - DM_lmc,w3_3 - DM_lmc,w4_3 - DM_lmc,j_3 - DM_lmc,h_3 - DM_lmc,k_3 - DM_lmc

	pntsz = 1
	xmin = -0.19
	xmax = 1.79

	fig = plt.figure(figsize=(12,5))
	fig.subplots_adjust(top=0.975, right=0.975, left=0.07, wspace=0.35, hspace=0)

	deg = 2
	data_color = 'green'
	fit_color = 'blue'

	def regress(xvals,yvals,dy,deg=2):
		ordered = sorted(range(len(xvals)), key=lambda k: xvals[k])
		X = xvals[ordered]
		if deg == 1:
			M = np.column_stack((np.ones((len(X))),X)) # design matrix
		if deg == 2:
			M = np.column_stack((np.ones((len(X))),X,X**2)) # design matrix
		if deg == 3:
			M = np.column_stack((np.ones((len(X))),X,X**2,X**3)) # design matrix

		Y = yvals[ordered]
		dy = dy[ordered]
		C = np.identity(len(xvals))*(dy*dy)

		A = np.dot(np.dot(M.transpose(),np.linalg.pinv(C)),M)
		B = np.dot(np.dot(M.transpose(),np.linalg.pinv(C)),Y)
		theta = np.dot(np.linalg.pinv(A),B)

		if deg == 1:
			Y_model = theta[0] + theta[1]*X
		if deg == 2:
			Y_model = theta[0] + theta[1]*X + theta[2]*X*X
		if deg == 3:
			Y_model = theta[0] + theta[1]*X + theta[2]*X*X + theta[3]*X*X*X

		return X, Y_model, theta



	xvals = np.concatenate((col12_1[cut1],col12_2[cut2],col12_3[cut3]))

	ax = plt.subplot(241)
	yvals = np.concatenate((j_1[cut1],j_2[cut2],j_3[cut3]))
	dy = np.concatenate((jerr_1[cut1], jerr_2[cut2], jerr_3[cut3]))

	ax.scatter(xvals, yvals, edgecolor='None',c=data_color,s=pntsz)

	## Linear Regression to find the Fit!
	X, Y_model, coeffs = regress(xvals,yvals,dy,deg)

	ax.plot(X, Y_model, color=fit_color)
	ax.text(0.97,0.9,'y = %.2f + %.2f*x + %.2fx$^2$' % (coeffs[0],coeffs[1],coeffs[2]),horizontalalignment='right',fontsize=8,transform=ax.transAxes)

	ax.set_ylabel('M$_{J}$')
	ax.set_ylim(16.9-DM_lmc,9.1-DM_lmc)
	ax.set_xlim(xmin,xmax)

	ax = plt.subplot(242)
	yvals = np.concatenate((h_1[cut1],h_2[cut2],h_3[cut3]))
	dy = np.concatenate((herr_1[cut1], herr_2[cut2], herr_3[cut3]))

	ax.scatter(xvals, yvals, edgecolor='None',c=data_color,s=pntsz)

	## Linear Regression to find the Fit!
	X, Y_model, coeffs = regress(xvals,yvals,dy,deg)

	ax.plot(X, Y_model, color=fit_color)
	ax.text(0.97,0.9,'y = %.2f + %.2f*x + %.2fx$^2$' % (coeffs[0],coeffs[1],coeffs[2]),horizontalalignment='right',fontsize=8,transform=ax.transAxes)

	ax.set_ylabel('M$_{H}$')
	ax.set_ylim(14.9-DM_lmc,8.1-DM_lmc)
	ax.set_xlim(xmin,xmax)

	ax = plt.subplot(243)
	yvals = np.concatenate((k_1[cut1],k_2[cut2],k_3[cut3]))
	dy = np.concatenate((kerr_1[cut1], kerr_2[cut2], kerr_3[cut3]))
	ax.scatter(xvals, yvals, edgecolor='None',c=data_color,s=pntsz)

	## Linear Regression to find the Fit!
	X, Y_model, coeffs = regress(xvals,yvals,dy,deg)

	ax.plot(X, Y_model, color=fit_color)
	ax.text(0.97,0.9,'y = %.2f + %.2f*x + %.2fx$^2$' % (coeffs[0],coeffs[1],coeffs[2]),horizontalalignment='right',fontsize=8,transform=ax.transAxes)

	ax.set_ylabel('M$_{K}$')
	ax.set_ylim(12.9-DM_lmc,7.1-DM_lmc)
	ax.set_xlim(xmin,xmax)

	ax = plt.subplot(244)
	yvals = np.concatenate((w1_1[cut1],w1_2[cut2],w1_3[cut3]))
	dy = np.concatenate((w1err_1[cut1], w1err_2[cut2], w1err_3[cut3]))
	ax.scatter(xvals, yvals, edgecolor='None',c=data_color,s=pntsz)

	## Linear Regression to find the Fit!
	X, Y_model, coeffs = regress(xvals,yvals,dy,deg)

	ax.plot(X, Y_model, color=fit_color)
	ax.text(0.97,0.9,'y = %.2f + %.2f*x + %.2fx$^2$' % (coeffs[0],coeffs[1],coeffs[2]),horizontalalignment='right',fontsize=8,transform=ax.transAxes)

	ax.set_ylabel('M$_{W1}$')
	ax.set_xlabel('W1-W2')
	ax.set_ylim(10.9-DM_lmc,7.6-DM_lmc)
	ax.set_xlim(xmin,xmax)

	ax = plt.subplot(245)
	yvals = np.concatenate((w2_1[cut1],w2_2[cut2],w2_3[cut3]))
	dy = np.concatenate((w2err_1[cut1], w2err_2[cut2], w2err_3[cut3]))
	ax.scatter(xvals, yvals, edgecolor='None',c=data_color,s=pntsz)

	## Linear Regression to find the Fit!
	X, Y_model, coeffs = regress(xvals,yvals,dy,deg)

	ax.plot(X, Y_model, color=fit_color)
	ax.text(0.97,0.9,'y = %.2f + %.2f*x + %.2fx$^2$' % (coeffs[0],coeffs[1],coeffs[2]),horizontalalignment='right',fontsize=8,transform=ax.transAxes)

	ax.set_ylabel('M$_{W2}$')
	ax.set_xlabel('W1-W2')
	ax.set_ylim(10.4-DM_lmc,6.6-DM_lmc)
	ax.set_xlim(xmin,xmax)


	ax = plt.subplot(246)
	yvals = np.concatenate((w3_1[cut1],w3_2[cut2],w3_3[cut3]))
	dy = np.concatenate((w3err_1[cut1], w3err_2[cut2], w3err_3[cut3]))
	ax.scatter(xvals, yvals, edgecolor='None',c=data_color,s=pntsz)

	## Linear Regression to find the Fit!
	X, Y_model, coeffs = regress(xvals,yvals,dy,deg)

	ax.plot(X, Y_model, color=fit_color)
	ax.text(0.97,0.9,'y = %.2f + %.2f*x + %.2fx$^2$' % (coeffs[0],coeffs[1],coeffs[2]),horizontalalignment='right',fontsize=8,transform=ax.transAxes)

	ax.set_ylabel('M$_{W3}$')
	ax.set_xlabel('W1-W2')
	ax.set_ylim(9.4-DM_lmc,5.1-DM_lmc)
	ax.set_xlim(xmin,xmax)


	ax = plt.subplot(247)
	yvals = np.concatenate((w4_1[cut1],w4_2[cut2],w4_3[cut3]))
	dy = np.concatenate((w4err_1[cut1], w4err_2[cut2], w4err_3[cut3]))
	ax.scatter(xvals, yvals, edgecolor='None',c=data_color,s=pntsz)

	## Linear Regression to find the Fit!
	X, Y_model, coeffs = regress(xvals,yvals,dy,deg)

	ax.plot(X, Y_model, color=fit_color)
	ax.text(0.97,0.9,'y = %.2f + %.2f*x + %.2fx$^2$' % (coeffs[0],coeffs[1],coeffs[2]),horizontalalignment='right',fontsize=8,transform=ax.transAxes)

	ax.set_ylabel('M$_{W4}$')
	ax.set_xlabel('W1-W2')
	ax.set_ylim(8.4-DM_lmc,4.1-DM_lmc)
	ax.set_xlim(xmin,xmax)



	plt.show()

def lmc_color_mag_plot_both(sample1, sample2, sample3, carbindices1, carbindices2, carbindices3, oxyindices1, oxyindices2, oxyindices3):
	## Very similar to lmc_color_mag_plot, except that it plots for 
	## both populations of O-rich and C-rich candidates

	c_cut1 = carbindices1
	c_cut2 = carbindices2
	c_cut3 = carbindices3

	o_cut1 = oxyindices1
	o_cut2 = oxyindices2
	o_cut3 = oxyindices3

	DM_lmc = 18.32
	DMsig = 0.09
	lmc_rad = 2.15 #kpc

	catid_1,ra_1,decl_1,gall_1,galb_1,w1_1,w2_1,w3_1,w4_1,w1err_1,w2err_1,w3err_1,w4err_1,w1snr_1,w2snr_1,w3snr_1,w4snr_1,j_1,h_1,k_1,jerr_1,herr_1,kerr_1,mrad_1,stype_1 = sample1
	catid_2,ra_2,decl_2,gall_2,galb_2,w1_2,w2_2,w3_2,w4_2,w1err_2,w2err_2,w3err_2,w4err_2,w1snr_2,w2snr_2,w3snr_2,w4snr_2,j_2,h_2,k_2,jerr_2,herr_2,kerr_2,mrad_2,stype_2 = sample2
	catid_3,ra_3,decl_3,gall_3,galb_3,w1_3,w2_3,w3_3,w4_3,w1err_3,w2err_3,w3err_3,w4err_3,w1snr_3,w2snr_3,w3snr_3,w4snr_3,j_3,h_3,k_3,jerr_3,herr_3,kerr_3,mrad_3,stype_3 = sample3

	colk3_1 = k_1 - w3_1
	colk3_2 = k_2 - w3_2
	colk3_3 = k_3 - w3_3

	col12_1 = w1_1 - w2_1
	col12_2 = w1_2 - w2_2
	col12_3 = w1_3 - w2_3

	col23_1 = w2_1 - w3_1
	col23_2 = w2_2 - w3_2
	col23_3 = w2_3 - w3_3

	w1_1,w2_1,w3_1,w4_1,j_1,h_1,k_1 = w1_1 - DM_lmc,w2_1 - DM_lmc,w3_1 - DM_lmc,w4_1 - DM_lmc,j_1 - DM_lmc,h_1 - DM_lmc,k_1 - DM_lmc
	w1_2,w2_2,w3_2,w4_2,j_2,h_2,k_2 = w1_2 - DM_lmc,w2_2 - DM_lmc,w3_2 - DM_lmc,w4_2 - DM_lmc,j_2 - DM_lmc,h_2 - DM_lmc,k_2 - DM_lmc
	w1_3,w2_3,w3_3,w4_3,j_3,h_3,k_3 = w1_3 - DM_lmc,w2_3 - DM_lmc,w3_3 - DM_lmc,w4_3 - DM_lmc,j_3 - DM_lmc,h_3 - DM_lmc,k_3 - DM_lmc

	pntsz = 1
	xmin = min(colk3_1)
	xmax = max(colk3_1)
	# xmin = -0.19
	# xmax = 1.79

	fig = plt.figure(figsize=(5,4))
	fig.subplots_adjust(top=0.975, right=0.975, left=0.14, bottom=0.12, wspace=0, hspace=0)

	deg = 2
	orich_data_color = 'green'
	orich_fit_color = 'blue'

	crich_data_color = 'black'
	crich_fit_color = 'red'

	ylab1 = 'M$_{W1}$'
	ylab2 = '$\Delta$M$_{W1}$'


	def regress(xvals,yvals,dy,deg=2):
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
		dy = dy[ordered]
		C = np.identity(len(xvals))*(dy*dy)

		# A = np.dot(np.dot(M.transpose(),np.linalg.pinv(C)),M)
		# B = np.dot(np.dot(M.transpose(),np.linalg.pinv(C)),Y)

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

	def rms_error(xvals, yvals, model_params):
		theta = model_params
		Y_model = theta[0] + theta[1]*xvals + theta[2]*xvals*xvals
		errors = yvals - Y_model
		rms = np.sqrt(np.sum(errors**2)/len(xvals))
		return rms


	xvals_c = np.concatenate((colk3_1[c_cut1],colk3_2[c_cut2],colk3_3[c_cut3]))
	xvals_o = np.concatenate((colk3_1[o_cut1],colk3_2[o_cut2],colk3_3[o_cut3]))


	ax = plt.subplot(222)
	yvals = np.concatenate((w1_1[o_cut1],w1_2[o_cut2],w1_3[o_cut3]))
	dy = np.concatenate((w1err_1[o_cut1], w1err_2[o_cut2], w1err_3[o_cut3]))

	ax.scatter(xvals_o, yvals, edgecolor='None',c=orich_data_color,s=pntsz)

	## Linear Regression to find the Fit!
	X, Y_model, coeffs = regress(xvals_o, yvals, dy, deg)

	ax.fill_between(X, Y_model - DMsig, Y_model + DMsig, color=orich_fit_color, alpha=0.5)
	ax.plot(X, Y_model, color=orich_fit_color)
	ax.text(0.97,0.9,'y = %.2f + %.2f*x + %.2fx$^2$' % (coeffs[0],coeffs[1],coeffs[2]),horizontalalignment='right',fontsize=8,transform=ax.transAxes)

	ax.set_ylabel(ylab1)
	ax.set_ylim(-7.4,-10.7)
	ax.set_xlim(xmin,xmax)
	ax.minorticks_on()


	ax = plt.subplot(221)
	yvals = np.concatenate((w1_1[c_cut1],w1_2[c_cut2],w1_3[c_cut3]))
	dy = np.concatenate((w1err_1[c_cut1], w1err_2[c_cut2], w1err_3[c_cut3]))

	ax.scatter(xvals_c, yvals, edgecolor='None',c=crich_data_color,s=pntsz)

	## Linear Regression to find the Fit!
	X, Y_model, coeffs = regress(xvals_c,yvals,dy,deg)

	ax.fill_between(X, Y_model - DMsig, Y_model + DMsig, color=crich_fit_color, alpha=0.5)
	ax.plot(X, Y_model, color=crich_fit_color)
	ax.text(0.97,0.9,'y = %.2f + %.2f*x + %.2fx$^2$' % (coeffs[0],coeffs[1],coeffs[2]),horizontalalignment='right',fontsize=8,transform=ax.transAxes)

	ax.set_ylabel(ylab1)
	ax.set_ylim(-7.4,-10.7)
	ax.set_xlim(xmin,xmax)
	ax.minorticks_on()


	ax = plt.subplot(224)
	yvals = np.concatenate((w1_1[o_cut1],w1_2[o_cut2],w1_3[o_cut3]))
	dy = np.concatenate((w1err_1[o_cut1], w1err_2[o_cut2], w1err_3[o_cut3]))

	## Linear Regression to find the Fit!
	X, Y_model, coeffs = regress(xvals_o,yvals,dy,deg)
	err = rms_error(X, yvals, coeffs)
	ax.text(0.9,0.9,'$\sigma$: %.2f' % err, horizontalalignment='right',transform=ax.transAxes)

	ax.scatter(xvals_o, yvals - Y_model, edgecolor='None',c=orich_data_color,s=pntsz)
	ax.plot([xmin,xmax],[0,0],linestyle='-',color=orich_fit_color)
	ax.plot([xmin,xmax],[err,err],linestyle='--',color=orich_fit_color)
	ax.plot([xmin,xmax],[-err,-err],linestyle='--',color=orich_fit_color)

	ax.set_ylabel(ylab2)
	ax.set_xlabel('W1-W2')
	ax.set_ylim(-3.9,3.9)
	ax.set_xlim(xmin,xmax)
	ax.minorticks_on()


	ax = plt.subplot(223)
	yvals = np.concatenate((w1_1[c_cut1],w1_2[c_cut2],w1_3[c_cut3]))
	dy = np.concatenate((w1err_1[c_cut1], w1err_2[c_cut2], w1err_3[c_cut3]))

	## Linear Regression to find the Fit!
	X, Y_model, coeffs = regress(xvals_c,yvals,dy,deg)
	err = rms_error(X, yvals, coeffs)
	ax.text(0.9,0.9,'$\sigma$: %.2f' % err, horizontalalignment='right',transform=ax.transAxes)

	ax.scatter(xvals_c, yvals - Y_model, edgecolor='None',c=crich_data_color,s=pntsz)
	ax.plot([xmin,xmax],[0,0],linestyle='-',color=crich_fit_color)
	ax.plot([xmin,xmax],[err,err],linestyle='--',color=crich_fit_color)
	ax.plot([xmin,xmax],[-err,-err],linestyle='--',color=crich_fit_color)

	ax.set_ylabel(ylab2)
	ax.set_xlabel('W1-W2')
	ax.set_ylim(-3.9,3.9)
	ax.set_xlim(xmin,xmax)
	ax.minorticks_on()

	plt.show()



def lmc_colormag_resids(color, mag, pntcol, fitcol, colorlabel, outfile=None):
	pntsz = 1

	xmin = np.round(min(color),decimals=1)
	xmax = np.round(max(color),decimals=1)

	ylab1 = 'M$_{W1}$'
	ylab2 = '$\Delta$M$_{W1}$'

	fig = plt.figure(figsize=(4,4))
	fig.subplots_adjust(hspace=0, left=0.18, right=0.97, top=0.97, bottom=0.125)

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

	def rms_error(xvals, yvals):
		X, Y_model, theta = regress(xvals, yvals)
		errors = yvals - Y_model
		rms = np.sqrt(np.sum(errors**2)/len(xvals))
		return rms

	X, Y_model, coeffs = regress(color, mag)
	rms = rms_error(color, mag)

	ax = plt.subplot(211)
	ax.scatter(color, mag, s=pntsz, color=pntcol, edgecolor='None')
	ax.plot(X, Y_model, color=fitcol, linestyle='-')
	ax.set_xlim(xmin-0.4,xmax+0.5)
	ax.set_ylim(-7.25,-10.5)
	ax.text(0.97,0.9,'y = %.2f + %.2fx' % (coeffs[0],coeffs[1]),horizontalalignment='right',fontsize=8,transform=ax.transAxes)
	ax.minorticks_on()
	ax.set_xlabel(colorlabel)
	ax.set_ylabel('M$_{W1}$')
	for tick in ax.xaxis.get_major_ticks():
	    tick.label.set_fontsize(12) 
	for tick in ax.yaxis.get_major_ticks():
	    tick.label.set_fontsize(12) 
	
	ax = plt.subplot(212)
	ax.scatter(color, mag-Y_model, s=pntsz, color=pntcol, edgecolor='None')
	ax.plot([xmin-5,xmax+5], [0,0], color=fitcol, linestyle='-')
	ax.text(0.97,0.9,'$\sigma$: %.2f' % rms, horizontalalignment='right',transform=ax.transAxes, fontsize=8)
	ax.set_xlim(xmin-0.4,xmax+0.5)
	ax.set_ylim(-1.9,1.9)
	ax.minorticks_on()
	ax.set_xlabel(colorlabel)
	ax.set_ylabel('$\Delta$M$_{W1}$')
	for tick in ax.xaxis.get_major_ticks():
	    tick.label.set_fontsize(12) 
	for tick in ax.yaxis.get_major_ticks():
	    tick.label.set_fontsize(12) 

	if outfile != None:
		plt.savefig('/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/writeup/plots/'+outfile)
	else:
		plt.show()







