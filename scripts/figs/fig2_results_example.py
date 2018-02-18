
import os
import numpy as np
from matplotlib import pyplot
import spm1d
import smooth1d
import myplot


# datasets   = 'Challis1999a', 'Challis1999b', 'Challis1999c', 'Challis1999d', 'Challis1999e', 'Twisk1994'



#(0) Example data sample:
dataset    = 'Challis1999e'
t,y        = smooth1d.datasets.load( dataset )
### add noise:
np.random.seed(1)
J,Q        = 5, y.size
target     = 0.20
amp        = smooth1d.util.noise_for_target_rmse(y, target)
yn         = y + amp * np.random.randn(J, Q)


#(1) Smooth with three different parameters:
cutoffs    = [3, 4, 5]
orders     = [2, 2, 2]
dt         = t[1]-t[0]
yns        = [smooth1d.smooth.butter_lowpass(yn, dt, c, order=o)   for c,o in zip(cutoffs,orders)]
### compute RMSE:
prmse0     = 100*smooth1d.util.prmse(y, yn).mean()
prmse      = [100*smooth1d.util.prmse(y, yy).mean()   for yy in yns]
### residuals:
ynsr       = [yy-y  for yy in yns]
### spm:
spmi       = [spm1d.stats.ttest(yy-y).inference(0.05)  for yy in yns]






#(2) Plot
pyplot.close('all')
fontname = u'Times New Roman'
fig      = myplot.MyFigure(figsize=(11.25,6), axx=np.linspace(0.05,0.79,4), axy=np.linspace(0.68,0.07,3), axw=0.19, axh=0.29, fontname=fontname, set_font=True, set_visible=False)
AX       = fig.AX
[  ax.set_visible(False)  for ax in AX[[0,2],0]  ]
anchor   = (1.02, 0.01)
localex  = 0.16, 0.36, 0.63, 0.82


### plot noisy dataset:
ax  = AX[1,0]
h0  = ax.plot(t, yn.T, lw=0.5, color='0.6')[0]
# h0 = ax0.plot(t, yns5.T, lw=0.5, color='r')[0]
h1  = ax.plot(t, y, lw=3, color='k')[0]
leg = ax.legend([h1,h0], ['Datum', 'Noisy sample'], loc='lower right', bbox_to_anchor=anchor)
pyplot.setp(leg.get_texts(), name=fontname, size=9)
ax.text(0.6, 0.35, 'RMSE = %.1f%s' %(prmse0,'%'), transform=ax.transAxes, name=fontname, size=9)
[ax.axvline(x, color='0.90', lw=10, zorder=-1) for x in localex]



### plot filtered datasets:
for ax,yy,rmse,c,o in zip(AX[:,1],yns,prmse,cutoffs,orders):
	h0  = ax.plot(t, yy.T, lw=0.5, color='0.6')[0]
	h1  = ax.plot(t, y, lw=3, color='k')[0]
	if ax == AX[0,1]:
		leg = ax.legend([h1,h0], ['Datum', 'Filtered sample'], loc='lower right', bbox_to_anchor=anchor)
		pyplot.setp(leg.get_texts(), name=fontname, size=9)
	ax.text(0.6, 0.35, 'RMSE = %.1f%s' %(rmse,'%'), transform=ax.transAxes, name=fontname, size=9)
	ax.text(0.1, 0.6, 'Cutoff = %d Hz\nOrder = %d' %(c,o), transform=ax.transAxes, name=fontname, size=9)
	



### plot residuals:
for ax,yy in zip(AX[:,2],ynsr):
	h0  = ax.plot(t, yy.T, lw=0.5, color='0.6')[0]
	h1  = ax.plot(t, y-y, lw=3, color='k')[0]
	if ax == AX[0,2]:
		leg = ax.legend([h1,h0], ['Datum', 'Residuals'], loc='lower right', bbox_to_anchor=anchor)
		pyplot.setp(leg.get_texts(), name=fontname, size=9)
	ax.set_ylim(-0.25, 0.25)
	[ax.axvline(x, color='0.90', lw=10, zorder=-1) for x in localex]


### plot SPM results:
for ax,spm in zip(AX[:,3],spmi):
	spm.plot(ax=ax)
	# pyplot.setp(ax.lines[0], data=(np.linspace(0,1,spm.Q),spm.z))
	ax.set_ylim(-20, 45)
	if ax==AX[0,3]:
		xx,yy,ss = [5,5,35,35], [10.8,7.0, -9.8,-13.9], ['<', '>', '>', '<']
		for x,y,s in zip(xx,yy,ss):
			ax.text(x, y, r'$\alpha$ %s 0.05' %s, name=fontname, size=9)
	[ax.axvline(128*x, color='0.90', lw=10, zorder=-1) for x in localex]
	


[ax.set_xlabel('Time (s)', name=fontname, size=12)   for ax in [AX[1,0], AX[2,1], AX[2,2], AX[2,3]]]
AX[1,0].set_ylabel('Dependent variable', name=fontname, size=12)
[ax.set_ylabel('Dependent variable', name=fontname, size=12)    for ax in AX[:,1]]
[ax.set_ylabel('Residual', name=fontname, size=12)    for ax in AX[:,2]]

[ax.set_ylabel('t value', name=fontname, size=12)   for ax in AX[:,3]]
[ax.set_xticklabels([])  for ax in AX[:2,1:].flatten()]
[ax.text(0.5, 1.03, label, name=fontname, size=12, transform=ax.transAxes, ha='center')  for ax,label in zip([AX[1,0]] + list(AX[0,1:]),['Original Dataset','Filtered', 'Residuals', 'Hypothesis Test'])]


### label panels:
x,y  = 0.05, 0.91
tx0  = AX[1,0].text(x, y, '(a)', transform=AX[1,0].transAxes)
tx1  = [ax.text(x, y, '(%s)'%chr(98+i), transform=ax.transAxes)  for i,ax in enumerate(AX[:,1:].T.flatten())]
pyplot.setp([tx0]+tx1, name=fontname, size=12)


pyplot.show()


# pyplot.savefig('/Users/todd/Documents/Projects/projects/smooth/figs/results_example.pdf')