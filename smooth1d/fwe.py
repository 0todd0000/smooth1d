'''
fwe.py

A variety of procedures for computing family-wise error (FWE) rates.

All procedures implement corrections for multiple comparisons across a set of one-dimensional continuum nodes.

Procedures include:

- bonferroni   (Bonferroni correction, assumes that data at adjacent time nodes are uncorrelated)

- spm   (Statistical Parametric Mapping, asseses inter-node correlation and uses random field theory to compute FWE parametrically)

- snpm   (Statistical non-Parametric Mapping, asseses inter-node correlation implicitly through permutation-based test statistic distibution construction)

- uncorrected  (No multiple comparisons correction;  this will produce accurate FWE rates only if there is a single time node)

References:

- Friston, K. J., Ashburner, J. T., Kiebel, S. J., Nichols, T. E., Penny, W. D., 2007. Statistical Parametric Mapping: The Analysis of Functional Brain Images. London: Elsevier.

- Pataky, T. C., 2016. rft1d: Smooth one-dimensional random field upcrossing probabilities in Python. Journal of Statistical Software 71, 1–22.

- www.spm1d.org
'''


import numpy as np
from scipy import stats
import spm1d

from . import smooth
from . import util
tstat = util.tstat







def bonferroni(y, y0, alpha=0.05, two_tailed=True):
	'''
	Bonferroni correction
	
	Assumes that data at adjacent time nodes are uncorrelated.
	
	Arguments:
	
	*y* : collection of J noisy 1D measurements ( (J,Q) NumPy array )
	
	*y0* : datum continuum ( (Q,) NumPy array )
	
	*alpha* : Type I error rate
	
	*two_tailed* : whether or not two-tailed inference should be employed (bool)
	'''
	J,Q  = y.shape
	p    = 0.5 * alpha if two_tailed else False
	pth  = 1 - (1-alpha)**(1/float(Q))
	tth  = stats.t.isf(pth, J-1)
	t    = tstat(y - y0)
	h0reject = np.abs(t).max() > tth
	return h0reject



def spm(y, y0, alpha=0.05, two_tailed=True):
	'''
	Statistical Parametric Mapping
	
	Asseses inter-node correlation and uses random field theory to compute probabilities parametrically
	
	Arguments:
	
	*y* : collection of J noisy 1D measurements ( (J,Q) NumPy array )
	
	*y0* : datum continuum ( (Q,) NumPy array )
	
	*alpha* : Type I error rate
	
	*two_tailed* : whether or not two-tailed inference should be employed (bool)
	'''
	ti = spm1d.stats.ttest(y-y0).inference(alpha=alpha, two_tailed=two_tailed)
	return ti.h0reject, np.abs(ti.z).max(), ti.zstar



def snpm(y, y0, alpha=0.05, two_tailed=True):
	'''
	Statistical non-Parametric Mapping
	
	Asseses inter-node correlation implicitly through permutation-based test statistic distibution construction
	
	Arguments:
	
	*y* : collection of J noisy 1D measurements ( (J,Q) NumPy array )
	
	*y0* : datum continuum ( (Q,) NumPy array )
	
	*alpha* : Type I error rate
	
	*two_tailed* : whether or not two-tailed inference should be employed (bool)
	'''
	ti = spm1d.stats.nonparam.ttest(y-y0).inference(alpha=alpha, two_tailed=two_tailed)
	return ti.h0reject, np.abs(ti.z).max(), ti.zstar



def uncorrected(y, y0, alpha=0.05, two_tailed=True):
	'''
	Uncorrected inference (i.e. no correction for multiple comparisons across multiple time nodes)
	
	This procedure produces accurate FWE rates only if (a) there is a single time node, or equivalently:
	(b) if all 1D measurements are infinitely smooth
	
	Arguments:
	
	*y* : collection of J noisy 1D measurements ( (J,Q) NumPy array )
	
	*y0* : datum continuum ( (Q,) NumPy array )
	
	*alpha* : Type I error rate
	
	*two_tailed* : whether or not two-tailed inference should be employed (bool)
	'''
	J,Q  = y.shape
	p    = 0.5 * alpha if two_tailed else False
	tth  = stats.t.isf(p, J-1)
	### t stat:
	t    = tstat(y - y0)
	h0reject = np.abs(t).max() > tth
	return h0reject
