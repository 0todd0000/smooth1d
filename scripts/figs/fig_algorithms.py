
import numpy as np
from matplotlib import pyplot
import autosmooth
import spm1d
import myplot




#(0) Specify parameters:
np.random.seed(1)
METHODS       = 'None', 'Butterworth', 'Autocorr', 'GCVSPL', 'SSA'
COLLABELS     = 'Data sample', 'Residuals', 't statistic'
J             = 5
dataset       = 'challis1999e'
noiseamp      = 4 * 0.115 * 0.2
### algorithm-specific parameters:
butter_cutoff = 5.0
butter_order  = 2


NULL    = True
NULL    = False


#(1) Load data:
time,y0 = autosmooth.datasets.load( dataset )
Q       = y0.size
if NULL:
	y0  = np.zeros(Q)
dt      = time[1] - time[0]
### add noise:
y       = y0 + noiseamp * np.random.randn(J, Q)
### smooth:
ys0     = autosmooth.smooth.butter_lowpass(y, dt, butter_cutoff, forder=butter_order)
ys1     = autosmooth.smooth.challis(y, forder=2, time=time)
ys2     = autosmooth.smooth.spline(time, y, order=2)
ys3     = autosmooth.smooth.ssa(y, 10, 2)
YY      = [y,ys0,ys1,ys2,ys3]
### compute t statistics:
alpha   = 0.05
two_tailed = True
t       = spm1d.stats.ttest( y - y0 ).inference(alpha, two_tailed=two_tailed)
t0      = spm1d.stats.ttest( ys0 - y0 ).inference(alpha, two_tailed=two_tailed)
t1      = spm1d.stats.ttest( ys1 - y0 ).inference(alpha, two_tailed=two_tailed)
t2      = spm1d.stats.ttest( ys2 - y0 ).inference(alpha, two_tailed=two_tailed)
t3      = spm1d.stats.ttest( ys3 - y0 ).inference(alpha, two_tailed=two_tailed)
TT      = [t,t0,t1,t2,t3]



#(2) Plot
pyplot.close('all')
fontname = u'Times New Roman'
fig = myplot.MyFigure(figsize=(10,13), axx=np.linspace(0.06,0.73,3), axy=np.linspace(0.82,0.04,5), axw=0.26, axh=0.15, fontname=fontname, set_font=True, set_visible=False)
AX  = fig.AX

for i,(yy,tt) in enumerate( zip(YY,TT) ):
	ax = AX[i,0]
	h0 = ax.plot(time, yy.T, 'k', lw=0.5 )[0]
	h1 = ax.plot(time, y0, 'g', lw=2)[0]
	if i==1:
		# leg = ax.legend([h1,h0], ['True 1D mean', 'Simulated 1D observation'], loc='lower right')
		leg = ax.legend([h1,h0], ['True 1D mean', 'Simulated 1D observation'], loc='upper right', bbox_to_anchor=(0.98,1.30))
		pyplot.setp(leg.get_texts(), name=fontname, size=12)
	if NULL:
		ax.set_ylim([-0.25, 0.25])
	
	ax = AX[i,1]
	ax.plot(time, (yy-y0).T, 'k', lw=0.5)
	ax.plot(time, (y0-y0), 'g', lw=2)
	ax.set_ylim([-0.25, 0.25])

	ax = AX[i,2]
	ax.plot(time, tt.z, color='b', lw=2)
	[ax.axhline(a*tt.zstar, color='k', linestyle='--')   for a in [-1,+1]]
	ax.axhline(0, color='k', linestyle=':')
	ax.fill_between(time, tt.zstar, y2=tt.z, where=tt.z>tt.zstar, interpolate=True)
	ax.set_ylim(-15, 15)


[ax.set_xticklabels([])  for ax in AX[:-1].flatten()]

[ax.set_xlabel('Time (s)', name=fontname, size=14)  for ax in AX[-1]]
[ax.set_ylabel('Dependent variable', name=fontname, size=14)  for ax in AX[:,0]]
[ax.set_ylabel('SPM{t}', name=fontname, size=14)  for ax in AX[:,2]]
[ax.text(0.05, 0.9, '(%s)  %s' %(chr(97+i),s), name=fontname, size=12, transform=ax.transAxes)  for i,(ax,s) in enumerate(zip(AX[:,0],METHODS))]

[ax.text(0.5, 1.05, s, name=fontname, size=18, transform=ax.transAxes, ha='center')  for ax,s in zip(AX[0],COLLABELS)]


ax = AX[0,2]
ax.text(0.7, 0.78, r'$\alpha$ = 0.05', name=fontname, size=12, transform=ax.transAxes)

pyplot.show()



dirFIG   = '/Users/todd/Documents/Projects/projects/smooth/figs/'
fnamePDF = dirFIG + 'algorithms_ssize%d.pdf'%J
if NULL:
	fnamePDF = dirFIG + 'algorithms_null_ssize%d.pdf'%J
pyplot.savefig(fnamePDF)

