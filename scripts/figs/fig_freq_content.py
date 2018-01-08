
import os
import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot
import smoothbias1d as sb



#(0) Load datasets:
datasets   = 'challis1999a', 'challis1999b', 'challis1999c', 'challis1999d', 'challis1999e', 'twisk1994'
tt,yy      = [],[]
Q          = 1000
for dataset in datasets:
	t,y    = sb.datasets.load(dataset)
	ti     = np.linspace( t.min(), t.max(), Q )
	f      = interp1d(t, y, 'linear')
	yi     = f(ti)
	tt.append(ti)
	yy.append(yi)
yy[3] *= 100
yy[5] *= 10
# ### check:
# pyplot.close('all')
# pyplot.figure(figsize=(8,6))
# pyplot.get_current_fig_manager().window.wm_geometry("+0+0")
# ax = pyplot.axes()
# for t,y,s in zip(tt,yy,datasets):
# 	ax.plot( t, y, label=s )
# ax.set_xlim(0, 1)
# ax.legend()
# pyplot.show()


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



# pyplot.savefig('/Users/todd/Documents/Projects/projects/smooth/figs/freq_content.pdf')




# ``','``             pixel marker
# ``'o'``             circle marker
# ``'v'``             triangle_down marker
# ``'^'``             triangle_up marker
# ``'<'``             triangle_left marker
# ``'>'``             triangle_right marker
# ``'1'``             tri_down marker
# ``'2'``             tri_up marker
# ``'3'``             tri_left marker
# ``'4'``             tri_right marker
# ``'s'``             square marker
# ``'p'``             pentagon marker
# ``'*'``             star marker
# ``'h'``             hexagon1 marker
# ``'H'``             hexagon2 marker
# ``'+'``             plus marker
# ``'x'``             x marker
# ``'D'``             diamond marker
# ``'d'``             thin_diamond marker
# ``'|'``             vline marker
# ``'_'``             hline marker







