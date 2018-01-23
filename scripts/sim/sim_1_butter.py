
import os
import time
import smooth1d





#(0) Simulate one dataset, multuple parameters:
nIterations = 1000
JJ          = [5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 45, 50]
noise_amps  = [0.01, 0.20]
cutoffs     = [2, 3, 4, 5, 6, 7, 8, 9, 10]
orders      = [2, 3, 4, 5]
### simulate:
for cutoff in cutoffs:
	for order in orders:
		
		sim         = smooth1d.sim.Simulator()
		sim.set_alpha(0.05)
		# sim.set_dataset_name('Vaughan1982')
		# sim.set_dataset_name('Challis1999a')
		# sim.set_dataset_name('Challis1999b')
		# sim.set_dataset_name('Challis1999c')
		# sim.set_dataset_name('Challis1999d')
		sim.set_dataset_name('Challis1999e')
		sim.set_filter('Butterworth', params=dict(cutoff=cutoff, order=order))
		sim.set_metadata_labels(['sample_size','noise_amp'], types=[int,float])
		sim.set_results_directory( os.path.dirname(__file__) )
		sim.set_seed()
		
		
		for J in JJ:
			for amp in noise_amps:
				print('Cutoff = %d, order = %d, Sample size = %d, Noise amplitude = %.2f' %(cutoff,order,J,amp))
				t0 = time.time()
				sim.set_sample_size( J )
				sim.set_noise_amp( amp )
				sim.simulate(nIterations, metadata=[J, amp])
				sim.save()
				print('Elapsed time:  %.1f' %(time.time()-t0))









