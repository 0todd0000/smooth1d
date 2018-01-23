
'''
This module contains a "MyFigure" class for simplifying multi-panel plotting.
'''


import numpy as np
from matplotlib import pyplot



class MyFigure(object):
	def __init__(self, figsize=None, axx=None, axy=None, axw=None, axh=None, fontname=u'Times New Roman', set_font=True, set_visible=False):
		'''
		INPUTS
		
		figsize : integer 2-tuple, same as "figsize" parameter for pyplot.figure
		axx : list, relative x positions of axes
		axy : list, relative y positions of axes
		axw : float, relative width of all panels
		axh : float, relative height of all panels
		fontname : str, default font to use for plotting
		set_font : boolean, use "fontname" when initializing figure
		set_visible : boolean, show redundant x and y tick labels (i.e. show tick labels on inner panels)
		'''
		self.AX       = None
		self.axx      = axx
		self.axy      = axy
		self.axw      = axw
		self.axh      = axh
		self.figsize  = figsize
		self.fontname = u'%s' %fontname
		self.nRows    = len(axy)
		self.nCols    = len(axx)
		self._create()
		self._set_default(set_font, set_visible)
	def _create(self):
		pyplot.figure(figsize=self.figsize)
		self.AX       = np.array([[pyplot.axes([xx,yy,self.axw,self.axh])   for xx in self.axx] for yy in self.axy])
	def _set_default(self, set_font, set_visible):
		if set_font:
			self.set_ticklabel_props(name=self.fontname, size=8)
		if set_visible:
			self.set_xticklabels_off()
			self.set_yticklabels_off()
	def get_axes(self):
		return self.AX.flatten().tolist()

	def set_panel_labels(self, labels=[], pos=(0.05,0.92), size=10, add_letters=True, with_box=True):
		tx      = []
		for i,(ax,label) in enumerate( zip(self.get_axes(), labels) ):
			s   = '(%s)  %s' %(chr(97+i),label) if add_letters else label
			tx.append(  ax.text(pos[0], pos[1], s, transform=ax.transAxes)  )
		pyplot.setp(tx, size=size, name=self.fontname)
		if with_box:
			pyplot.setp(tx, bbox=dict(facecolor='w'))
		return tx

	def set_xticklabels_off(self):
		pyplot.setp(self.AX[:-1], xticklabels=[])
	def set_yticklabels_off(self):
		pyplot.setp(self.AX[:,1:], yticklabels=[])
	def set_ticklabel_props(self, name=None, size=9):
		if name==None:
			name = self.fontname
		[pyplot.setp(ax.get_xticklabels()+ax.get_yticklabels(), name=u'%s'%name, size=size)  for ax in self.get_axes()]
	def set_xlabels(self, labels, size=20):
		if isinstance(labels, str):
			labels = [labels]*self.nCols
		for ax,label in zip(self.AX[-1], labels):
			ax.set_xlabel(label, name=self.fontname, size=size)
	def set_ylabels(self, labels, size=20):
		if isinstance(labels, str):
			labels = [labels]*self.nRows
		for ax,label in zip(self.AX[:,0], labels):
			ax.set_ylabel(label, name=self.fontname, size=size)



def dummy_legend(ax, colors=None, labels=None, linestyles=None, markerfacecolors=None, linewidths=None, **kwdargs):
	'''
	Creates a legend independent of what is actually contained in the axes
	'''
	n      = len(colors)
	if linestyles is None:
		linestyles = ['-']*n
	if linewidths is None:
		linewidths = [1]*n
	if markerfacecolors is None:
		markerfacecolors = colors
	x0,x1  = ax.get_xlim()
	y0,y1  = ax.get_ylim()
	h      = [ax.plot([x1+1,x1+2,x1+3], [y1+1,y1+2,y1+3], ls, color=color, linewidth=lw, markerfacecolor=mfc)[0]   for color,ls,lw,mfc in zip(colors,linestyles,linewidths,markerfacecolors)]
	ax.set_xlim(x0, x1)
	ax.set_ylim(y0, y1)
	return ax.legend(h, labels, **kwdargs)
	

