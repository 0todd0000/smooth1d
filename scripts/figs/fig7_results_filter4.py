
import os,pathlib
import numpy as np
from matplotlib import pyplot
import smooth1d_plot as myplot



#(1) Plot results for all datasets:
filternum  = 4
dir0       = pathlib.Path(__file__).parents[2]
dir0       = os.path.join(dir0, 'simulation_results')
varnames   = ['h0reject', 'tstar', 'tmax', 'dmax', 'rmse', 'sample_size', 'noise_amp']
windows    = [5, 10, 15]
ncomp      = 3

# ncomponents = [2, 3, 4, 5]
# window     = 5
HH0        = []
for dataset in range(6):
	H0         = []
	for window in windows:
	# for ncomp in ncomponents:
		fnameNPZ   = os.path.join(dir0, 'filter%d'%filternum, 'dataset%d_filter%d_window%d_ncomponents%d.npz' %(dataset,filternum,window,ncomp))
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
colors   = ['b', 'g', 'r', 'c', 'k']
colors   = ['0.80', '0.50', 'k']
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
labels_window = ['Window = %d' %x for x in windows]
labels_noise = ['Noise = 1%', 'Noise = 20%']
leg0 = myplot.dummy_legend(AX[0], colors=['k']*2, labels=labels_noise, linestyles=['-', '--'], linewidths=[1]*2, loc='lower left', bbox_to_anchor=(0.43, 0.45))
leg1 = myplot.dummy_legend(AX[3], colors=colors, labels=labels_window, linestyles=['-']*3, linewidths=[2]*3, loc='lower left', bbox_to_anchor=(0.33, 0.35))
for leg in [leg0,leg1]:
	pyplot.setp(leg.get_texts(), name=fontname, size=9)


fig.set_xlabels('Sample size', size=12)
fig.set_ylabels('False positive rate (%)', size=12)
fig.set_panel_labels(labels=['Dataset %d'%(i+1) for i in range(6)], pos=(0.05, 0.92), size=10, add_letters=True, with_box=False)
[ax.set_ylim(0, 115) for ax in AX]
pyplot.show()


