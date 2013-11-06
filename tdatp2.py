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

class Copiar():
	def __init__(self,char):
		self.char = char

	def __str__(self):
		s = "copiar %s" % self.char
		return s

class Reemplazar():
	def __init__(self,char1,char2):
		self.char1=char1
		self.char2=char2

	def __str__(self):
		s = "reemplazar %s %s" %(self.char1,self.char2)
		return s

class Borrar():
	def __init__(self,char):
		self.char=char

	def __str__(self):
		s = "borrar %s" % self.char
		return s

class Insertar():
	def __init__(self,char):
		self.char=char

	def __str__(self):
		s = "insertar %s" % self.char
		return s

class Intercambiar():
	def __init__(self,char1,char2):
		self.char1=char1
		self.char2=char2

	def __str__(self):
		s = "intercambiar %s %s" % (self.char1 , self.char2)
		
		return s

class Terminar():
	def __str__(self):
		return "terminar"

class Problem():

	def __init__(self,pal1,pal2):
		self.base = pal1
		self.posbase = 0
		self.objective = pal2
		self.res=[]
		self.mem={}
		self.cost=0

	def eob(self):
		return self.posbase == len(self.base)

	def verBase(self):
		return self.base[self.posbase]

	def verSigBase(self):
		try:
			return self.base[self.posbase+1]
		except IndexError:
			return None

	def copiar(self):
		c = Copiar(self.verBase())
		self.posbase += 1
		self.cost += Cost().costo('copiar')
		return [c]

	def insertar(self,pos):
		char = self.objective[pos]
		i = Insertar(char)
		self.cost += Cost().costo('insertar')
		return [i]

	def intercambiar(self,pos):

	def solve(self,pos):
		"""Determina cual es la mejor manera de obtener el caracter actual
		con la palabra base
		"""
		print "Se intenta solucionar para %s" % self.objective[pos]
		r = []
		if self.eob():
			"""No hay otra opcion más que insertar, ya que se agotaron
			los caracteres disponibles en la base"""
			return self.insertar(pos)

		if self.verBase() == self.objective[pos]:
			"""Es el caso de copiar"""
			print "es el caso de copiar"
			return self.copiar()

		if pos < len(self.objective):
			x = self.verBase()
			y = self.verSigBase()
			if (not y is None) and (x == self.objective[pos+1]) and (y == self.objective[pos]):
				print "Hay que intercambiar" 


	def solution(self,pos):
		"""Como premisa supongo que ya poseo como conseguir una solucion anterior
		"""
		if pos == 0:
			return self.solve(pos)

		if not self.mem.has_key(pos-1):
			self.mem[pos-1] = self.solution(pos-1)
		if not self.mem.has_key(pos):
			self.mem[pos] = self.mem[pos-1] + self.solve(pos)
		return self.mem[pos]

def checkArguments():
	return True





def main():
	print "Teoria y Algoritmos 1 - [75.29]"
	print "TP2 - Distancia de Edicion"
	print "Autores: Alejandro Pernin (92216) y Lautaro Medrano (90009)\n"
	s1 = Cost(file_source=sys.argv[3])
	pal = sys.argv[1]
	pal2 = sys.argv[2]
	copy = Copiar('h')
	print copy
	p = Problem(pal,pal2)
	s = p.solution(3)
	for i in s:
		print i
	print "El costo es: %s" % str(p.cost)
if __name__ == '__main__':
	main()