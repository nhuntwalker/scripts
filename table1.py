import numpy as np
import MySQLdb
import locale
import os
import retrieve_samples as get

db = MySQLdb.connect(host='localhost', user='root', passwd='root')
cursor = db.cursor()

locale.setlocale(locale.LC_ALL, 'en_US')

os.chdir('/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/scripts')


## Make a table of objects before and after reduction
sql_ogle_orich = "SELECT COUNT(*) FROM agbtables.ogle3_allwise_allmags AS w INNER JOIN agbtables.ogle3_agbs AS o ON w.ogleid = o.ogle3cnt WHERE o.spectr LIKE 'O-rich';"
sql_ogle_crich = "SELECT COUNT(*) FROM agbtables.ogle3_allwise_allmags AS w INNER JOIN agbtables.ogle3_agbs AS o ON w.ogleid = o.ogle3cnt WHERE o.spectr LIKE 'C-rich';"

sql_simbad_c = "SELECT COUNT(*) FROM agbtables.simbad_allwise_allmags AS w INNER JOIN agbtables.simbad_agbs AS s ON w.simbadid = s.simbadid WHERE s.startype LIKE 'C*';"
sql_simbad_o = "SELECT COUNT(*) FROM agbtables.simbad_allwise_allmags AS w INNER JOIN agbtables.simbad_agbs AS s ON w.simbadid = s.simbadid WHERE s.startype LIKE 'OH/IR';"
sql_simbad_s = "SELECT COUNT(*) FROM agbtables.simbad_allwise_allmags AS w INNER JOIN agbtables.simbad_agbs AS s ON w.simbadid = s.simbadid WHERE s.startype LIKE 'S*';"
sql_simbad_mira = "SELECT COUNT(*) FROM agbtables.simbad_allwise_allmags AS w INNER JOIN agbtables.simbad_agbs AS s ON w.simbadid = s.simbadid WHERE s.startype LIKE 'Mira';"
sql_simbad_agb = "SELECT COUNT(*) FROM agbtables.simbad_allwise_allmags AS w INNER JOIN agbtables.simbad_agbs AS s ON w.simbadid = s.simbadid WHERE s.startype LIKE 'AGB*';"

sql_macho1 = "SELECT COUNT(*) FROM agbtables.macho_allwise_allmags AS w INNER JOIN agbtables.macho_lpvs AS m ON w.machoid = m.machoid WHERE m.sequence LIKE 'seq1';"
sql_macho2 = "SELECT COUNT(*) FROM agbtables.macho_allwise_allmags AS w INNER JOIN agbtables.macho_lpvs AS m ON w.machoid = m.machoid WHERE m.sequence LIKE 'seq2';"
sql_macho3 = "SELECT COUNT(*) FROM agbtables.macho_allwise_allmags AS w INNER JOIN agbtables.macho_lpvs AS m ON w.machoid = m.machoid WHERE m.sequence LIKE 'seq3';"
sql_macho4 = "SELECT COUNT(*) FROM agbtables.macho_allwise_allmags AS w INNER JOIN agbtables.macho_lpvs AS m ON w.machoid = m.machoid WHERE m.sequence LIKE 'seq4';"

cursor.execute(sql_ogle_orich)
ogle_orich_count = int(cursor.fetchall()[0][0])
cursor.execute(sql_ogle_crich)
ogle_crich_count = int(cursor.fetchall()[0][0])

cursor.execute(sql_simbad_o)
simbad_orich_count = int(cursor.fetchall()[0][0])
cursor.execute(sql_simbad_c)
simbad_crich_count = int(cursor.fetchall()[0][0])
cursor.execute(sql_simbad_s)
simbad_s_count = int(cursor.fetchall()[0][0])
cursor.execute(sql_simbad_mira)
simbad_mira_count = int(cursor.fetchall()[0][0])
cursor.execute(sql_simbad_agb)
simbad_agb_count = int(cursor.fetchall()[0][0])

cursor.execute(sql_macho1)
macho_s1_count = int(cursor.fetchall()[0][0])
cursor.execute(sql_macho2)
macho_s2_count = int(cursor.fetchall()[0][0])
cursor.execute(sql_macho3)
macho_s3_count = int(cursor.fetchall()[0][0])
cursor.execute(sql_macho4)
macho_s4_count = int(cursor.fetchall()[0][0])

## ========
simc = "SELECT count(*) FROM agbtables.simbad_allwise_allmags AS w "
simc += "INNER JOIN agbtables.simbad_agbs AS s ON w.simbadid = s.simbadid"
simc += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
simc += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND"
simc += " (w.jmag > -9999) AND (w.kmag > -9999) AND s.startype LIKE 'C*';"
cursor.execute(simc)
simbad_crich_reduced = int(cursor.fetchall()[0][0])

simo = "SELECT count(*) FROM agbtables.simbad_allwise_allmags AS w "
simo += "INNER JOIN agbtables.simbad_agbs AS s ON w.simbadid = s.simbadid"
simo += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
simo += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND"
simo += " (w.jmag > -9999) AND (w.kmag > -9999) AND s.startype LIKE 'OH/IR';"
cursor.execute(simo)
simbad_orich_reduced = int(cursor.fetchall()[0][0])

simmira = "SELECT count(*) FROM agbtables.simbad_allwise_allmags AS w "
simmira += "INNER JOIN agbtables.simbad_agbs AS s ON w.simbadid = s.simbadid"
simmira += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
simmira += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND"
simmira += " (w.jmag > -9999) AND (w.kmag > -9999) AND s.startype LIKE 'Mira';"
cursor.execute(simmira)
simbad_mira_reduced = int(cursor.fetchall()[0][0])

sims = "SELECT count(*) FROM agbtables.simbad_allwise_allmags AS w "
sims += "INNER JOIN agbtables.simbad_agbs AS s ON w.simbadid = s.simbadid"
sims += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
sims += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND"
sims += " (w.jmag > -9999) AND (w.kmag > -9999) AND s.startype LIKE 'S*';"
cursor.execute(sims)
simbad_s_reduced = int(cursor.fetchall()[0][0])

simagb = "SELECT count(*) FROM agbtables.simbad_allwise_allmags AS w "
simagb += "INNER JOIN agbtables.simbad_agbs AS s ON w.simbadid = s.simbadid"
simagb += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
simagb += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND"
simagb += " (w.jmag > -9999) AND (w.kmag > -9999) AND s.startype LIKE 'AGB*';"
cursor.execute(simagb)
simbad_agb_reduced = int(cursor.fetchall()[0][0])

# ----------

ogleo = "SELECT count(*) FROM agbtables.ogle3_allwise_allmags AS w "
ogleo += "INNER JOIN agbtables.ogle3_agbs AS o ON w.ogleid = o.ogle3cnt"
ogleo += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
ogleo += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND"
ogleo += " (w.jmag > -9999) AND (w.kmag > -9999) AND o.spectr LIKE 'O-rich';"
cursor.execute(ogleo)
ogle_orich_reduced = int(cursor.fetchall()[0][0])

oglec = "SELECT count(*) FROM agbtables.ogle3_allwise_allmags AS w "
oglec += "INNER JOIN agbtables.ogle3_agbs AS o ON w.ogleid = o.ogle3cnt"
oglec += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
oglec += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND"
oglec += " (w.jmag > -9999) AND (w.kmag > -9999) AND o.spectr LIKE 'C-rich';"
cursor.execute(oglec)
ogle_crich_reduced = int(cursor.fetchall()[0][0])

# ----------

mach1 = "SELECT count(*) FROM agbtables.macho_allwise_allmags AS w "
mach1 += "INNER JOIN agbtables.macho_lpvs AS m ON w.machoid = m.machoid"
mach1 += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
mach1 += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND"
mach1 += " (w.jmag > -9999) AND (w.kmag > -9999) AND m.sequence LIKE 'seq1';"
cursor.execute(mach1)
macho_s1_reduced = int(cursor.fetchall()[0][0])

mach2 = "SELECT count(*) FROM agbtables.macho_allwise_allmags AS w "
mach2 += "INNER JOIN agbtables.macho_lpvs AS m ON w.machoid = m.machoid"
mach2 += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
mach2 += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND"
mach2 += " (w.jmag > -9999) AND (w.kmag > -9999) AND m.sequence LIKE 'seq2';"
cursor.execute(mach2)
macho_s2_reduced = int(cursor.fetchall()[0][0])

mach3 = "SELECT count(*) FROM agbtables.macho_allwise_allmags AS w "
mach3 += "INNER JOIN agbtables.macho_lpvs AS m ON w.machoid = m.machoid"
mach3 += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
mach3 += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND"
mach3 += " (w.jmag > -9999) AND (w.kmag > -9999) AND m.sequence LIKE 'seq3';"
cursor.execute(mach3)
macho_s3_reduced = int(cursor.fetchall()[0][0])

mach4 = "SELECT count(*) FROM agbtables.macho_allwise_allmags AS w "
mach4 += "INNER JOIN agbtables.macho_lpvs AS m ON w.machoid = m.machoid"
mach4 += " WHERE (w.n2mass = 1) AND (w.match_rad <= 2.0) AND "
mach4 += "(w.w1snr > 3) AND (w.w2snr > 3) AND (w.w3snr > 3) AND (w.w4snr > 3) AND"
mach4 += " (w.jmag > -9999) AND (w.kmag > -9999) AND m.sequence LIKE 'seq4';"
cursor.execute(mach4)
macho_s4_reduced = int(cursor.fetchall()[0][0])

# ----------

sql_agn = "SELECT COUNT(*) FROM sdsstables.vagc_allwise_allmags AS w INNER JOIN sdsstables.vagc_objects AS v ON w.vagcid = v.vagcid WHERE v.SUBCLASS LIKE 'AGN%';"
sql_qso = "SELECT COUNT(*) FROM sdsstables.vagc_allwise_allmags AS w INNER JOIN sdsstables.vagc_objects AS v ON w.vagcid = v.vagcid WHERE v.CLASS LIKE 'QSO%';"
sql_lrg = "SELECT COUNT(*) FROM sdsstables.lrg_allwise_allmags;"
sql_star = "SELECT COUNT(*) FROM sdsstables.dr9_sspp_allwise_allmags;"
sql_gal = "SELECT COUNT(*) FROM sdsstables.vagc_allwise_allmags AS w INNER JOIN sdsstables.vagc_objects AS v ON w.vagcid = v.vagcid WHERE v.CLASS LIKE 'GALAXY' AND v.SUBCLASS NOT LIKE 'AGN%';"

cursor.execute(sql_agn)
agn_count = int(cursor.fetchall()[0][0])
cursor.execute(sql_qso)
qso_count = int(cursor.fetchall()[0][0])
cursor.execute(sql_lrg)
lrg_count = int(cursor.fetchall()[0][0])
cursor.execute(sql_star)
star_count = int(cursor.fetchall()[0][0])
cursor.execute(sql_gal)
gal_count = int(cursor.fetchall()[0][0])

## ==========
outdir = "/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/refined_matches/"

# machodata = open(outdir+'macho_output.dat').readlines()
# ogledata = open(outdir+'ogle_output.dat').readlines()

agndata = open(outdir+'agn_output.dat').readlines()
qsodata = open(outdir+'qso_output.dat').readlines()
lrgdata = open(outdir+'lrg_output.dat').readlines()
stardata = open(outdir+'dr9sspp_output.dat').readlines()
galdata = open(outdir+'galaxies_output.dat').readlines()

table = "\hline\n"
table += "Population & SIMBAD C stars & OH/IR stars & Miras & S stars & AGB stars \\\\\n"
table += "\hline\n"
table += "Initial & %s & %s & %s & %s & %s \\\\\n" % (locale.format("%d", simbad_crich_count, grouping=True),locale.format("%d", simbad_orich_count, grouping=True),locale.format("%d", simbad_mira_count, grouping=True),locale.format("%d", simbad_s_count, grouping=True),locale.format("%d", simbad_agb_count, grouping=True))
table += "Reduced & %s & %s & %s & %s & %s \\\\\n" % (locale.format("%d", simbad_crich_reduced, grouping=True),locale.format("%d", simbad_orich_reduced, grouping=True),locale.format("%d", simbad_mira_reduced, grouping=True),locale.format("%d", simbad_s_reduced, grouping=True),locale.format("%d", simbad_agb_reduced, grouping=True))
table += "\hline\hline\n"

table += "Population & MACHO seq1 & seq2 & seq3 & seq4\\\\\n"
table += "\hline\n"
table += "Initial & %s & %s & %s & %s \\\\\n" % (locale.format("%d", macho_s1_count, grouping=True),locale.format("%d", macho_s2_count, grouping=True),locale.format("%d", macho_s3_count, grouping=True),locale.format("%d", macho_s4_count, grouping=True))
table += "Reduced & %s & %s & %s & %s \\\\\n" % (locale.format("%d", macho_s1_reduced, grouping=True),locale.format("%d", macho_s2_reduced, grouping=True),locale.format("%d", macho_s3_reduced, grouping=True),locale.format("%d", macho_s4_reduced, grouping=True))
table += "\hline\hline\n"

table += "Population & OGLE C-rich & O-rich\\\\\n"
table += "\hline\n"
table += "Initial & %s & %s \\\\\n" % (locale.format("%d", ogle_crich_count, grouping=True),locale.format("%d", ogle_orich_count, grouping=True))
table += "Reduced & %s & %s \\\\\n" % (locale.format("%d", ogle_crich_reduced, grouping=True),locale.format("%d", ogle_orich_reduced, grouping=True))
table += "\hline\hline\n"

table += "Population & Locus Stars & AGN & LRG & QSO & Galaxies \\\\\n"
table += "\hline\n"
table += "Initial & %s & %s & %s & %s & %s \\\\\n" % (locale.format("%d", star_count, grouping=True),locale.format("%d", agn_count, grouping=True),locale.format("%d", lrg_count, grouping=True),locale.format("%d", qso_count, grouping=True),locale.format("%d", gal_count, grouping=True))
table += "Reduced & %s & %s & %s & %s & %s \\\\\n" % (locale.format("%d", len(stardata), grouping=True),locale.format("%d", len(agndata), grouping=True),locale.format("%d", len(lrgdata), grouping=True),locale.format("%d", len(qsodata), grouping=True),locale.format("%d", len(galdata), grouping=True))
table += "\hline\n"

print table



