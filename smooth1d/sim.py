'''
sim.py

Classes for facilitiating simulation

This module is undocumented.  Its use can be inferred from the example scripts provided in:
./smooth1d/scripts/sim/

A procedural equivalent to one realization of this module is also available in the
scripts directory mentioned above.
'''


import os
import numpy as np
import spm1d

from . import datasets
from . import smooth
from . import util





class SimulationResults(object):
	def __init__(self):
		self.n               = 0     #number of records
		self.labels          = ['h0reject', 'tstar', 'tmax', 'dmax', 'rmse']  #main data labels
		self.dmax            = []    #maximum difference (originnal units)
		self.h0reject        = []    #significant difference detected?
		self.rmse            = []    #root-mean square error
		self.tmax            = []    #maximum absolute t value
		self.tstar           = []    #critical (two-tailed) threshold
		self.metadata        = []    #record labels
		self.metadata_labels = None  #metadata variable labels
		self.metadata_types  = None  #metadata variable types
		
	
	def append(self, rmse, h0reject, tstar, tmax, dmax):
		self.dmax.append(dmax)
		self.h0reject.append(h0reject)
		self.rmse.append(rmse)
		self.tmax.append(tmax)
		self.tstar.append(tstar)
		self.n += 1
	
	def append_metadata(self, metadata):
		self.metadata.append( metadata ) 
	
	def get_metadata(self):
		arrays = [np.asarray(x, dtype=typ)   for x,typ in zip(np.asarray(self.metadata).T,self.metadata_types)]
		return dict( zip(self.metadata_labels, arrays ) )
	
	def get_metrics(self):
		data   = [self.h0reject, self.tstar, self.tmax, self.dmax, self.rmse]
		return dict( zip(self.labels, data) )
	
	def save(self, filename):
		results_dict  = self.get_metrics()
		metadata_dict = self.get_metadata()
		np.savez_compressed(filename, **results_dict, **metadata_dict)
	
	def set_metadata_labels(self, labels, types=None):
		assert isinstance(labels, (tuple,list)), 'Metadata labels must be a tuple or list of strings'
		for s in labels:
			assert isinstance(s, str), 'Each metadata label must be a string'
		for typ in types:
			assert (typ is int) or (typ is float), 'Each metadata type must be int or float'
		self.metadata_labels = list(labels)
		self.metadata_types  = types




class Simulator(object):
	def __init__(self):
		self.dataset_names   = 'Twisk1994', 'Challis1999a', 'Challis1999b', 'Challis1999c', 'Challis1999d', 'Challis1999e'
		self.filter_names    = 'None', 'Butterworth', 'Autocorr', 'GCVSPL', 'SSA'
		self.J               = None   #sample size (number of continuum observations)
		self.Q               = None   #number of continuum nodes
		self.alpha           = 0.05   #Type I error rate
		self.dataset_name    = None   #dataset name
		self.dt              = None   #duration between samples
		self.filterfn        = None   #filtering function
		self.filter_name     = None   #dataset name
		self.filter_params   = None   #filter parameter dictionary
		self.noise_amp       = None   #noise amplitude (in RMSE units)
		self.noise_sd        = None   #noise amplitude (in SD units)
		self.results_dir     = None   #directory to which results will be saved
		self.t               = None   #time continuum
		self.y0              = None   #dependent variable continuum
		self.y               = None   #noisy sample (J x Q array)
		self.ys              = None   #filtered sample (J x Q array)
		self.results         = SimulationResults()


		
	def filter(self):
		self.ys        = np.array([self.filterfn(yy) for yy in self.y])
	
	def generate_noisy_sample(self):
		self.y         = self.y0 + self.noise_sd * np.random.randn(self.J, self.Q)

	def get_dataset(self):
		return self.t, self.y0
	def get_dataset_index(self):
		return self.dataset_names.index(self.dataset_name)
	def get_filter_index(self):
		return self.filter_names.index(self.filter_name)
	def get_filtered_sample(self):
		return self.t, self.ys
	def get_noisy_sample(self):
		return self.t, self.y
	def get_metadata(self):
		return self.results.get_metadata()
	def get_results(self):
		return self.results
	def get_results_filename(self):
		ind_filter  = self.get_filter_index()
		ind_dataset = self.get_dataset_index()
		fname       = 'dataset%d' %ind_dataset
		fname      += '_filter%d' %ind_filter
		if self.filter_params is not None:
			for key,value in self.filter_params.items():
				fname  += '_%s%d' %(key,value)
		fname      += '.npz'
		fname       = os.path.join(self.results_dir, fname)
		return fname
	
	def save(self):
		results     = self.get_results()
		fnameNPZ    = self.get_results_filename()
		results.save(fnameNPZ)
	
	def set_alpha(self, alpha):
		assert (isinstance(alpha, float) and (alpha>0) and (alpha<1)), 'alpha must be a float between 0 and 1'
		self.alpha     = alpha

	def set_dataset_name(self, name):
		assert (name in self.dataset_names), 'The specified dataset name ("%s") must be one of: %s' %(name, self.dataset_names)
		self.dataset_name = name
		t,y0              = datasets.load( name )
		self.Q            = y0.size
		self.dt           = t[1] - t[0]
		self.t            = t
		self.y0           = y0

	def set_filter(self, name, params=None):
		assert (name in self.filter_names), 'The specified filter name ("%s") must be one of: %s' %(name, self.filter_names)
		self.filter_name      = name
		self.filter_params    = params
		if name is 'None':
			self.filterfn     = lambda x: x
		elif name is 'Butterworth':
			assert isinstance(params,dict) and (list(params.keys()) == ['cutoff', 'order']), 'params must be a dictionary containing "cutoff" and "order" keys'
			cutoff            = params['cutoff']
			order             = params['order']
			assert isinstance(cutoff, (int,float)) and (cutoff>0), 'params["cutoff"] must be an integer or float greater than zero'
			assert isinstance(order, int) and (order>0), 'params["order"] must be an integer greater than zero'
			self.filterfn     = lambda x: smooth.butter_lowpass(x, self.dt, cutoff, order=order)
		elif name is 'Autocorr':
			assert isinstance(params,dict) and (list(params.keys()) == ['order']), 'params must be a dictionary containing an "order" key'
			order             = params['order']
			assert isinstance(order, int) and (order>0), 'params["order"] must be an integer greater than zero'
			self.filterfn     = lambda x: smooth.autocorr(x, order=order, time=self.t)
		elif name is 'GCVSPL':
			assert isinstance(params,dict) and (list(params.keys()) == ['order']), 'params must be a dictionary containing an "order" key'
			order             = params['order']
			assert isinstance(order, int) and (order>0), 'params["order"] must be an integer greater than zero'
			self.filterfn     = lambda x: smooth.gcvspl(self.t, x, order=order)
		elif name is 'SSA':
			assert isinstance(params,dict) and (list(params.keys()) == ['window','ncomponents']), 'params must be a dictionary containing an "order" key'
			window            = params['window']
			ncomponents       = params['ncomponents']
			assert isinstance(window, int) and (window>0), 'params["window"] must be an integer greater than zero'
			assert isinstance(ncomponents, int) and (ncomponents>0), 'params["ncomponents"] must be an integer greater than zero'
			self.filterfn     = lambda x: smooth.ssa(x, window, ncomponents)
	
	def set_metadata_labels(self, labels, types=None):
		self.results.set_metadata_labels(labels, types=types)

	def set_seed(self):
		ind_filter  = self.get_filter_index()
		ind_dataset = self.get_dataset_index()
		np.random.seed(ind_filter+ind_dataset)
	
	def set_results_directory(self, dir0):
		assert os.path.isdir(dir0), "Results directory must be an existing directory"
		self.results_dir = dir0
	
	def set_noise_amp(self, amp):
		assert isinstance(amp, (float,int)), 'Noise ampltiude must be a float or an integer'
		self.noise_amp = amp
		self.noise_sd  = util.noise_for_target_rmse(self.y0, amp)
		
		
	def set_sample_size(self, J):
		assert (isinstance(J, int) and (J>0)), 'Sample size must be an integer' %(amp)
		self.J         = J

	def simulate(self, n_iterations, metadata=None):
		assert (isinstance(n_iterations, int) and (n_iterations>0)), 'n_iterations must be an integer greater than zero'
		for i in range(n_iterations):
			self.generate_noisy_sample()
			self.filter()
			t,y           = self.get_filtered_sample()
			rmse          = util.prmse(self.y0, y).mean()
			spmi          = spm1d.stats.ttest(y-self.y0).inference(alpha=self.alpha, two_tailed=True)
			h0reject      = spmi.h0reject
			tmax          = np.abs( spmi.z ).max()
			tstar         = spmi.zstar
			ind           = np.abs( spmi.z ).argmax()
			dmax          = y[:,ind].mean() - self.y0[ind]
			self.results.append( rmse, h0reject, tstar, tmax, dmax )
			if metadata is not None:
				self.results.append_metadata(metadata)



