
'''
Standlone simulation (free from smooth1d.sim convenience functions)

This script is procedural, and emphasizes how smoothed.sim's
object-oriented approach works.

This script uses just:
- a single 1D datum
- a single sample size
- a single noise amplitude
- a single smoothing procedure

The functions and classes in smooth1d.sim facilitate
simulation for arbitrary datasets, sample sizes, etc.
'''

import numpy as np
from matplotlib import pyplot
import spm1d
import smooth1d




#(0) Load 1D datum:
dataset    = 'Challis1999e'
t,y        = smooth1d.datasets.load( dataset )



#(1) Initialize simulation:
np.random.seed(1)     #seed random number generator
alpha      = 0.05     #Type I error rate
### set counts:
nIter      = 50       #number of simulation iterations (>500 for numerical convergence)
J          = 5        #number of observations (sample size)
Q          = y.size   #number of continuum nodes
### set noise parameters:
target     = 0.20     #target noise level
amp        = smooth1d.util.noise_for_target_rmse(y, target)  #noise amplitude
### set smoothing parameters:
dt         = t[1]-t[0]
cutoff     = 4
order      = 2
### initialize outputs:
false_pos  = []       #false positives (store one bool value for each iteration)



#(2) Simulate:
for i in range(nIter):
	yn     = y + amp * np.random.randn(J, Q)   #noisy dataset
	yns    = smooth1d.smooth.butter_lowpass(yn, dt, cutoff, order)   #smoothed data
	### one-sample t test (comparing the sample to its known datum):
	spmi   = spm1d.stats.ttest(yns-y).inference(alpha)  #computes 1D t statistic and conducted inference 
	false_pos.append( spmi.h0reject )   #"h0reject" is True when maximum 1D difference is statistically significant
	print(   'Iteration %d, false positive = %s' %(i, spmi.h0reject)   )
### summarize:
fpr        = 100 * np.mean(false_pos)
print(   'False positive rate = {0:.1f}%'.format( fpr )   )










