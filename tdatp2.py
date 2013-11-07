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

	def verObj(self,pos):
		return self.objective[pos]

	def verSigObj(self,pos):
		try:
			return self.objective[pos+1]
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

	def terminar(self):
		t = Terminar()
		self.cost += Cost().costo('terminar')
		return [t]

	def intercambiar(self):
		x = self.verBase()
		y = self.verSigBase()
		i = Intercambiar(x,y)
		self.cost += Cost().costo('intercambiar')
		self.posbase += 2
		return [i]

	def reemplazar(self,pos):
		r = Reemplazar(self.verBase(),self.verObj(pos))
		self.cost += Cost().costo('reemplazar')
		self.posbase += 1
		return [r]

	def checkintercambio(self,pos):
		"""Evalua si es viable un intercambio"""
		if pos < len(self.objective):
			"""Evaluo caso de intercambio"""
			b1 = self.verBase()
			b2= self.verSigBase()
			o1 = self.objective[pos]
			o2 = self.verSigObj(pos)
			if (not b2 is None and not o2 is None) and (b1 == o2) and (b2 == o1):
				print "Hay que intercambiar" 
				return True
		return False

	def distcopy(self,pos):
		"""Mide la distancia al proximo elemento que se pueda copiar"""
		dist = 0
		aux = self.posbase #Guardo la posicion original
		while not self.eob():
			print "analizando"
			if self.verBase()==self.verObj(pos):
				dist = self.posbase - aux
			self.posbase += 1
		self.posbase = aux #Vuelvo a colocarlo en su posicion original
		return dist

	def distinter(self,pos):
		"""Mide la distancia al proximo intercambio(de ser posible)"""
		dist = 0
		aux = self.posbase
		while not self.eob():
			if self.checkintercambio(pos):
				dist = self.posbase - aux
			self.posbase +=1
		self.posbase = aux
		return dist

	def min(self,l):
		minimo = None
		for i in l:
			if (minimo is None) or (i[0]*Cost().costo(i[1]) < Cost().costo(minimo)):
				minimo = i[1]
		print "El minimo es %s" % minimo 
		return minimo

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
			aux = self.checkintercambio(pos)
			"""Evaluo si en vez de copiar se puede intercambiar y si es mas optimo"""
			if not aux or (aux and self.min([(1,'copiar'),(1,'intercambiar')])=='copiar'):
				"""Evaluo si en vez de copiar se puede reemplazar"""
				if (self.min([(1,'copiar'),(1,'reemplazar')])=='copiar'):
					return self.copiar()
				else:
					"""No tiene sentido que reemplazar sea mas eficiente, igual se implementa"""
					return self.reemplazar(pos)

		if pos < len(self.objective):
			"""Evaluo caso de intercambio"""
			if self.checkintercambio(pos):
				r = self.intercambiar()
				self.mem[pos+1]=self.mem[pos-1]+r
				return r

		"""En este punto tengo que evaluar borrar, insertar o reemplazar"""
		print "LA DISTANCIA AL PROXIMO INTERCAMBIO ES %s" % self.distinter(pos)
		return ['false']

	def solution(self,pos):
		"""Como premisa supongo que ya poseo como conseguir una solucion anterior
		"""
		if pos == 0:
			return self.solve(pos)

		if not self.mem.has_key(pos-1):
			self.mem[pos-1] = self.solution(pos-1)
		if not self.mem.has_key(pos):
			print "Veo si hay solucion para %s con pos %s" % (self.objective[pos],pos)
			self.mem[pos] = self.mem[pos-1] + self.solve(pos)
		if pos == len(self.objective)-1 and not self.eob():
			"""Ya obtuvimos la solucion y aun hay elementos en la base que deben ser
			descartados"""
			self.mem[pos] += self.terminar()
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
	s = p.solution(len(pal2)-1)
	for i in s:
		print i
	print "El costo es: %s" % str(p.cost)
if __name__ == '__main__':
	main()