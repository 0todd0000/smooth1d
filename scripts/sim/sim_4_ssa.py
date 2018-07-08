
import os
import time
import smooth1d





#(0) Simulate one dataset, multuple parameters:
nIterations = 1000
JJ          = [5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 45, 50] #sample sizes
noise_amps  = [0.01, 0.20]
windows     = [5, 10, 15, 20, 25]
ncomponents = [2, 3, 4, 5]
### simulate:
for window in windows:
	for ncomp in ncomponents:
		
		sim         = smooth1d.sim.Simulator()
		sim.set_alpha(0.05)
		# sim.set_dataset_name('Vaughan1982')
		# sim.set_dataset_name('Challis1999a')
		# sim.set_dataset_name('Challis1999b')
		# sim.set_dataset_name('Challis1999c')
		# sim.set_dataset_name('Challis1999d')
		sim.set_dataset_name('Challis1999e')
		sim.set_filter('SSA', params=dict(window=window, ncomponents=ncomp))
		sim.set_metadata_labels(['sample_size','noise_amp'], types=[int,float])
		sim.set_results_directory( os.path.dirname(__file__) )
		sim.set_seed()
		
		
		for J in JJ:
			for amp in noise_amps:
				print('SSA:   Dataset=%d, Window=%d, nComp=%d, J=%d, Noise=%.2f' %(sim.get_dataset_index(),window,ncomp,J,amp))
				t0 = time.time()
				sim.set_sample_size( J )
				sim.set_noise_amp( amp )
				sim.simulate(nIterations, metadata=[J, amp])
				sim.save()
				print('Elapsed time:  %.1f' %(time.time()-t0))









