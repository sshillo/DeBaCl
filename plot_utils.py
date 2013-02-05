############################################
## Brian P. Kent
## plotUtils.py
## Created: 20120712
## Updated: 20120814
## Repository of python basic plotting functions
###########################################


###########################################
### SET UP ###
###########################################

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import matplotlib as mpl
mpl.rc('axes', labelsize=18)
mpl.rc('axes', titlesize=22) 
mpl.rc('xtick', labelsize=14)
mpl.rc('ytick', labelsize=14) 



#####################################
### UTILITY FUNCTIONS AND CLASSES ###
#####################################

def addJitter(x, width=0.5):
	'''Add uniformly distributed jittering to each entry in the numpy vector x.'''
	
	return x + width*np.random.random(np.alen(x)) - width/2.0
	
	
	
	
def makeColorMatrix(n, bg_color, bg_alpha, ix=None,
	fg_color=[228/255.0, 26/255.0, 28/255.0], fg_alpha=1.0):

	rgba = np.zeros((n, 4), dtype=np.float)
	rgba[:, 0:3] = bg_color
	rgba[:, 3] = bg_alpha
	
	if ix is not None:
		if np.array(fg_color).dtype.kind == 'i':  # then fg_color is a palette index
			palette = Palette()
			fg_color = palette.applyColorset(fg_color)
		
		rgba[ix, 0:3] = fg_color
		rgba[ix, 3] = fg_alpha
		
	return rgba




class Palette:

	def __init__(self, use='scatter'):
		self.black = np.array([0.0, 0.0, 0.0])
		if use == 'lines':
			self.colorset = np.array([
				(228, 26, 28), #red
				(55, 126, 184), #blue
				(77, 175, 74), #green
				(152, 78, 163), #purple
				(255, 127, 0), #orange
				(166, 86, 40), #brown
				(0, 206, 209), #turqoise
				(82, 82, 82), #dark gray
				(247, 129, 191), #pink	
				(184, 134, 11), #goldenrod									
				]) / 255.0
		else:
			self.colorset = np.array([
					(228, 26, 28), #red
					(55, 126, 184), #blue
					(77, 175, 74), #green
					(152, 78, 163), #purple
					(255, 127, 0), #orange
					(247, 129, 191), #pink
					(166, 86, 40), #brown
					(0, 206, 209), #turqoise
					(238, 213, 183), #bisque
					(85, 107, 47), #olive green
					(127, 255, 0), #chartreuse
					(205, 92, 92), #light red
					(0, 0, 128), #navy
					(255, 20, 147), #hot pink
					(184, 134, 11), #goldenrod
					(176, 224, 230), #light blue
					(255, 255, 51), #yellow
					(0, 250, 192),
					(13, 102, 113),
					(83, 19, 67),
					(162, 38, 132),
					(171, 15, 88),
					(82, 82, 82), #dark gray
					(150, 150, 150), #gray
					(240, 240, 240) # super light gray
					]) / 255.0
					

	


 	def applyColorset(self, ix):
 		"""
 		Turn a numpy array of group labels (integers) into RGBA colors.
 		"""

		return self.colorset[ix] 		
 	
 	
 	
 	def makeColorMap(self):
 		"""
 		Returns a matplotlib colormap indexed by integers 0,1,...,20 with good colors.
 		"""
	
		n_color = self.palette.shape[0]
		cmap = clr.ListedColormap(colors=self.palette, name='plotUtilsCMap')
		cnorm = clr.BoundaryNorm(range(n_color), n_color)
	
		return cmap, cnorm 		
 		




###########################################
### BASIC PLOTS ###
###########################################

def makeFrame(title='', xlab='x', ylab='y'):
	'''The basic framework for a matplotlib plot.'''

	fig = plt.figure(figsize=(9, 9))
#	fig.suptitle(title, weight='bold')
	ax = fig.add_subplot(111)
	ax.set_title(title)
	ax.set_xlabel(xlab); ax.set_ylabel(ylab)
	
	return fig, ax
	
	
	
	
def makeFrame3D(title='', xlab='x', ylab='y', zlab='z', size=(8,8)):
	'''The basic framework for a 3D matplotlib plot.'''

	fig = plt.figure(figsize=size)
	fig.suptitle(title, weight='bold')
	ax = fig.add_subplot(111, projection='3d')
	fig.subplots_adjust(bottom=0.0, top=1.0, left=-0.05, right=0.98)
	ax.set_xlabel(xlab); ax.set_ylabel(ylab); ax.set_zlabel(zlab)
	
	return fig	

	
	
	
def plotHist(x, b=20, freq=True, xlab='x', title=''):
	'''Plots a histogram of the entries in 'x'.
	
	Inputs
	* x - a one dimensional numpy vector
	* b - the number of bins
	* freq - if 'True' (the default), shows the count of observations per bin. Otherwise,
	the plots shows the proportion of observations per bin.'''
	
	fig = makeFrame(title, xlab)
	ax = fig.axes[0]
	ax.hist(x, bins=b, normed=(not freq))
	
	if freq:
		ax.set_ylabel('Frequency')
	else:
		ax.set_ylabel('Proportion')
	
	return fig




def plotPoints(X, size=20, clr='blue', symb='o', alpha=None, edgecolor=None, title='',
	xlab='x', ylab='y', zlab='z', azimuth=160, elev=10):
	"""
	Draw a scatterplot from the rows of numpy array 'X'.
	
	Inputs
	* X - the data array. Each row is plotted as a point.
	"""

	n, p = X.shape
	
	## Deal with 'clr' vectors
	if isinstance(clr, np.ndarray) and clr.ndim == 1:
		palette = Palette()
		clr = palette.applyColorset(clr)


	if p == 2:
		fig = makeFrame(title, xlab, ylab)
		ax = fig.axes[0]
		ax.scatter(X[:,0], X[:,1], s=size, c=clr, marker=symb, alpha=alpha,
			edgecolor=edgecolor)
		
	else:
		fig = makeFrame3D(title, xlab, ylab, zlab)
		ax = fig.axes[0]
		ax.scatter(X[:,0], X[:,1], X[:,2], s=size, c=clr, edgecolor=edgecolor)
		ax.azim = azimuth
		ax.elev = elev
			
	return fig
	
	

	
def plotError(x, y, error, xlab='x', ylab='y', title='', label=''):
	'''Plots x vs y, with symmetrical vertical error bars.'''
	
	fig = makeFrame(title, xlab, ylab)
	ax = fig.axes[0]
	ax.errorbar(x, y, yerr=error, fmt='o--', markersize=10, elinewidth=1.5, capsize=5,
		label=label)
			
	rng = max(x) - min(x)
	pad = 0.025 * rng	
	ax.set_xlim((min(x)-pad, max(x)+pad))
	ax.set_ylim((0, 1))

	return fig



############################
### SPECIFIC FANCY PLOTS ###
############################
def oneDimClusterHist(x, cluster, fhat=None, f=None, levels=None):
	"""
	Makes a histogram of the data and colors points and density estimate according to the
	clusters. 'f' is the true density, should be a two-dimensional matrix. The first column
	contains arguments on a grid, the second column contains function values. 'cluster'
	similarly should be a two column matrix with data indices in the first column and
	cluster labels in the second column.
	"""
	
	n = len(x)
	palette = Palette()
	
	## set up the figure and plot the data histogram
	fig, (ax0, ax1) = plt.subplots(2, figsize=(10, 10), sharex=True)
	ax0.set_position([0.125, 0.12, 0.8, 0.78])
	ax1.set_position([0.125, 0.05, 0.8, 0.05])

	ax1.get_yaxis().set_ticks([])
	ax0.hist(x, bins=n/20, normed=1, alpha=0.18)
	
	
	## plot the foreground points in the second axes
	for i, c in enumerate(np.unique(cluster[:, 1])):
		ix = cluster[np.where(cluster[:, 1] == c)[0], 0]
		ax1.scatter(x[ix], np.zeros((len(ix),)), alpha=0.08, s=20,
			color=palette.colorset[i])
		
		if fhat is not None:
			eps = 0.02 * (max(fhat) - min(fhat))
			ax0.set_ylim(bottom=0.0-eps, top=max(fhat)+eps)
			ax0.scatter(x[ix], fhat[ix], s=12, alpha=0.5, color=palette.colorset[i])
	
	
	## plot the true density
	if f is not None:	
		ax0.plot(f[:,0], f[:,1], color='blue', ls='-', lw=1)
	
	
	## plot the estimate density
	if fhat is not None:
		ax0.plot(x, fhat, color='black', lw=1.5, alpha=0.6)


	## plot horizontal lines at desired levels
	if levels is not None:
		for lev in levels:
			ax0.axhline(lev, color='red', lw=1, ls='--', alpha=0.7)
			
			
	
	return fig
	




