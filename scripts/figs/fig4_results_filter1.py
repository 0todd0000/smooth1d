
import os
import numpy as np
from matplotlib import pyplot
import smooth1d_plot as myplot





#(1) Plot results for all datasets:
filternum  = 1
dir0       = '/Users/todd/DataProc/projects/smooth/results/filter%d/' %filternum
varnames   = ['h0reject', 'tstar', 'tmax', 'dmax', 'rmse', 'sample_size', 'noise_amp']
# cutoffs    = [2, 3, 4, 5, 6, 7, 8, 9, 10]
cutoffs    = [4, 6, 8, 10]
order      = 5
HH0        = []
for dataset in range(6):
	H0         = []
	for cutoff in cutoffs:
		fnameNPZ   = dir0 + 'dataset%d_filter%d_cutoff%d_order%d.npz' %(dataset,filternum,cutoff,order)
		with np.load(fnameNPZ) as Z:
			h0,tstar,tmax,dmax,rmse,J,amp = [Z[s] for s in varnames]
			### compute false positive rate as a function of sample size and amplitude:
			uJ         = np.unique(J)
			uamp       = np.unique(amp)
			h          = np.array([[  h0[(J==j) & (amp==a)].mean()    for a in uamp]  for j in uJ])
			H0.append( 100*h )
	HH0.append(H0)
### plot:
pyplot.close('all')
fontname = u'Times New Roman'
# colors   = ['b', 'g', 'r', 'k']
colors   = ['0.90', '0.70', '0.30', 'k']
# colors   = pyplot.cm.jet(np.linspace(0,1,len(cutoffs)+2))[1:-1]
fig  = myplot.MyFigure(figsize=(8,4), axx=np.linspace(0.07,0.7,3), axy=[0.56,0.1], axw=0.29, axh=0.43, fontname=fontname, set_visible=True)
AX   = fig.AX.flatten()
for i,(ax,H0) in enumerate(zip(AX,HH0)):
	for c,h0 in zip(colors,H0):
		ax.plot(uJ, h0[:,0], 'o-', color=c, markersize=3)
		ax.plot(uJ, h0[:,1], 'o--', color=c, markersize=3)
		ax.set_xticks( np.arange(5, 51, 10) )
	ax.axhline(5, color='k', ls='--')

### create legends:
labels_cutoff = ['Cutoff = %d Hz' %x for x in cutoffs]
labels_noise = ['Noise = 1%', 'Noise = 20%']
leg0 = myplot.dummy_legend(AX[0], colors=['k']*2, labels=labels_noise, linestyles=['-', '--'], linewidths=[1]*2, loc='lower left', bbox_to_anchor=(0.43, 0.25))
leg1 = myplot.dummy_legend(AX[4], colors=colors, labels=labels_cutoff, linestyles=['-']*4, linewidths=[2]*4, loc='lower left', bbox_to_anchor=(0.03, 0.25))
for leg in [leg0,leg1]:
	pyplot.setp(leg.get_texts(), name=fontname, size=9)


fig.set_xlabels('Sample size', size=12)
fig.set_ylabels('False positive rate (%)', size=12)
fig.set_panel_labels(labels=['Dataset %d'%(i+1) for i in range(6)], pos=(0.05, 0.92), size=10, add_letters=True, with_box=False)
[ax.set_ylim(0, 115) for ax in AX]
pyplot.show()


