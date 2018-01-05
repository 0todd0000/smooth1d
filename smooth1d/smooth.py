'''
smooth.py

Various algorithms for filtering noisy 1D data. 

Currently implemented algorithms include:

- autocorr : autocorrelation-based, optimum low-pass Butterworth filter

- butter_lowpass : low-pass Butterworth filter

- gcvspl : generalized cross-validatory spline filter

- ssa : singular Spectrum Analysis smoother

'''


import os
import ctypes
from math import sqrt,log
import numpy as np
import scipy.signal
from statsmodels.robust import mad
import pywt


from . import util
round_up_to_odd = util.round_up_to_odd
paddon          = util.paddon
paddoff         = util.paddoff



def butter_lowpass(y, dt, cutoff, order=2):
	'''
	Lowpass Butterworth filter
	
	INPUTS:
	
	*y* : 1D measurement ( (Q,) array )
	
	*dt* : inter-node duration = (1 / sampling frequency)
	
	*cutoff* : cut-off frequency (Hz) (int or float)
	
	*order* : filter order (int)

	OUTPUTS:
	
	*ys* : smoothed 1D measurement ( (Q,) array )
	'''
	cutoff    = cutoff / ( 2**0.5 - 1 ) ** (0.5/order)
	b,a       = scipy.signal.butter(order, 2*cutoff*dt, btype='lowpass')
	fdata     = scipy.signal.filtfilt( b, a, y, padtype='odd')
	return fdata


def embed(time, y, cutoffs=None, order=2):
	'''
	Embed a measurement in an abstract 2D time-cutoff space
	
	INPUTS:
	
	*time* : 1D time vector ( (Q,) array )
	
	*y* : 1D measurement ( (Q,) array )
	
	*cutoffs* : cut-off frequencies (Hz) (list of int or float)
	
	*order* : filter order (int)

	OUTPUTS:
	
	*Ys* : smoothed, embedded 1D measurement ( (J,Q) array )
	'''
	dt      = time[1] - time[0]
	cutoffs = cutoffs if cutoffs is not None else np.linspace(5, 10, 50)
	ncut    = cutoffs.size
	if y.ndim == 1:
		ye    = np.array([butter_lowpass(y, dt, xx, order=order)  for xx in cutoffs])
	elif y.ndim == 2:
		J,Q   = y.shape
		ye    = np.zeros( (J,ncut,Q) )
		for i,xx in enumerate(cutoffs):
			ye[:,i,:] = butter_lowpass(y, dt, xx, order=order)
	return ye



def _filtmat(dt, cutoff, order, data):
	'''
	(Code translated from a MATLAB implementation written by John Challis; 
	MATLAB code received by email without license)
	'''
	return butter_lowpass(data, dt, cutoff, order)



def _autocorr(nsignal, dt, order):
	'''
	(Code translated from a MATLAB implementation written by John Challis; 
	MATLAB code received by email without license)
	'''
	colow = 0.5
	coup  = 0.25 / dt
	for i,co in enumerate(np.arange(colow, coup+0.1, 0.1)):
		ssignal = _filtmat(dt, co, order, nsignal)
		resid   = ssignal - nsignal
		acorr   = np.correlate(resid, resid, mode='full')
		acorr  /= acorr.max()
		f       = np.sum( np.abs(acorr) )
		if i==0:
			fmin  = f         #objective function
			coopt = co        #(currently) optimum cutoff frequency
			s     = ssignal   #(currently) optimally smoothed signal
		if f < fmin:
			fmin  = f
			coopt = co
			s     = ssignal
	return s,coopt



def autocorr(y, order=2, time=None):
	'''
	Autocorrelation filtering method.
	
	(Code translated from a MATLAB implementation written by John Challis; 
	MATLAB code received by email from author, without license)
	
	Reference:
	
	Challis JH (1999). A procedure for the automatic determination of filter
	cutoff frequency for the processing of biomechanical data. Journal of
	Applied Biomechanics 15, 303–317.
	'''
	dt    = 1 if time is None else time[1] - time[0]
	if y.ndim == 1:
		ys,cutoff = _autocorr(y, dt, order)
	else:
		ys,xopt   = [],[]
		for yy in y:
			s,c   = _autocorr(yy, dt, order)
			ys.append(s)
			xopt.append(c)
		ys,cutoff = np.array(ys), np.array(xopt)
	return ys



def _gcvspl(x, y, order=2, library='gcvspl.so'):
	'''
	Generalized cross-validatory spline filtering 
	
	(Using this function requires a compiled dynamic link library.)
	(This code is distributed with a library called "gcvspl.so" which
	was compiled for Mac using the source code from Twisk (1994), link below.)
	
	https://isbweb.org/resources/software-resources/137-signal-processing-software/497-gcvspl-in-c-d-twisk
	
	Reference:
	
	Craven P, Wahba G (1979). Smoothing noisy data with splines functions. Numerische Mathematik 31, 377–403.
	'''
	### load DLL:
	fnameSO    = os.path.join( os.path.dirname(__file__), library)
	L          = ctypes.CDLL(fnameSO)
	### assemble required variable types
	c_int      = ctypes.c_int
	c_double   = ctypes.c_double
	p_double   = np.ctypeslib.ndpointer(ctypes.c_double)
	p_int      = np.ctypeslib.ndpointer(ctypes.c_int32)
	### specify argument types
	L.gcvspl.argtypes = [p_double, p_double, p_double, c_int, c_int, p_double, c_double, p_double, c_int]
	L.splder.argtypes = [c_int, c_int, c_int, c_double, p_double, p_double, p_int, p_double]
	L.splder.restype  = c_double
	
	K   = 1
	NN  = x.size

	MM  = 10
	MM2 = 2*MM
	NWK = NN+6*(NN*MM+1)

	c  = np.zeros(NN)
	wk = np.zeros(NWK)
	q  = np.zeros(MM+1)
	v  = np.zeros(MM2)
	q0 = np.zeros(NN)
	q1 = np.zeros(NN)
	q2 = np.zeros(NN)

	wy    = 1.0
	wx    = np.ones(NN)
	m     = order
	n     = NN
	var   = -1.0
	ier   = 0
	L.gcvspl(x, y, wx, m, n, c, var, wk, ier)

	Q         = NN
	ider      = 0  #derivative order
	t         = x.copy()
	l         = 2 * np.ones(Q, dtype=np.int32)
	q         = np.zeros(2*m)
	a         = np.array([L.splder(ider, m, n, tt, x, c, l, q)  for tt in t])
	return a



def gcvspl(x, y, order=3):
	'''
	Generalized cross-validatory spline filtering 
	
	(Using this function requires a compiled dynamic link library.)
	(This code is distributed with a library called "gcvspl.so" which
	was compiled for Mac using the source code from Twisk (1994), link below.)
	
	https://isbweb.org/resources/software-resources/137-signal-processing-software/497-gcvspl-in-c-d-twisk
	
	Reference:
	
	Craven P, Wahba G (1979). Smoothing noisy data with splines functions. Numerische Mathematik 31, 377–403.
	'''
	if y.ndim==2:
		ys    = np.array([_gcvspl(x, yy, order) for yy in y])
	else:
		ys    = _gcvspl(x, y, order)
	return ys




def _ssa(x, L=5, ncomponents=2):
	'''
	Singular Spectrum Analysis smoother
	
	Adapted from the MATLAB code "ssa.m" by Francisco Javier Alonso Sanchez
	The original MATLAB code was downloaded on 2017-11-20 from:
	
	https://www.mathworks.com/matlabcentral/fileexchange/8115-singular-spectrum-analysis-smoother?s_tid=prof_contriblnk
	
	References:
	
	Golyandina, N., Nekrutkin,  V., Zhigljavsky, A., 2001. Analisys of Time Series Structure - SSA and Related Techniques. Chapman & Hall/CR
	
	Alonso, F.J., Del Castillo, J.M, Pintado, P., (2005), Application of singular spectrum analysis to the smoothing of raw kinematic signals. J. Biomech. 38, 1085-1092.
	'''
	#Step 1: Build trajectory matrix:
	N = x.size
	L = (N - L) if (L > N/2) else L
	K = N - L + 1
	X = np.zeros((L, K))
	for i in range(K):
		X[:L, i] = x[i:L+i]
	X = np.matrix( X )

	#Step 2: SVD
	U,s,v = np.linalg.svd(X)
	V     = X.T * U
	rc    = U * V.T

	#Step 3: Grouping
	I     = range(ncomponents)
	rca   = U[:, I] * V.T[I]

	#Step 4: Reconstruction
	y  = np.zeros(N)
	Lp = min(L, K)
	Kp = max(L, K)

	for k in range(0, Lp-1):
		for m in range(k+1):
			y[k] += (1.0/(k+1)) * rca[m,k-m]

	for k in range(Lp-1, Kp):
		for m in range(Lp):
			y[k] += (1.0/Lp) * rca[m,k-m]

	for k in range(Kp, N):
		for m in range(k-Kp+1, N-Kp+1):
			y[k] += (1.0/(N-k)) * rca[m,k-m]

	return y



def ssa(y, L, ncomponents=2):
	'''
	Singular Spectrum Analysis smoother
	
	Adapted from the MATLAB code "ssa.m" by Francisco Javier Alonso Sanchez
	The original MATLAB code was downloaded on 2017-11-20 from:
	
	https://www.mathworks.com/matlabcentral/fileexchange/8115-singular-spectrum-analysis-smoother?s_tid=prof_contriblnk
	
	References:
	
	Golyandina, N., Nekrutkin,  V., Zhigljavsky, A., 2001. Analisys of Time Series Structure - SSA and Related Techniques. Chapman & Hall/CR
	
	Alonso, F.J., Del Castillo, J.M, Pintado, P., (2005), Application of singular spectrum analysis to the smoothing of raw kinematic signals. J. Biomech. 38, 1085-1092.
	'''
	if y.ndim==2:
		ys    = np.array([_ssa(yy, L, ncomponents) for yy in y])
	else:
		ys    = _ssa(y, L, ncomponents)
	return ys





def _wavelet_single(y):
	'''
	Wachowiak (2000)
	Following code from:
	http://jseabold.net/blog/2012/02/23/wavelet-regression-in-python/
	'''
	yy,nadd  = paddon(y)
	coefs    = pywt.wavedec(yy, 'db8', level=None, mode='per')
	sigma    = mad( coefs[-1] )
	uthresh  = sigma * sqrt( 2*log(len(y)) )
	denoised = coefs[:]
	denoised[1:] = (pywt.threshold(i, value=uthresh, mode='soft') for i in denoised[1:])
	ys           = pywt.waverec(denoised, 'db8', mode='per')
	ys           = paddoff(ys, nadd)
	return ys


def wavelet(y):
	'''
	Wachowiak (2000)
	Following code from:
	http://jseabold.net/blog/2012/02/23/wavelet-regression-in-python/
	'''
	if y.ndim == 1:
		ys = _wavelet_single(y)
	else:
		ys = np.array([_wavelet_single(yy) for yy in y])
	return ys



def wiener(y, window_rel=0.05):
	'''
	Weiner filter
	
	This is a convenience interface to scipy.signal.wiener
	'''
	n          = y.size if y.ndim==1 else y.shape[1]
	window     = round_up_to_odd( window_rel * n )
	ys         = np.array([scipy.signal.wiener(yy, window, None) for yy in y])
	return ys


