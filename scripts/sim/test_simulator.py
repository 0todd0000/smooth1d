
import numpy as np
from matplotlib import pyplot
import smooth1d





#(0) Check that Simulator is working properly:
sim      = smooth1d.sim.Simulator()
sim.set_alpha(0.05)
sim.set_dataset_name('Vaughan1982')
sim.set_sample_size(5)
sim.set_noise_amp(0.05)
# sim.set_filter('None')
# sim.set_filter('Butterworth', params=dict(cutoff=2, order=2))
# sim.set_filter('Autocorr', params=dict(order=2))
sim.set_filter('GCVSPL', params=dict(m=3))
# sim.set_filter('SSA', params=dict(window=25, ncomponents=2))
sim.generate_noisy_sample()
sim.generate_noisy_sample()
sim.filter()
### get noisy and filtered data:
t,y     = sim.get_noisy_sample()
t,ys    = sim.get_filtered_sample()
### plot:
pyplot.close('all')
pyplot.figure(figsize=(8,6))
pyplot.get_current_fig_manager().window.wm_geometry("+0+0")
ax = pyplot.subplot(221);  ax.plot( t, y.T );   ax.set_title('Noisy data')
ax = pyplot.subplot(222);  ax.plot( t, ys.T );  ax.set_title('Filtered data')
pyplot.show()










