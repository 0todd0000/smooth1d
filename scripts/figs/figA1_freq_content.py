
import os
import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot
import smooth1d



#(0) Load datasets:
datasets   = 'Challis1999a', 'Challis1999b', 'Challis1999c', 'Challis1999d', 'Challis1999e', 'Vaughan1982'
tt,yy      = [],[]
Q          = 1000
for dataset in datasets:
	t,y    = smooth1d.datasets.load(dataset)
	ti     = np.linspace( t.min(), t.max(), Q )
	f      = interp1d(t, y, 'linear')
	yi     = f(ti)
	tt.append(ti)
	yy.append(yi)
yy[3] *= 100
yy[5] *= 10




#(1) Compute frequency content:
x,power    = [], []
for t,y in zip(tt,yy):
	dt     = t[1]-t[0]
	ps     = np.abs( np.fft.fft(y) )**2
	freqs  = np.fft.fftfreq( Q, dt )
	freqs  = np.abs(freqs)
	idx    = np.argsort(freqs)
	x.append( freqs[idx] )
	power.append( ps[idx] )



#(2) Plot:
pyplot.close('all')
pyplot.figure(figsize=(4.8,3.5))
fontname = u'Times New Roman'
pyplot.get_current_fig_manager().window.wm_geometry("+0+0")
ax = pyplot.axes([0.12,0.14,0.86,0.84])
# ax.plot( freqs[idx], ps[idx] )
symbols = 'o', 'o', 's', 's', 'v', 'v'
colors  = '0.0', '0.7', '0.0', '0.7', '0.0', '0.7'
for i,(xx,pp,sym,c) in enumerate( zip(x, power, symbols, colors) ):
	ax.plot( xx, 100 * np.cumsum(pp) / pp.sum(), '%s-'%sym, color=c, label='Dataset %d'%(i+1) )
ax.axhline(80, color='k', ls='--')
ax.set_xlim(-0.1, 5.1)
ax.set_xlabel('Frequency (Hz)', size=14, name=fontname)
ax.set_ylabel('Cumulative spectral power (%)', size=14, name=fontname)
pyplot.setp(ax.get_xticklabels() + ax.get_yticklabels(), name=fontname)
leg = ax.legend()
pyplot.setp(leg.get_texts(), name=fontname)
pyplot.show()








