import numpy as np
from sklearn import mixture
import matplotlib.pyplot as plt
import os

os.chdir('/Users/Nick/Documents/AGBstuff/workstation/allwise_reboot/scripts')

f1 = '../selected_known_agbs/SIMBAD_c_rich_testset.dat'
f2 = '../selected_known_agbs/SIMBAD_o_rich_testset.dat'
# data = np.genfromtxt(f1, dtype='int,float,float,float,float,float,S8,int')

# column titles: catid,coljk,colk3,col12,col23,col34,stype)
# data1 = np.loadtxt(f1, usecols = (1,2,3,4,5,7))
# data2 = np.loadtxt(f2, usecols = (1,2,3,4,5,7))

## ==========================
## Choose my dimensions here
## ==========================
data1 = np.loadtxt(f1, usecols = (4,5,7))
data2 = np.loadtxt(f2, usecols = (4,5,7))

## ================
## Attributes here
## ================
X1 = data1[:, :-1]
X2 = data2[:, :-1]

## ==================
## Point labels here
## ==================
y1 = data1[:,-1]
y2 = data2[:,-1]

X = np.concatenate((X1,X2))
y = np.concatenate((y1,y2))

h = 0.02

col12min = min(X[:,0])
col12max = max(X[:,0])

col23min = min(X[:,1])
col23max = max(X[:,1])

# col34min = min(X[:,2])
# col34max = max(X[:,2])

## ==================================
## Setting my graph limits for later
## ==================================
xlim = (col12min, col12max) 
ylim = (col23min, col23max)
# zlim = (col34min, col34max)

# xx, yy, zz = np.meshgrid(np.linspace(xlim[0], xlim[1], 50),
# 	np.linspace(ylim[0], ylim[1], 50),
# 	np.linspace(zlim[0], zlim[1], 50))

## =============================================================
## Return coordinate matrices from 2 or more coordinate vectors
## =============================================================
xx1, yy2 = np.meshgrid(np.linspace(xlim[0], xlim[1], 50),
	np.linspace(ylim[0], ylim[1], 50))
xx1, zz2 = np.meshgrid(np.linspace(xlim[0], xlim[1], 50),
	np.linspace(zlim[0], zlim[1], 50))
yy1, zz2 = np.meshgrid(np.linspace(ylim[0], ylim[1], 50),
	np.linspace(zlim[0], zlim[1], 50))

## =============================
## Select GMMs as my classifier
## =============================
clf1 = mixture.GMM(n_components=1, n_iter=10, covariance_type = 'full')
clf2 = mixture.GMM(n_components=1, n_iter=10, covariance_type = 'full')

## =================
## Fit my data here
## =================
clf1.fit(X1)
clf2.fit(X2)

# Xgrid = np.c_[xx.ravel(), yy.ravel(), zz.ravel()]
Xgrid = np.c_[xx.ravel(), yy.ravel()]

Z1 = np.log(-clf1.score_samples(Xgrid)[0])
Z2 = np.log(-clf2.score_samples(Xgrid)[0])

Z1 = Z1.reshape(xx.shape)
Z2 = Z2.reshape(xx.shape)


fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(X1[:, 0], X1[:, 1], c='r', s=3, edgecolor='None') #crich
ax.scatter(X2[:, 0], X2[:, 1], c='b', s=3, edgecolor='None') #orich

ax.contour(xx, yy, Z1, [0.5], linewidths = 1., colors='r')
ax.contour(xx, yy, Z2, [0.5], linewidths = 1., colors='b')
# cax = ax.imshow(Z1,extent=[xlim[0],xlim[-1],ylim[0],ylim[-1]], origin='lower', cmap = plt.cm.Greys)
# fig.colorbar(cax)
ax.set_xlim(xlim)
ax.set_xlabel('W2-W3')
ax.set_ylim(ylim)
ax.set_ylabel('W3-W4')


plt.show()






