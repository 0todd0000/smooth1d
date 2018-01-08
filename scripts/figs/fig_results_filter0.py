
import os
import numpy as np
from matplotlib import pyplot
import myplot


# #(0) Check one dataset:
# dir0       = '/Users/todd/DataProc/projects/smooth/results/filter0/'
# dataset    = 0
# varnames   = ['h0reject', 'tstar', 'tmax', 'dmax', 'rmse', 'sample_size', 'noise_amp']
# fnameNPZ   = dir0 + 'dataset%d_filter0.npz' %dataset
# with np.load(fnameNPZ) as Z:
# 	h0,tstar,tmax,dmax,rmse,J,amp = [Z[s] for s in varnames]
# ### compute false positive rate as a function of sample size and amplitude:
# uJ         = np.unique(J)
# uamp       = np.unique(amp)
# H0         = np.array([[  h0[(J==j) & (amp==a)].mean()    for a in uamp]  for j in uJ])
# ### plot:
# pyplot.close('all')
# pyplot.figure(figsize=(8,6))
# pyplot.get_current_fig_manager().window.wm_geometry("+0+0")
# ax = pyplot.axes();  ax.plot(uJ, H0, 'o-')
# # ax = pyplot.subplot(222);  ax.plot(zstar)
# # ax = pyplot.subplot(223);  ax.plot( rmse )
# # ax.plot( y )
# pyplot.show()



#(1) Check all datasets:
dir0       = '/Users/todd/DataProc/projects/smooth/results/filter0/'
varnames   = ['h0reject', 'tstar', 'tmax', 'dmax', 'rmse', 'sample_size', 'noise_amp']
H0         = []
for dataset in range(6):
	fnameNPZ   = dir0 + 'dataset%d_filter0.npz' %dataset
	with np.load(fnameNPZ) as Z:
		h0,tstar,tmax,dmax,rmse,J,amp = [Z[s] for s in varnames]
		### compute false positive rate as a function of sample size and amplitude:
		uJ         = np.unique(J)
		uamp       = np.unique(amp)
		h          = np.array([[  h0[(J==j) & (amp==a)].mean()    for a in uamp]  for j in uJ])
		H0.append( 100*h )
### plot:
pyplot.close('all')
fontname = u'Times New Roman'
fig  = myplot.MyFigure(figsize=(8,4), axx=np.linspace(0.07,0.7,3), axy=[0.56,0.1], axw=0.29, axh=0.43, fontname=fontname, set_visible=True)
AX   = fig.AX.flatten()
for i,(ax,h0) in enumerate(zip(AX,H0)):
	ax.plot(uJ, h0[:,0], 'o-', color='k', label='Noise amp = 1%')
	ax.plot(uJ, h0[:,1], 'o-', color='0.7', label='Noise amp = 20%')
	ax.set_xticks( np.arange(5, 51, 10) )
	ax.axhline(5, color='k', ls='--')
	if i==0:
		leg = ax.legend(loc='lower right')
		pyplot.setp(leg.get_texts(), name=fontname, size=10)
fig.set_xlabels('Sample size', size=12)
fig.set_ylabels('False positive rate (%)', size=12)
fig.set_panel_labels(labels=['Dataset %d'%(i+1) for i in range(6)], pos=(0.05, 0.92), size=10, add_letters=True, with_box=False)
[ax.set_ylim(0, 10) for ax in AX]
pyplot.show()


# pyplot.savefig('/Users/todd/Documents/Projects/projects/smooth/figs/results_filter0.pdf')