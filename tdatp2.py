#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

class Cost(object):
	_instance = None
	_init = False

	def __new__(cls,*args, **kwargs):
		if not cls._instance:
			cls._instance = super(Cost, cls).__new__(cls)
		return cls._instance

	def __init__(self, file_source = None):
		if self._init :	return  #Avoids __init__ being called on every access.
		self.dict = {}
		if file_source is not None:
			self.load_file(file_source)
		self._init = True

	def load_file(self, file_source):
		print "el archivo se llama %s \n" % file_source
		_file = open(file_source)
		for line in _file:
			line = line.replace('\n','').split(':')
			self.dict[line[0]]=int(line[1])

	def costo(self,op):
		return self.dict[op]

def checkArguments():
	return True





def main():
	print "Teoria y Algoritmos 1 - [75.29]"
	print "TP2 - Distancia de Edicion"
	print "Autores: Alejandro Pernin (92216) y Lautaro Medrano (90009)\n"
	s1 = Cost(file_source=sys.argv[1])
	print s1.dict
	print "El costo de intercambiar es %s " % s1.costo('intercambiar')


if __name__ == '__main__':
	main()