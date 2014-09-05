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

matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['text.usetex'] = True

font = {'family':'normal', 'size':10}
axes = {'titlesize':14}
matplotlib.rc('font', **font)
matplotlib.rc('axes', **axes)

infiledir = '/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/allwise_relaxed/TRILEGAL4Nick/trilegal_1.5/outputs/'
infiles = [infiledir+f for f in os.listdir(infiledir) if f.startswith('simdata')]

colnames = np.array('Gc logAge [M/H] m_ini   logL   logTe logg  m-M0   Av    m2/m1 mbol   j      h      k     w1     w2     w3     w4     Mcore C/O Per   mode  logML       Mact'.split())
simdata = {}
nums = []
for ii in range(len(colnames)):
	simdata[colnames[ii]] = []

for ii in range(len(infiles)):
	lines = open(infiles[ii]).readlines()[1:-1]
	nums.append(len(lines))
	for line in lines:
		elements = line.split()
		for jj in range(len(elements)):
			simdata[colnames[jj]].append(eval(elements[jj]))


simdata_df = df(simdata)#, columns=colnames)

## add colors to the dataframe
simdata_df['coljk'] = simdata_df.j - simdata_df.k
simdata_df['colk3'] = simdata_df.k - simdata_df.w3
simdata_df['col12'] = simdata_df.w1 - simdata_df.w2
simdata_df['col23'] = simdata_df.w2 - simdata_df.w3
simdata_df['col34'] = simdata_df.w3 - simdata_df.w4

photo_cuts = (simdata_df['coljk'] > 1.0) & (simdata_df['col23'] > 0) & (simdata_df.w1 < 16.83) & (simdata_df.w2 < 15.6) & (simdata_df.w3 < 11.32) & (simdata_df['col34'] < -0.83*simdata_df['col23'] + 3.37)
simdata_df = simdata_df[photo_cuts]
cut1 = simdata_df['C/O'] > 1.0

fig = plt.figure(figsize=(12,6))
fig.subplots_adjust(top=0.85)
plt.subplot(121)
plt.title('(gall, galb) : (15 to 50$^\circ$, -5 to 5$^\circ$)\nC/O $>$ 1.0')
H, xed, yed = np.histogram2d(simdata_df.col23[cut1],simdata_df.col34[cut1],bins=200)
extent = [xed[0],xed[-1],yed[0],yed[-1]]
plt.imshow(np.log10(H.T), extent=extent, origin='lower', aspect='auto', interpolation='nearest', cmap=plt.cm.Greys)
plt.minorticks_on()
plt.xlabel('W2-W3')
plt.ylabel('W3-W4')
plt.ylim(-1.5,3.5)
plt.xlim(0,3.5)

cut2 = simdata_df['C/O'] < 1.0

plt.subplot(122)
plt.title('(gall, galb) : (15 to 50$^\circ$, -5 to 5$^\circ$)\nC/O $<$ 1.0')
H, xed, yed = np.histogram2d(simdata_df.col23[cut2],simdata_df.col34[cut2],bins=200)
extent = [xed[0],xed[-1],yed[0],yed[-1]]
plt.imshow(np.log10(H.T), extent=extent, origin='lower', aspect='auto', interpolation='nearest', cmap=plt.cm.Greys)
plt.minorticks_on()
plt.xlabel('W2-W3')
plt.ylabel('W3-W4')
plt.ylim(-1.5,3.5)
plt.xlim(0,3.5)
plt.show()

