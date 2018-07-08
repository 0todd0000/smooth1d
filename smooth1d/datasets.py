'''
datasets.py

A collection of 1D datum continua for filtering performance evaluation.

Datasets are taken from two sources:

- Challis JH (1999). A procedure for the automatic determination of filter
cutoff frequency for the processing of biomechanical data. Journal of
Applied Biomechanics 15, 303-317.

- Vaughan CL (1982). Smoothing and differentiation of displacement-time
data: an application of splines and digital filtering. International
Journal of Bio-Medical Computing 13, 375–386.

An additional null datum (containing zeros) is provided.
'''



from math import pi,sin
import numpy as np


dataset_names = ['Challis1999a',
				'Challis1999b',
				'Challis1999c',
				'Challis1999d',
				'Challis1999e',
				'Null',
				'Vaughan1982']




class _Dataset(object):
	'''
	Abstract template class for all datasets
	'''
	author = None   #Author's name
	name   = None   #Dataset name
	year   = None   #Year of publication / dissemination
	y      = None   #The 1D datum continuum
	t      = None   #Time vector
	dt     = None   #Duration between time nodes (s)
	hz     = None   #Sample frequency (Hz)
	
	def get_data(self):
		'''
		Get time vector and 1D datum continuum
		
		Arguments:
		
		(None)
		
		Returns:
		
		*t* : time vector (1D NumPy array)
		
		*y* : 1D datum continuum  (1D NumPy array)
		'''
		return self.t, self.y
	
	def get_name(self):
		'''
		Get dataset name.
		
		Arguments:
		
		(None)
		
		Returns:
		
		*s* : dataset name (str)
		'''
		s  = self.author
		if self.year is not None:
			s += ' (%s)' %self.year
		if self.name is not None:
			s += ' %s' %self.name
		return s

	def get_namep(self):
		s  = self.author
		if self.year is not None:
			s += ' %s' %self.year
		if self.name is not None:
			s += ' %s' %self.name
		return s



class Null(_Dataset):
	'''
	A null 1D datum;  y(q)=0 for all q
	'''
	def __init__(self):
		self.author = 'Null'
		self.name   = None
		self.year   = None
		self.t      = np.linspace(0, 1, 101)
		self.y      = np.zeros(101)
		self.dt     = 0.01
		self.hz     = 1 / self.dt



class Vaughan1982(_Dataset):
	'''
	Data available in Vaughan (1982, p.379, Table 1,)
	
	Vaughan CL (1982). Smoothing and differentiation of displacement-time data: an application of splines and digital filtering. International Journal of Bio-Medical Computing 13, 375–386.

	'''
	def __init__(self):
		self.author = 'Vaughan'
		self.name   = None
		self.year   = 1982
		self.y      = np.array([1.770,1.757,1.748,1.740,1.726, 1.715,1.698,1.683,1.667,1.651,1.632,1.612,1.593,1.572,1.551,1.530,1.507,1.483,1.445,1.428,1.401,1.371,1.343,1.311,1.279,1.245,1.212,1.175,1.143,1.105,1.063,1.029,0.991,0.953,0.910,0.869,0.823,0.779,0.732,0.691,0.644,0.595,0.548,0.501,0.447,0.395,0.350,0.294,0.243,0.185])
		self.dt     = 0.00985
		self.hz     = 1 / self.dt
		self.t      = self.dt * np.arange( self.y.size )



class _Challis1999(_Dataset):
	CONST_W0  = 2 * pi
	CONST_A   = np.array([16, 12, 6.3, 0.5, 1.2, 0.6, 0.3, 0.2, 0.1, 0.09, 0.04, 0.06, 0.01])
	CONST_PHI = np.array([0.99, 0.23, -2.97, 0.0, -3.13, -0.84, 2.14, 0.58, 1.15, 0.17, -1.13, 0.76, -1.21])
	author    = 'Challis'
	year      = 1999
	
	def __init__(self):
		self.dt     = self.t[1] - self.t[0]
		self.hz     = 1 / self.dt

	def get_namep(self):
		return '%s %s, Dataset %s' %(self.author, self.year, self.name)


class Challis1999A(_Challis1999):
	'''
	Dataset A from:
	Challis JH (1999). A procedure for the automatic determination of filter cutoff frequency for the processing of biomechanical data. Journal of Applied Biomechanics 15, 303-317.
	'''
	def __init__(self):
		w0,a,phi    = self.CONST_W0, self.CONST_A, self.CONST_PHI
		self.name   = 'A'
		self.t      = np.linspace(0, 1, 91)
		self.y      = np.array([(a * np.sin( np.arange(1,14) * w0 * tt + phi)).sum() for tt in self.t])
		super().__init__()
	

class Challis1999B(_Challis1999):
	'''
	Dataset B from:
	Challis JH (1999). A procedure for the automatic determination of filter cutoff frequency for the processing of biomechanical data. Journal of Applied Biomechanics 15, 303-317.
	'''
	def __init__(self):
		self.name   = 'B'
		self.t      = np.linspace(0, 1, 91)
		self.y      = self._get_y()
		super().__init__()

	def _get_y(self):
		w0,a,phi    = self.CONST_W0, self.CONST_A, self.CONST_PHI
		t           = self.t
		n,k,dt      = t.size, 40.0, t[1] - t[0]
		p           = (dt * (n-1)) - (0.5*dt)
		f           = []
		for tt in t:
			ff      = k * (tt- 0.5*p)**2
			for i,(aa,pphi) in enumerate( zip(a,phi) ):
				ff += (aa) * sin( (i+1) * w0 * tt + pphi)
			f.append(ff)
		return np.array(f)
		


class Challis1999C(_Challis1999):
	'''
	Dataset C from:
	Challis JH (1999). A procedure for the automatic determination of filter cutoff frequency for the processing of biomechanical data. Journal of Applied Biomechanics 15, 303-317.
	'''
	def __init__(self):
		self.name   = 'C'
		self.t      = np.linspace(0, 1, 91)
		self.y      = self._get_y()
		super().__init__()

	def _get_y(self):
		t           = self.t
		f           = np.zeros(t.size)
		i0          = t <= 0.85
		i1          = t > 0.85
		f[i0]       = (-55.1 * t[i0]) + (427 * t[i0]**3) + (-342 * t[i0]**4)
		f[i1]       = 579.97 - (304.32 * t[i1]) + (-241.77 * t[i1]**-1)
		return np.array(f)
	


class Challis1999D(_Challis1999):
	'''
	Dataset D from:
	Challis JH (1999). A procedure for the automatic determination of filter cutoff frequency for the processing of biomechanical data. Journal of Applied Biomechanics 15, 303-317.
	'''
	def __init__(self):
		self.name   = 'D'
		self.t      = np.linspace(0, 5, 200)
		self.y      = self._get_y()
		super().__init__()

	def _get_y(self):
		t     = self.t
		f     = np.zeros(t.size)
		i0    = t <= 4.
		i1    = t > 4.0
		f[i0] = pi**-2 * np.sin( pi * t[i0] )
		f[i1] = pi**-1 * ( t[i1] - 4 )
		return f
	


class Challis1999E(_Challis1999):
	'''
	Dataset E from:
	Challis JH (1999). A procedure for the automatic determination of filter cutoff frequency for the processing of biomechanical data. Journal of Applied Biomechanics 15, 303-317.
	'''
	def __init__(self):
		self.name   = 'E'
		self.t      = np.linspace(0, 1, 128)
		self.y      = self._get_y()
		super().__init__()

	def _get_y(self):
		t     = self.t
		B     = 10000
		f     = B * t**2 * (t-0.1) * (t-0.2) * (t-0.5) * (t-0.75) * (t-0.95) * (t-1)**2 + t**2
		return f
	


dataset_classes = [Null, Vaughan1982, Challis1999A, Challis1999B, Challis1999C, Challis1999D, Challis1999E]




def load(datasetname):
	assert isinstance(datasetname, str) and (datasetname in dataset_names), 'datasetname must be one of %s' %dataset_names
	if datasetname=='Null':
		dataset = Null()
	if datasetname=='Challis1999a':
		dataset = Challis1999A()
	elif datasetname=='Challis1999b':
		dataset = Challis1999B()
	elif datasetname=='Challis1999c':
		dataset = Challis1999C()
	elif datasetname=='Challis1999d':
		dataset = Challis1999D()
	elif datasetname=='Challis1999e':
		dataset = Challis1999E()
	elif datasetname=='Vaughan1982':
		dataset = Vaughan1982()
	else:
		raise( ValueError('Unknown dataset name: %s' %datasetname) )
	t,y = dataset.get_data()
	return t,y



