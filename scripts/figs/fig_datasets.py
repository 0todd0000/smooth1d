
import numpy as np
from matplotlib import pyplot
import myplot
import smooth1d



#(0) Load datasets:
np.random.seed(0)
dataset_classes = smooth1d.datasets.dataset_classes[1:]



pyplot.close('all')
fontname = u'Times New Roman'
fig = myplot.MyFigure(figsize=(9,6), axx=np.linspace(0.06,0.71,3), axy=[0.60, 0.08], axw=0.28, axh=0.36, fontname=fontname, set_font=True, set_visible=False)

AX          = fig.AX

# amps        = [0.01, 0.01, 0.01,   0.2, 0.2, 0.2]
# amps        = [0.2, 0.2, 0.2,   0.2, 0.2, 0.2]
np.random.seed(0)
for i,(ax,dataset_class) in enumerate( zip(AX.flatten(),dataset_classes)):
	dataset = dataset_class()
	t,y     = dataset.get_data()
	### add noise:
	J,Q        = 5, y.size
	sd0        = smooth1d.util.noise_for_target_rmse(y, 0.01)
	sd         = smooth1d.util.noise_for_target_rmse(y, 0.2)
	yn         = y + sd * np.random.randn(J, Q)
	
	h0 = ax.plot( t, yn.T, '0.7', lw=0.5)[0]
	h1 = ax.plot( t, y, 'k', lw=3)[0]
	if ax == AX[0,0]:
		leg = ax.legend([h0,h1], ['Datum','Noisy sample'], loc='lower left', bbox_to_anchor=(0.05,0.15))
		pyplot.setp(leg.get_texts(), name=fontname, size=8)
	ax.set_title('Dataset %d (%s)' %(i+1, dataset.get_namep()), name=fontname, size=12 )
	ax.set_xlabel('Time (s)', name=fontname, size=12)
	ax.axhline(0, color='k', ls=':')
	ax.text(0.25, 0.87, 'SD (RMSE=1%s)   = %.5f\nSD (RMSE=20%s) = %.5f' %('%',sd0,'%',sd), name=fontname, size=9, transform=ax.transAxes)
[ax.set_ylabel('Dependent variable value', name=fontname, size=12)  for ax in AX[:,0]]



pyplot.show()


# pyplot.savefig('/Users/todd/Documents/Projects/projects/smooth/figs/datasets.pdf')



