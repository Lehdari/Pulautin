import os
import inspect


class Flags:
	def __init__(self):
		self.cfgList = {}
		self.macroList = {}
		self.force = False
		self.macroFileExtensions = []
		self.dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/'