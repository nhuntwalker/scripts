import MySQLdb
import numpy as np

db = MySQLdb.connect(host='localhost', user='root', passwd='root')
cursor = db.cursor()

fntlims = [16.83,15.6,11.32,8.0]
brtlims = [2.0,1.5,-3.0,-4.0]

outdir = "/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/refined_matches/"

def sample_simbad(output=False):
	""" Time: 326 milliseconds """

	sql = "SELECT w.simbadid, w.ra, w.decl, w.glon, w.glat, "
	sql += "w.w1, w.w2, w.w3, w.w4, "
	sql += "w.w1err, w.w2err, w.w3err, w.w4err, "
	sql += "w.w1snr, w.w2snr, w.w3snr, w.w4snr, "
	sql += "w.jmag, w.hmag, w.kmag, w.jerr, w.herr, w.kerr, "
	sql += "w.match_rad, s.startype "
	sql += "FROM agbtables.simbad_allwise_allmags AS w "
	sql += "INNER JOIN agbtables.simbad_agbs AS s ON w.simbadid = s.simbadid"
	sql += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND (w.ccflag LIKE '0000') AND "
	# sql += " (ABS(w.glat) < 20) AND "
	sql += "(w.w1err > -9999) AND (w.w2err > -9999) AND (w.w3err > -9999)"
	# sql += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND"
	# sql += " (w.jmag > -9999) AND (w.kmag > -9999);"

	cursor.execute(sql)
	data = cursor.fetchall()
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
		catid[i] = data[i][0]
		ra[i] = data[i][1]
		decl[i] = data[i][2]
		gall[i] = data[i][3]
		galb[i] = data[i][4]
		w1[i] = data[i][5]
		w2[i] = data[i][6]
		w3[i] = data[i][7]
		w4[i] = data[i][8]
		w1err[i] = data[i][9]
		w2err[i] = data[i][10]
		w3err[i] = data[i][11]
		w4err[i] = data[i][12]
		w1snr[i] = data[i][13]
		w2snr[i] = data[i][14]
		w3snr[i] = data[i][15]
		w4snr[i] = data[i][16]
		j[i] = data[i][17]
		h[i] = data[i][18]
		k[i] = data[i][19]
		jerr[i] = data[i][20]
		herr[i] = data[i][21]
		kerr[i] = data[i][22]
		mrad[i] = data[i][23]
		stype[i] = data[i][24]

	photocut =  np.where((w1 < fntlims[0]) & (w2 < fntlims[1]) & (w3 < fntlims[2]) & (w4 < fntlims[3]) &
		(w1 > brtlims[0]) & (w2 > brtlims[1]) & (w3 > brtlims[2]) & (w4 > brtlims[3]))

	catid = catid[photocut]
	ra = ra[photocut]
	decl = decl[photocut]
	gall = gall[photocut]
	galb = galb[photocut]
	w1 = w1[photocut]
	w2 = w2[photocut]
	w3 = w3[photocut]
	w4 = w4[photocut]
	w1err = w1err[photocut]
	w2err = w2err[photocut]
	w3err = w3err[photocut]
	w4err = w4err[photocut]
	w1snr = w1snr[photocut]
	w2snr = w2snr[photocut]
	w3snr = w3snr[photocut]
	w4snr = w4snr[photocut]
	j = j[photocut]
	h = h[photocut]
	k = k[photocut]
	jerr = jerr[photocut]
	herr = herr[photocut]
	kerr = kerr[photocut]
	mrad = mrad[photocut]
	stype = stype[photocut]

	if output == True:
		outfile = open(outdir+"simbad_output.dat",'w')
		fmt = "%i %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %s\n"
		for q in range(len(catid)):
			outfile.write(fmt % (catid[q],ra[q],decl[q],gall[q],galb[q],w1[q],w2[q],w3[q],w4[q],w1err[q],w2err[q],w3err[q],w4err[q],w1snr[q],w2snr[q],w3snr[q],w4snr[q],j[q],h[q],k[q],jerr[q],herr[q],kerr[q],mrad[q],stype[q]))
		outfile.close()

	else:
		return catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,stype

def sample_ogle3(output=False):
	""" Time: 300 milliseconds """

	sql = "SELECT w.ogleid, w.ra, w.decl, w.glon, w.glat, "
	sql += "w.w1, w.w2, w.w3, w.w4, "
	sql += "w.w1err, w.w2err, w.w3err, w.w4err, "
	sql += "w.w1snr, w.w2snr, w.w3snr, w.w4snr, "
	sql += "w.jmag, w.hmag, w.kmag, w.jerr, w.herr, w.kerr, "
	sql += "w.match_rad, o.spectr "
	sql += "FROM agbtables.ogle3_allwise_allmags AS w "
	sql += "INNER JOIN agbtables.ogle3_agbs AS o ON w.ogleid = o.ogle3cnt"
	sql += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
	sql += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND"
	sql += " (w.jmag > -9999) AND (w.kmag > -9999);"

	cursor.execute(sql)
	data = cursor.fetchall()
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
		catid[i] = data[i][0]
		ra[i] = data[i][1]
		decl[i] = data[i][2]
		gall[i] = data[i][3]
		galb[i] = data[i][4]
		w1[i] = data[i][5]
		w2[i] = data[i][6]
		w3[i] = data[i][7]
		w4[i] = data[i][8]
		w1err[i] = data[i][9]
		w2err[i] = data[i][10]
		w3err[i] = data[i][11]
		w4err[i] = data[i][12]
		w1snr[i] = data[i][13]
		w2snr[i] = data[i][14]
		w3snr[i] = data[i][15]
		w4snr[i] = data[i][16]
		j[i] = data[i][17]
		h[i] = data[i][18]
		k[i] = data[i][19]
		jerr[i] = data[i][20]
		herr[i] = data[i][21]
		kerr[i] = data[i][22]
		mrad[i] = data[i][23]
		stype[i] = data[i][24]

	photocut =  np.where((w1 < fntlims[0]) & (w2 < fntlims[1]) & (w3 < fntlims[2]) & (w4 < fntlims[3]) &
		(w1 > brtlims[0]) & (w2 > brtlims[1]) & (w3 > brtlims[2]) & (w4 > brtlims[3]))

	catid = catid[photocut]
	ra = ra[photocut]
	decl = decl[photocut]
	gall = gall[photocut]
	galb = galb[photocut]
	w1 = w1[photocut]
	w2 = w2[photocut]
	w3 = w3[photocut]
	w4 = w4[photocut]
	w1err = w1err[photocut]
	w2err = w2err[photocut]
	w3err = w3err[photocut]
	w4err = w4err[photocut]
	w1snr = w1snr[photocut]
	w2snr = w2snr[photocut]
	w3snr = w3snr[photocut]
	w4snr = w4snr[photocut]
	j = j[photocut]
	h = h[photocut]
	k = k[photocut]
	jerr = jerr[photocut]
	herr = herr[photocut]
	kerr = kerr[photocut]
	mrad = mrad[photocut]
	stype = stype[photocut]

	if output == True:
		outfile = open(outdir+"ogle_output.dat",'w')
		fmt = "%i %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %s\n"
		for q in range(len(catid)):
			outfile.write(fmt % (catid[q],ra[q],decl[q],gall[q],galb[q],w1[q],w2[q],w3[q],w4[q],w1err[q],w2err[q],w3err[q],w4err[q],w1snr[q],w2snr[q],w3snr[q],w4snr[q],j[q],h[q],k[q],jerr[q],herr[q],kerr[q],mrad[q],stype[q]))
		outfile.close()

	else:
		return catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,stype

def sample_macho(output=False):
	""" Time: 125 milliseconds """

	sql = "SELECT w.machoid, w.ra, w.decl, w.glon, w.glat, "
	sql += "w.w1, w.w2, w.w3, w.w4, "
	sql += "w.w1err, w.w2err, w.w3err, w.w4err, "
	sql += "w.w1snr, w.w2snr, w.w3snr, w.w4snr, "
	sql += "w.jmag, w.hmag, w.kmag, w.jerr, w.herr, w.kerr, "
	sql += "w.match_rad, m.sequence "
	sql += "FROM agbtables.macho_allwise_allmags AS w "
	sql += "INNER JOIN agbtables.macho_lpvs AS m ON w.machoid = m.machoid"
	sql += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
	sql += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND"
	sql += " (w.jmag > -9999) AND (w.kmag > -9999);"

	cursor.execute(sql)
	data = cursor.fetchall()
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
		catid[i] = data[i][0]
		ra[i] = data[i][1]
		decl[i] = data[i][2]
		gall[i] = data[i][3]
		galb[i] = data[i][4]
		w1[i] = data[i][5]
		w2[i] = data[i][6]
		w3[i] = data[i][7]
		w4[i] = data[i][8]
		w1err[i] = data[i][9]
		w2err[i] = data[i][10]
		w3err[i] = data[i][11]
		w4err[i] = data[i][12]
		w1snr[i] = data[i][13]
		w2snr[i] = data[i][14]
		w3snr[i] = data[i][15]
		w4snr[i] = data[i][16]
		j[i] = data[i][17]
		h[i] = data[i][18]
		k[i] = data[i][19]
		jerr[i] = data[i][20]
		herr[i] = data[i][21]
		kerr[i] = data[i][22]
		mrad[i] = data[i][23]
		stype[i] = data[i][24]

	photocut =  np.where((w1 < fntlims[0]) & (w2 < fntlims[1]) & (w3 < fntlims[2]) & (w4 < fntlims[3]) &
		(w1 > brtlims[0]) & (w2 > brtlims[1]) & (w3 > brtlims[2]) & (w4 > brtlims[3]))

	catid = catid[photocut]
	ra = ra[photocut]
	decl = decl[photocut]
	gall = gall[photocut]
	galb = galb[photocut]
	w1 = w1[photocut]
	w2 = w2[photocut]
	w3 = w3[photocut]
	w4 = w4[photocut]
	w1err = w1err[photocut]
	w2err = w2err[photocut]
	w3err = w3err[photocut]
	w4err = w4err[photocut]
	w1snr = w1snr[photocut]
	w2snr = w2snr[photocut]
	w3snr = w3snr[photocut]
	w4snr = w4snr[photocut]
	j = j[photocut]
	h = h[photocut]
	k = k[photocut]
	jerr = jerr[photocut]
	herr = herr[photocut]
	kerr = kerr[photocut]
	mrad = mrad[photocut]
	stype = stype[photocut]

	if output == True:
		outfile = open(outdir+"macho_output.dat",'w')
		fmt = "%i %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %s\n"
		for q in range(len(catid)):
			outfile.write(fmt % (catid[q],ra[q],decl[q],gall[q],galb[q],w1[q],w2[q],w3[q],w4[q],w1err[q],w2err[q],w3err[q],w4err[q],w1snr[q],w2snr[q],w3snr[q],w4snr[q],j[q],h[q],k[q],jerr[q],herr[q],kerr[q],mrad[q],stype[q]))
		outfile.close()

	else:
		return catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,stype

def sample_lrgs(output=False):
	""" Time: 11.3 milliseconds """

	sql = "SELECT lrgid, ra, decl, glon, glat, "
	sql += "w1, w2, w3, w4, "
	sql += "w1err, w2err, w3err, w4err, "
	sql += "w1snr, w2snr, w3snr, w4snr, "
	sql += "jmag, hmag, kmag, jerr, herr, kerr, "
	sql += "match_rad "
	sql += "FROM sdsstables.lrg_allwise_allmags"
	sql += " WHERE (n2mass = 1) AND (match_rad <= 2.0) AND "
	sql += "(ccflag LIKE '0000') AND (w1err > -9999) AND (w2err > -9999) AND (w3err > -9999)"
	# sql += "(w1snr > 3) AND (w2snr > 3) AND (w3snr > 3) AND "
	# sql += "(jmag > -9999) AND (kmag > -9999);"

	cursor.execute(sql)
	data = cursor.fetchall()
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

	for i in range(n):
		catid[i] = data[i][0]
		ra[i] = data[i][1]
		decl[i] = data[i][2]
		gall[i] = data[i][3]
		galb[i] = data[i][4]
		w1[i] = data[i][5]
		w2[i] = data[i][6]
		w3[i] = data[i][7]
		w4[i] = data[i][8]
		w1err[i] = data[i][9]
		w2err[i] = data[i][10]
		w3err[i] = data[i][11]
		w4err[i] = data[i][12]
		w1snr[i] = data[i][13]
		w2snr[i] = data[i][14]
		w3snr[i] = data[i][15]
		w4snr[i] = data[i][16]
		j[i] = data[i][17]
		h[i] = data[i][18]
		k[i] = data[i][19]
		jerr[i] = data[i][20]
		herr[i] = data[i][21]
		kerr[i] = data[i][22]
		mrad[i] = data[i][23]

	photocut =  np.where((w1 < fntlims[0]) & (w2 < fntlims[1]) & (w3 < fntlims[2]) & (w4 < fntlims[3]) &
		(w1 > brtlims[0]) & (w2 > brtlims[1]) & (w3 > brtlims[2]) & (w4 > brtlims[3]))

	catid = catid[photocut]
	ra = ra[photocut]
	decl = decl[photocut]
	gall = gall[photocut]
	galb = galb[photocut]
	w1 = w1[photocut]
	w2 = w2[photocut]
	w3 = w3[photocut]
	w4 = w4[photocut]
	w1err = w1err[photocut]
	w2err = w2err[photocut]
	w3err = w3err[photocut]
	w4err = w4err[photocut]
	w1snr = w1snr[photocut]
	w2snr = w2snr[photocut]
	w3snr = w3snr[photocut]
	w4snr = w4snr[photocut]
	j = j[photocut]
	h = h[photocut]
	k = k[photocut]
	jerr = jerr[photocut]
	herr = herr[photocut]
	kerr = kerr[photocut]
	mrad = mrad[photocut]

	if output == True:
		outfile = open(outdir+"lrg_output.dat",'w')
		fmt = "%i %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n"
		for q in range(len(catid)):
			outfile.write(fmt % (catid[q],ra[q],decl[q],gall[q],galb[q],w1[q],w2[q],w3[q],w4[q],w1err[q],w2err[q],w3err[q],w4err[q],w1snr[q],w2snr[q],w3snr[q],w4snr[q],j[q],h[q],k[q],jerr[q],herr[q],kerr[q],mrad[q]))
		outfile.close()

	else:
		return catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad


def sample_galaxies(output=False):
	""" Time: 39 seconds """

	sql = "SELECT w.vagcid, w.ra, w.decl, w.glon, w.glat, "
	sql += "w.w1, w.w2, w.w3, w.w4, "
	sql += "w.w1err, w.w2err, w.w3err, w.w4err, "
	sql += "w.w1snr, w.w2snr, w.w3snr, w.w4snr, "
	sql += "w.jmag, w.hmag, w.kmag, w.jerr, w.herr, w.kerr, "
	sql += "w.match_rad "
	sql += "FROM sdsstables.vagc_allwise_allmags AS w INNER JOIN"
	sql += " sdsstables.vagc_objects AS v ON w.vagcid = v.vagcid"
	sql += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
	sql += "(w.ccflag LIKE '0000') AND (w.w1err > -9999) AND (w.w2err > -9999) AND (w.w3err > -9999) AND "
	# sql += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND "
	# sql += "(w.jmag > -9999) AND (w.kmag > -9999) AND "
	sql += "v.CLASS LIKE 'GALAXY' AND v.SUBCLASS NOT LIKE 'AGN%';"

	cursor.execute(sql)
	data = cursor.fetchall()
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

	for i in range(n):
		catid[i] = data[i][0]
		ra[i] = data[i][1]
		decl[i] = data[i][2]
		gall[i] = data[i][3]
		galb[i] = data[i][4]
		w1[i] = data[i][5]
		w2[i] = data[i][6]
		w3[i] = data[i][7]
		w4[i] = data[i][8]
		w1err[i] = data[i][9]
		w2err[i] = data[i][10]
		w3err[i] = data[i][11]
		w4err[i] = data[i][12]
		w1snr[i] = data[i][13]
		w2snr[i] = data[i][14]
		w3snr[i] = data[i][15]
		w4snr[i] = data[i][16]
		j[i] = data[i][17]
		h[i] = data[i][18]
		k[i] = data[i][19]
		jerr[i] = data[i][20]
		herr[i] = data[i][21]
		kerr[i] = data[i][22]
		mrad[i] = data[i][23]

	photocut =  np.where((w1 < fntlims[0]) & (w2 < fntlims[1]) & (w3 < fntlims[2]) & (w4 < fntlims[3]) &
		(w1 > brtlims[0]) & (w2 > brtlims[1]) & (w3 > brtlims[2]) & (w4 > brtlims[3]))

	catid = catid[photocut]
	ra = ra[photocut]
	decl = decl[photocut]
	gall = gall[photocut]
	galb = galb[photocut]
	w1 = w1[photocut]
	w2 = w2[photocut]
	w3 = w3[photocut]
	w4 = w4[photocut]
	w1err = w1err[photocut]
	w2err = w2err[photocut]
	w3err = w3err[photocut]
	w4err = w4err[photocut]
	w1snr = w1snr[photocut]
	w2snr = w2snr[photocut]
	w3snr = w3snr[photocut]
	w4snr = w4snr[photocut]
	j = j[photocut]
	h = h[photocut]
	k = k[photocut]
	jerr = jerr[photocut]
	herr = herr[photocut]
	kerr = kerr[photocut]
	mrad = mrad[photocut]

	if output == True:
		outfile = open(outdir+"galaxies_output.dat",'w')
		fmt = "%i %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n"
		for q in range(len(catid)):
			outfile.write(fmt % (catid[q],ra[q],decl[q],gall[q],galb[q],w1[q],w2[q],w3[q],w4[q],w1err[q],w2err[q],w3err[q],w4err[q],w1snr[q],w2snr[q],w3snr[q],w4snr[q],j[q],h[q],k[q],jerr[q],herr[q],kerr[q],mrad[q]))
		outfile.close()

	else:
		return catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad


def sample_agn(output=False):
	""" Time: 10 seconds """

	sql = "SELECT w.vagcid, w.ra, w.decl, w.glon, w.glat, "
	sql += "w.w1, w.w2, w.w3, w.w4, "
	sql += "w.w1err, w.w2err, w.w3err, w.w4err, "
	sql += "w.w1snr, w.w2snr, w.w3snr, w.w4snr, "
	sql += "w.jmag, w.hmag, w.kmag, w.jerr, w.herr, w.kerr, "
	sql += "w.match_rad "
	sql += "FROM sdsstables.vagc_allwise_allmags AS w INNER JOIN"
	sql += " sdsstables.vagc_objects AS v ON w.vagcid = v.vagcid"
	sql += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
	sql += "(w.ccflag LIKE '0000') AND (w.w1err > -9999) AND (w.w2err > -9999) AND (w.w3err > -9999) AND "
	# sql += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND "
	# sql += "(w.jmag > -9999) AND (w.kmag > -9999) AND "
	sql += "v.SUBCLASS LIKE 'AGN%';"

	cursor.execute(sql)
	data = cursor.fetchall()
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

	for i in range(n):
		catid[i] = data[i][0]
		ra[i] = data[i][1]
		decl[i] = data[i][2]
		gall[i] = data[i][3]
		galb[i] = data[i][4]
		w1[i] = data[i][5]
		w2[i] = data[i][6]
		w3[i] = data[i][7]
		w4[i] = data[i][8]
		w1err[i] = data[i][9]
		w2err[i] = data[i][10]
		w3err[i] = data[i][11]
		w4err[i] = data[i][12]
		w1snr[i] = data[i][13]
		w2snr[i] = data[i][14]
		w3snr[i] = data[i][15]
		w4snr[i] = data[i][16]
		j[i] = data[i][17]
		h[i] = data[i][18]
		k[i] = data[i][19]
		jerr[i] = data[i][20]
		herr[i] = data[i][21]
		kerr[i] = data[i][22]
		mrad[i] = data[i][23]

	photocut =  np.where((w1 < fntlims[0]) & (w2 < fntlims[1]) & (w3 < fntlims[2]) & (w4 < fntlims[3]) &
		(w1 > brtlims[0]) & (w2 > brtlims[1]) & (w3 > brtlims[2]) & (w4 > brtlims[3]))

	catid = catid[photocut]
	ra = ra[photocut]
	decl = decl[photocut]
	gall = gall[photocut]
	galb = galb[photocut]
	w1 = w1[photocut]
	w2 = w2[photocut]
	w3 = w3[photocut]
	w4 = w4[photocut]
	w1err = w1err[photocut]
	w2err = w2err[photocut]
	w3err = w3err[photocut]
	w4err = w4err[photocut]
	w1snr = w1snr[photocut]
	w2snr = w2snr[photocut]
	w3snr = w3snr[photocut]
	w4snr = w4snr[photocut]
	j = j[photocut]
	h = h[photocut]
	k = k[photocut]
	jerr = jerr[photocut]
	herr = herr[photocut]
	kerr = kerr[photocut]
	mrad = mrad[photocut]

	if output == True:
		outfile = open(outdir+"agn_output.dat",'w')
		fmt = "%i %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n"
		for q in range(len(catid)):
			outfile.write(fmt % (catid[q],ra[q],decl[q],gall[q],galb[q],w1[q],w2[q],w3[q],w4[q],w1err[q],w2err[q],w3err[q],w4err[q],w1snr[q],w2snr[q],w3snr[q],w4snr[q],j[q],h[q],k[q],jerr[q],herr[q],kerr[q],mrad[q]))
		outfile.close()

	else:
		return catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad


def sample_qso(output=False):
	""" Time: 12.5 seconds """

	sql = "SELECT w.vagcid, w.ra, w.decl, w.glon, w.glat, "
	sql += "w.w1, w.w2, w.w3, w.w4, "
	sql += "w.w1err, w.w2err, w.w3err, w.w4err, "
	sql += "w.w1snr, w.w2snr, w.w3snr, w.w4snr, "
	sql += "w.jmag, w.hmag, w.kmag, w.jerr, w.herr, w.kerr, "
	sql += "w.match_rad "
	sql += "FROM sdsstables.vagc_allwise_allmags AS w INNER JOIN"
	sql += " sdsstables.vagc_objects AS v ON w.vagcid = v.vagcid"
	sql += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
	sql += "(w.ccflag LIKE '0000') AND (w.w1err > -9999) AND (w.w2err > -9999) AND (w.w3err > -9999) AND "
	# sql += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND "
	# sql += "(w.jmag > -9999) AND (w.kmag > -9999) AND "
	sql += "v.CLASS LIKE 'QSO%';"

	cursor.execute(sql)
	data = cursor.fetchall()
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

	for i in range(n):
		catid[i] = data[i][0]
		ra[i] = data[i][1]
		decl[i] = data[i][2]
		gall[i] = data[i][3]
		galb[i] = data[i][4]
		w1[i] = data[i][5]
		w2[i] = data[i][6]
		w3[i] = data[i][7]
		w4[i] = data[i][8]
		w1err[i] = data[i][9]
		w2err[i] = data[i][10]
		w3err[i] = data[i][11]
		w4err[i] = data[i][12]
		w1snr[i] = data[i][13]
		w2snr[i] = data[i][14]
		w3snr[i] = data[i][15]
		w4snr[i] = data[i][16]
		j[i] = data[i][17]
		h[i] = data[i][18]
		k[i] = data[i][19]
		jerr[i] = data[i][20]
		herr[i] = data[i][21]
		kerr[i] = data[i][22]
		mrad[i] = data[i][23]

	photocut =  np.where((w1 < fntlims[0]) & (w2 < fntlims[1]) & (w3 < fntlims[2]) & (w4 < fntlims[3]) &
		(w1 > brtlims[0]) & (w2 > brtlims[1]) & (w3 > brtlims[2]) & (w4 > brtlims[3]))

	catid = catid[photocut]
	ra = ra[photocut]
	decl = decl[photocut]
	gall = gall[photocut]
	galb = galb[photocut]
	w1 = w1[photocut]
	w2 = w2[photocut]
	w3 = w3[photocut]
	w4 = w4[photocut]
	w1err = w1err[photocut]
	w2err = w2err[photocut]
	w3err = w3err[photocut]
	w4err = w4err[photocut]
	w1snr = w1snr[photocut]
	w2snr = w2snr[photocut]
	w3snr = w3snr[photocut]
	w4snr = w4snr[photocut]
	j = j[photocut]
	h = h[photocut]
	k = k[photocut]
	jerr = jerr[photocut]
	herr = herr[photocut]
	kerr = kerr[photocut]
	mrad = mrad[photocut]

	if output == True:
		outfile = open(outdir+"qso_output.dat",'w')
		fmt = "%i %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n"
		for q in range(len(catid)):
			outfile.write(fmt % (catid[q],ra[q],decl[q],gall[q],galb[q],w1[q],w2[q],w3[q],w4[q],w1err[q],w2err[q],w3err[q],w4err[q],w1snr[q],w2snr[q],w3snr[q],w4snr[q],j[q],h[q],k[q],jerr[q],herr[q],kerr[q],mrad[q]))
		outfile.close()

	else:
		return catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad


def sample_dr9sspp(output=False):
	""" Time: 1 minute """

	sql = "SELECT w.ssppid, w.ra, w.decl, w.glon, w.glat, "
	sql += "w.w1, w.w2, w.w3, w.w4, "
	sql += "w.w1err, w.w2err, w.w3err, w.w4err, "
	sql += "w.w1snr, w.w2snr, w.w3snr, w.w4snr, "
	sql += "w.jmag, w.hmag, w.kmag, w.jerr, w.herr, w.kerr, "
	sql += "w.match_rad, s.GR, s.RI, s.V_MAG, s.BV "
	sql += "FROM sdsstables.dr9_sspp_allwise_allmags AS w INNER JOIN"
	sql += " sdsstables.dr9_sspp AS s ON w.ssppid = s.ssppid"
	sql += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
	sql += "(w.ccflag LIKE '0000') AND (w.w1err > -9999) AND (w.w2err > -9999) AND (w.w3err > -9999) AND "	
	# sql += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND "
	# sql += "(w.jmag > -9999) AND (w.kmag > -9999) AND "
	sql += "s.SNR > 5;"

	cursor.execute(sql)
	data = cursor.fetchall()
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
	colgr = np.zeros(n)
	colri = np.zeros(n)
	vmag = np.zeros(n)
	colbv = np.zeros(n)

	for i in range(n):
		catid[i] = data[i][0]
		ra[i] = data[i][1]
		decl[i] = data[i][2]
		gall[i] = data[i][3]
		galb[i] = data[i][4]
		w1[i] = data[i][5]
		w2[i] = data[i][6]
		w3[i] = data[i][7]
		w4[i] = data[i][8]
		w1err[i] = data[i][9]
		w2err[i] = data[i][10]
		w3err[i] = data[i][11]
		w4err[i] = data[i][12]
		w1snr[i] = data[i][13]
		w2snr[i] = data[i][14]
		w3snr[i] = data[i][15]
		w4snr[i] = data[i][16]
		j[i] = data[i][17]
		h[i] = data[i][18]
		k[i] = data[i][19]
		jerr[i] = data[i][20]
		herr[i] = data[i][21]
		kerr[i] = data[i][22]
		mrad[i] = data[i][23]
		colgr[i] = data[i][24]
		colri[i] = data[i][25]
		vmag[i] = data[i][26]
		colbv[i] = data[i][27]

	colgi = colgr + colri

	f1 = open('/Users/Nick/Documents/AGBstuff/workstation/contaminants/locusout.dat')
	data2 = f1.readlines(); f1.close()
	giloc,grloc,grstd,riloc,ristd = np.array(data2[:138]),np.array(data2[138:276]),np.array(data2[276:414]),np.array(data2[414:552]),np.array(data2[552:690])
	giloc,grloc,grstd,riloc,ristd = giloc.astype(float),grloc.astype(float),grstd.astype(float),riloc.astype(float),ristd.astype(float)

	fit = np.polyfit(giloc,grloc,deg=4)
	ypoints = fit[0]*giloc**4 + fit[1]*giloc**3 + fit[2]*giloc**2 + fit[3]*giloc + fit[4]

	locus_and_photo = np.where((colgr < fit[0]*colgi**4 + fit[1]*colgi**3 + fit[2]*colgi**2 + fit[3]*colgi + fit[4] + 0.5) & (colgr > fit[0]*colgi**4 + fit[1]*colgi**3 + fit[2]*colgi**2 + fit[3]*colgi + fit[4] - 0.5) & 
		(w1 < fntlims[0]) & (w2 < fntlims[1]) & (w3 < fntlims[2]) & (w4 < fntlims[3]) &
		(w1 > brtlims[0]) & (w2 > brtlims[1]) & (w3 > brtlims[2]) & (w4 > brtlims[3]))

	catid = catid[locus_and_photo]
	ra = ra[locus_and_photo]
	decl = decl[locus_and_photo]
	gall = gall[locus_and_photo]
	galb = galb[locus_and_photo]
	w1 = w1[locus_and_photo]
	w2 = w2[locus_and_photo]
	w3 = w3[locus_and_photo]
	w4 = w4[locus_and_photo]
	w1err = w1err[locus_and_photo]
	w2err = w2err[locus_and_photo]
	w3err = w3err[locus_and_photo]
	w4err = w4err[locus_and_photo]
	w1snr = w1snr[locus_and_photo]
	w2snr = w2snr[locus_and_photo]
	w3snr = w3snr[locus_and_photo]
	w4snr = w4snr[locus_and_photo]
	j = j[locus_and_photo]
	h = h[locus_and_photo]
	k = k[locus_and_photo]
	jerr = jerr[locus_and_photo]
	herr = herr[locus_and_photo]
	kerr = kerr[locus_and_photo]
	mrad = mrad[locus_and_photo]
	colgr = colgr[locus_and_photo]
	colri = colri[locus_and_photo]
	vmag = vmag[locus_and_photo]
	colbv = colbv[locus_and_photo]


	if output == True:
		outfile = open(outdir+"dr9sspp_output.dat",'w')
		fmt = "%i %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n"
		for q in range(len(catid)):
			outfile.write(fmt % (catid[q],ra[q],decl[q],gall[q],galb[q],w1[q],w2[q],w3[q],w4[q],w1err[q],w2err[q],w3err[q],w4err[q],w1snr[q],w2snr[q],w3snr[q],w4snr[q],j[q],h[q],k[q],jerr[q],herr[q],kerr[q],mrad[q],colgr[q],colgi[q],vmag[q],colbv[q]))
		outfile.close()

	else:
		return catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,colgr,colgi,vmag,colbv


def retrieve_all():
	sample_simbad(output=True)
	print "SIMBAD done"

	sample_ogle3(output=True)
	print "OGLE done"

	sample_macho(output=True)
	print "MACHO done"

	sample_qso(output=True)
	print "QSOs done"

	sample_agn(output=True)
	print "AGN done"

	sample_galaxies(output=True)
	print "Galaxies done"

	sample_lrgs(output=True)
	print "LRGs done"

	sample_dr9sspp(output=True)
	print "DR9 SSPP done"


# def sample_vagcstars(output=False):
# 	sql = "SELECT w.vagcid, w.ra, w.decl, w.glon, w.glat, "
# 	sql += "w.w1, w.w2, w.w3, w.w4, "
# 	sql += "w.w1err, w.w2err, w.w3err, w.w4err, "
# 	sql += "w.w1snr, w.w2snr, w.w3snr, w.w4snr, "
# 	sql += "w.jmag, w.hmag, w.kmag, w.jerr, w.herr, w.kerr, "
# 	sql += "w.match_rad, v.u_PSFMAG, v.g_PSFMAG, v.r_PSFMAG, v.i_PSFMAG, v.z_PSFMAG, "
# 	sql += "v.u_EXTINCTION, v.g_EXTINCTION, v.r_EXTINCTION, v.i_EXTINCTION, v.z_EXTINCTION "
# 	sql += "FROM sdsstables.vagc_allwise_allmags AS w INNER JOIN"
# 	sql += " sdsstables.vagc_objects AS v ON w.vagcid = v.vagcid"
# 	sql += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
# 	sql += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND "
# 	sql += "(w.jmag > -9999) AND (w.kmag > -9999) AND v.CLASS LIKE 'STAR%';"

# 	cursor.execute(sql)
# 	data = cursor.fetchall()
# 	n = len(data)

# 	catid = np.zeros(n, int)
# 	ra = np.zeros(n)
# 	decl = np.zeros(n)
# 	gall = np.zeros(n)
# 	galb = np.zeros(n)
# 	w1 = np.zeros(n)
# 	w2 = np.zeros(n)
# 	w3 = np.zeros(n)
# 	w4 = np.zeros(n)
# 	w1err = np.zeros(n)
# 	w2err = np.zeros(n)
# 	w3err = np.zeros(n)
# 	w4err = np.zeros(n)
# 	w1snr = np.zeros(n)
# 	w2snr = np.zeros(n)
# 	w3snr = np.zeros(n)
# 	w4snr = np.zeros(n)
# 	j = np.zeros(n)
# 	h = np.zeros(n)
# 	k = np.zeros(n)
# 	jerr = np.zeros(n)
# 	herr = np.zeros(n)
# 	kerr = np.zeros(n)
# 	mrad = np.zeros(n)
# 	u_PSFMAG = np.zeros(n)
# 	g_PSFMAG = np.zeros(n)
# 	r_PSFMAG = np.zeros(n)
# 	i_PSFMAG = np.zeros(n)
# 	z_PSFMAG = np.zeros(n)
# 	u_EXTINCTION = np.zeros(n)
# 	g_EXTINCTION = np.zeros(n)
# 	r_EXTINCTION = np.zeros(n)
# 	i_EXTINCTION = np.zeros(n)
# 	z_EXTINCTION = np.zeros(n)

# 	for i in range(n):
# 		catid[i] = data[i][0]
# 		ra[i] = data[i][1]
# 		decl[i] = data[i][2]
# 		gall[i] = data[i][3]
# 		galb[i] = data[i][4]
# 		w1[i] = data[i][5]
# 		w2[i] = data[i][6]
# 		w3[i] = data[i][7]
# 		w4[i] = data[i][8]
# 		w1err[i] = data[i][9]
# 		w2err[i] = data[i][10]
# 		w3err[i] = data[i][11]
# 		w4err[i] = data[i][12]
# 		w1snr[i] = data[i][13]
# 		w2snr[i] = data[i][14]
# 		w3snr[i] = data[i][15]
# 		w4snr[i] = data[i][16]
# 		j[i] = data[i][17]
# 		h[i] = data[i][18]
# 		k[i] = data[i][19]
# 		jerr[i] = data[i][20]
# 		herr[i] = data[i][21]
# 		kerr[i] = data[i][22]
# 		mrad[i] = data[i][23]
# 		u_PSFMAG[i] = data[i][24]
# 		g_PSFMAG[i] = data[i][25]
# 		r_PSFMAG[i] = data[i][26]
# 		i_PSFMAG[i] = data[i][27]
# 		z_PSFMAG[i] = data[i][28]
# 		u_EXTINCTION[i] = data[i][29]
# 		g_EXTINCTION[i] = data[i][30]
# 		r_EXTINCTION[i] = data[i][31]
# 		i_EXTINCTION[i] = data[i][32]
# 		z_EXTINCTION[i] = data[i][33]

# 	if output == True:
# 		outfile = open(outdir+"dr9sspp_output.dat",'w')
# 		fmt = "%i %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g %g\n"
# 		for q in range(len(catid)):
# 			outfile.write(fmt % (catid[q],ra[q],decl[q],gall[q],galb[q],w1[q],w2[q],w3[q],w4[q],w1err[q],w2err[q],w3err[q],w4err[q],w1snr[q],w2snr[q],w3snr[q],w4snr[q],j[q],h[q],k[q],jerr[q],herr[q],kerr[q],mrad[q],u_PSFMAG[q],g_PSFMAG[q],r_PSFMAG[q],i_PSFMAG[q],z_PSFMAG[q],u_EXTINCTION[q],g_EXTINCTION[q],r_EXTINCTION[q],i_EXTINCTION[q],z_EXTINCTION[q]))
# 		outfile.close()

# 	else:
# 		return catid,ra,decl,gall,galb,w1,w2,w3,w4,w1err,w2err,w3err,w4err,w1snr,w2snr,w3snr,w4snr,j,h,k,jerr,herr,kerr,mrad,u_PSFMAG,g_PSFMAG,r_PSFMAG,i_PSFMAG,z_PSFMAG,u_EXTINCTION,g_EXTINCTION,r_EXTINCTION,i_EXTINCTION,z_EXTINCTION




