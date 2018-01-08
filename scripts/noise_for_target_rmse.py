'''
This script demonstrates three types of RMSE-relevant computation

GLOSSARY

RMSE : root mean square error
SD   : standard deviation

Types of computation:

1. Percentage RMSE (given a noisy dataset)
2. Noise amplitude (given a 1D datum and a target RMSE value)
3. Numerical validation of #2

The "dataset" variable should be one of:
	Challis1999a
	Challis1999b
	Challis1999c
	Challis1999d
	Challis1999e
	Twisk1994
'''


import numpy as np
import smooth1d



dataset   = 'Challis1999b'




#(0) Compute percentage RMSE value for one dataset given noise amplitude:
np.random.seed(0)
amp       = 3.465   #noise amplitude (SD units)
J         = 1000    #number of random 1D observations to generate
### load dataset:
t,y       = smooth1d.datasets.load(dataset)
Q         = y.size  #number of 1D continuum nodes
# yn        = y + amp * np.random.randn(Q)    #optionally run for a single noisy 1D observation
yn        = y + amp * np.random.randn(J, Q)   #multiple noisy 1D observations
rmse      = smooth1d.util.prmse(y, yn)
### report:
print( '---- PART A -----' )
print( 'Noise amplitude:  %s' %amp )
print( 'Percentage RMSE:  %s' %rmse.mean() )
print()



#(1) Compute noise amplitude for one dataset given target RMSE value:
targets   = [0.01, 0.20]   #target RMSE value
### load dataset:
t,y       = smooth1d.datasets.load(dataset)
### compute noise amplitudes
amps      = smooth1d.util.noise_for_target_rmse(y, targets)
### report:
print( '---- PART B -----' )
print( 'Target RMSE values:  %s' %targets )
print( 'Noise amplitudes:    %s' %amps )
print()



#(2) Validate a target RMSE value:
np.random.seed(0)
target    = 0.20    #target RMSE value
J         = 1000    #number of random 1D observations to generate
### load dataset:
t,y       = smooth1d.datasets.load(dataset)
### compute noise amplitude (analytically):
amp       = smooth1d.util.noise_for_target_rmse(y, target)
### verify that this amplitude yields the desired RMSE:
yn        = y + amp * np.random.randn(J, y.size)   #multiple noisy 1D observations
rmse      = smooth1d.util.prmse(y, yn)
### report:
print( '---- PART C -----' )
print( 'Target RMSE: %.5f' %target )
print( 'Actual RMSE: %.5f' %rmse.mean() )
print()


