'''
util.py

A collection of utility functions.
'''


from math import floor,ceil
import numpy as np



def noise_for_target_rmse(y_orig, target):
	'''
	Find Gaussian noise amplitude needed to produce a target percent
	root mean squared error (RMSE) for a particular 1D datum
	
	INPUTS:
	
	y_orig:    (1 x Q) array, 1D datum
	target:    positive float or array of floats (target percentage RMSE)
	
	OUTPUTS:
	
	x:         noise amplitude (standard deviation of Gaussian noise)
	'''
	rms   = (y_orig ** 2).mean() ** 0.5   #root-mean squared value
	return np.asarray(target) * rms   #target rmse


def paddon(y):
	'''
	Pad a 1D continuum prior to filtering
	(Code translated from a MATLAB implementation written by John Challis; 
	MATLAB code received by email without license)
	
	INPUTS:
	
	*y* : (1 x Q) array, 1D measurement
	
	OUTPUTS:
	
	*x* : 1D array, padded 1D measurement
	
	*nadd* : int, number of nodes added
	'''
	nadd = round( 0.3 * y.size )
	yp   = np.pad(y, nadd, 'reflect')
	return yp,nadd


def paddoff(y, nadd):
	'''
	Trim a padded 1D continuum
	(Code translated from a MATLAB implementation written by John Challis; 
	MATLAB code received by email without license)
	
	INPUTS:
	
	*x* : 1D array, padded 1D measurement (usually after filtering)
	
	*nadd* : int, number of nodes added by "paddon"
	
	OUTPUTS:
	
	*y* : 1D array, 1D measurement, same size as array submitted to "paddon"
	'''
	i0 = nadd
	i1 = 2 * ceil(0.5*nadd)
	return y[i0:-i1]



def round_up_to_odd(x):
	'''
	Round a number up to the nearest odd number
	'''
	return ceil(x) // 2 * 2 + 1


def prmse(y_orig, y_noisy):
	'''
	Percent root mean squared error (RMSE)
	
	INPUTS:
	
	y_orig:    (1 x Q) array
	y_noisy:   (J x Q) array
	
	OUTPUTS:
	
	x:         percent RMSE
	'''
	if y_noisy.ndim==1:
		y_noisy = np.asarray([y_noisy])
	rmse        = ((y_orig - y_noisy) ** 2).mean(axis=1) ** 0.5  #root-mean squared error
	rms         = (y_orig ** 2).mean() ** 0.5   #root-mean squared value
	return rmse / rms


def tstat(y):
	'''
	Compute the one-sample t statistic continuum
	
	INPUTS:
	
	*y* : (J x Q) array, collection of J datum-subtracted 1D measurements
	
	OUTPUTS:
	
	*x* : (1 X Q) array, t statistic continuum
	'''
	return y.mean(axis=0) / (  y.std(ddof=1, axis=0)/ (y.shape[0])**0.5  )


