#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import LCS

class Cost(object):
	"""Se utiliza el patron singleton que fue modificado
	para que no se llame a init en cada llamado a la instancia"""

	_instance = None
	_init = False

	"""O(1)"""
	def __new__(cls,*args, **kwargs):
		if not cls._instance:
			cls._instance = super(Cost, cls).__new__(cls)
		return cls._instance

	"""O(1)"""
	def __init__(self, file_source = None):
		if self._init :	return  #Avoids __init__ being called on every access.
		self.dict = {}
		if file_source is not None:
			self.load_file(file_source)
		self._init = True

	"""O(#Operaciones) en este caso O(6)"""
	def load_file(self, file_source):
		#print "el archivo se llama %s \n" % file_source
		_file = open(file_source)
		for line in _file:
			line = line.replace('\n','').split(':')
			self.dict[line[0]]=int(line[1])

	"""O(1)"""
	def costo(self,op):
		return self.dict[op]

	def existe(self,op):
		return self.dict.has_key(op)

"""TODAS LAS OPERACIONES SON O(1)"""
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
	"""O(1)"""
	def __init__(self,pal1,pal2):
		self.base = pal1
		self.posbase = 0
		self.objective = pal2
		self.lcs= LCS.lcs(pal1,pal2) #O(#pal1 * #pal2)
		self.poslcs = 0
		self.mem={}
		self.diff = len(pal2)-len(pal1) #O(1) 
		self.cost=0
		self.term = False if (self.diff >= 0) else True #O(1)
		self.inser = self.diff if (self.diff > 0) else 0 #O(1)
		self.borr = self.diff if (self.diff < 0) else 0 #O(1)

	"""O(1)"""
	def eob(self):
		return self.posbase == len(self.base)

	def verLcs(self):
		try:
			return self.lcs[self.poslcs]
		except IndexError:
			return None

	"""O(1)"""
	def verBase(self):
		return self.base[self.posbase]

	"""O(1)"""
	def verSigBase(self):
		try:
			return self.base[self.posbase+1]
		except IndexError:
			return None

	"""O(1)"""
	def verObj(self,pos):
		return self.objective[pos]

	"""O(1)"""
	def verSigObj(self,pos):
		try:
			return self.objective[pos+1]
		except IndexError:
			return None

	"""O(1)"""
	def copiar(self):
		c = Copiar(self.verBase())
		self.posbase += 1
		self.cost += Cost().costo('copiar')
		self.poslcs += 1
		return [c]

	"""O(1)"""
	def insertar(self,pos):
		char = self.objective[pos]
		i = Insertar(char)
		self.cost += Cost().costo('insertar')
		_terminar = Cost().existe('terminar')
		_borrar = Cost().existe('borrar')
		if self.diff >= 0:
			if not _borrar and _terminar:
				self.term = True
			elif _borrar and _terminar:
				minim = min(Cost().costo('borrar'),Cost().costo('terminar'))
				if minim == Cost().costo('terminar'):
					self.term = True
		return [i]

	"""O(1)"""
	def terminar(self):
		t = Terminar()
		self.cost += Cost().costo('terminar')
		return [t]

	"""O(1)"""
	def intercambiar(self):
		x = self.verBase()
		y = self.verSigBase()
		i = Intercambiar(x,y)
		self.cost += Cost().costo('intercambiar')
		self.posbase += 2
		return [i]

	"""O(1)"""
	def reemplazar(self,pos):
		r = Reemplazar(self.verBase(),self.verObj(pos))
		self.cost += Cost().costo('reemplazar')
		if (self.verBase()==self.verLcs()):
			self.poslcs +=1
		self.posbase += 1
		return [r]

	"""O(1)"""
	def borrar(self):
		b = Borrar(self.verBase())
		self.posbase += 1
		self.cost += Cost().costo('borrar')
		return [b]

	"""O(1)"""
	def aInsertar(self,pos):
		"""Se analiza el costo de insertar, se supone que la prox seria copia 
			sino no conviene insertar"""
		costo = Cost().costo('insertar')+Cost().costo('copiar')
		_terminar = Cost().existe('terminar')
		_borrar = Cost().existe('borrar')
		if self.diff <= 0:
			#Insertar implica que deba o borrar o terminar
			if not _borrar and _terminar:
				costo += Cost().costo('terminar') if not self.term else 0
			elif not _terminar and _borrar:
				costo += Cost().costo('borrar')
			else:
				step = min(Cost().costo('terminar'),Cost().costo('borrar'))
				if step == Cost().costo('terminar'):
					costo += step if not self.term else 0
				else:
					costo += step

		return costo

	"""O(1)"""
	def aBorrar(self,pos):
		costo = Cost().costo('borrar')+Cost().costo('copiar')
		if self.diff >= 0:
			#Borrar implica insertar
			costo += Cost().costo('insertar')
		return costo

	"""O(1)"""
	def aReemplazar(self,pos):
		costo=Cost().costo('reemplazar')

		if self.verBase()==self.verLcs():
			costo+=Cost().costo('reemplazar') if Cost().existe('terminar') else 0
		if self.verSigBase()==self.verSigObj(pos):
			costo+=Cost().costo('copiar')
		else:
			costo+=Cost().costo('reemplazar')
		return costo

	"""O(1)"""
	def checkintercambio(self,pos):
		"""Evalua si es viable un intercambio"""
		if not Cost().existe('intercambio'):
			return False
		if pos < len(self.objective):
			"""Evaluo caso de intercambio"""
			b1 = self.verBase()
			b2= self.verSigBase()
			o1 = self.objective[pos]
			o2 = self.verSigObj(pos)
			if (not b2 is None and not o2 is None) and (b1 == o2) and (b2 == o1):
				return True
		return False

	"""
	El peor caso es que me encuentre al principio del string y que no haya ningun
	elemento cuya copia sea posible por lo que debe recorrer todo el string base
	O(#base)
	"""
	def distcopy(self,pos):
		"""Mide la distancia al proximo elemento que se pueda copiar"""
		dist = 0
		aux = self.posbase #Guardo la posicion original
		while not self.eob():
			if self.verBase()==self.verObj(pos):
				dist = self.posbase - aux
			self.posbase += 1
		self.posbase = aux #Vuelvo a colocarlo en su posicion original
		return dist

	"""
	Idem anterior, el peor caso es que no haya ningun elemento cuyo intercambio
	sea posible.
	O(#base)
	"""
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

	"""
	Mide el minimo en un conjunto de operaciones
	O(#l)
	En esta implementacion podemos decir que es:
	O(2)=O(1)
	"""
	def min(self,l):
		minimo = None
		for i in l:
			if (i[0]==0):
				continue
			if (minimo is None) or (i[0]*Cost().costo(i[1]) < Cost().costo(minimo)):
				minimo = i[1]
		return minimo
	
	"""
	O(#l)
	A efectos de esta implementacion:
	O(3)=O(1)
	"""
	def min2(self,l):
		minimo = None
		costo = None
		for i in l:
			if i[0] is None:
				continue
			if (minimo is None) or (i[0] < costo):
				minimo = i[1]
				costo = i[0] 
		return minimo

	"""
	Determina cual es la mejor manera de obtener el caracter actual
	con los elementos disponibles en la palabra base
	O(1)
	"""
	def solve(self,pos,aux=None):
		r = []
		if self.eob(): #O(1)
			"""No hay otra opcion mas que insertar, ya que se agotaron
			los caracteres disponibles en la base"""
			if Cost().existe('insertar'):
				return self.insertar(pos)   #O(1)

		#O(1)
		if (self.verBase() == self.objective[pos]) \
											and Cost().existe('copiar'): 
			"""Es el caso de copiar"""
			aux = self.checkintercambio(pos) #O(1)
			"""Evaluo si en vez de copiar se puede intercambiar y si es mas optimo"""
			#O(1)
			if not aux or (aux and \
								self.min([(1,'copiar'),(1,'intercambiar')])=='copiar'):
				"""Evaluo si en vez de copiar se puede reemplazar"""
				#O(1)
				if (not Cost().existe('reemplazar'))or\
								(self.min([(1,'copiar'),(1,'reemplazar')])=='copiar'):
					return self.copiar() #O(1)
				else:
					"""No tiene sentido que reemplazar sea mas eficiente, 
					igual se implementa"""
					return self.reemplazar(pos) #O(1)
		
		#O(1)
		if pos < len(self.objective):
			"""Evaluo caso de intercambio"""
			if self.checkintercambio(pos): 
				r = self.intercambiar()   #O(1)
				"""
				Se guarda en dos posiciones de memoria dado que al intercambiar
				estamos solucionando dos posiciones del objetivo
				"""
				try: 
					self.mem[pos+1]=self.mem[pos-1]+r    #O(1)
				except KeyError:
					if (aux is not None):
						self.mem[pos+1]=aux+r      #O(1)
					else:
						pass
				return r

		if Cost().existe('copiar'):
			costoInsertar = None
			costoBorrar = None
			costoReemplazar = None
			if self.verBase() == self.verLcs(): #O(1)
				#Evaluo insertar, y la siguiente operacion seria una copia
				costoInsertar = self.aInsertar(pos) #O(1)
			if self.verSigBase() == self.verLcs() :				
				#Evaluo borrar, y la siguiente operacion seria una copia
				costoBorrar = self.aBorrar(pos)
			costoReemplazar = self.aReemplazar(pos)
			#O(1)
			op = self.min2([(costoReemplazar,'r'),(costoInsertar,'i'),(costoBorrar,'b')])
			if op == 'r':
				return self.reemplazar(pos)
			elif op == 'b':
				r += self.borrar() #O(1)
				r += self.solve(pos,r) #O(1)
				return r
			else:
				return self.insertar(pos) #O(1)

		print "No debiera llegar a este punto---"

	"""
	Se emplea programacion dinamica usando memorizacion.
	Se hacen tantas llamadas a la funcion como caracteres a obtener de alli
	O(#Objetivo)
	"""
	def solution(self,pos):
		"""Como premisa supongo que ya poseo como conseguir una solucion anterior
		"""
		if pos == 0:
			return self.solve(pos)

		if not self.mem.has_key(pos-1):
			self.mem[pos-1] = self.solution(pos-1)
		if not self.mem.has_key(pos):
			self.mem[pos] = self.mem[pos-1] + self.solve(pos)
		if pos == len(self.objective)-1 and not self.eob():
			"""Ya obtuvimos la solucion y aun hay elementos en la base que deben ser
			descartados"""
			self.mem[pos] += self.terminar()
		return self.mem[pos]

"""
Siendo #pal2 < #pal1 * #pal2
O(#pal1 * #pal2) + O(#pal2) < 2 O(#pal1 * #pal2)
O(#pal1 * #pal2)
"""
def main():
	print "Teoria y Algoritmos 1 - [75.29]"
	print "TP2 - Distancia de Edicion"
	print "Autores: Alejandro Pernin (92216) - Lautaro Medrano (90009)\n"
	s1 = Cost(file_source=sys.argv[3])
	pal = sys.argv[1]
	pal2 = sys.argv[2]
	p = Problem(pal,pal2) #O(#pal1 * #pal2)
	s = p.solution(len(pal2)-1) #O(#pal2)
	for i in enumerate(s):
		print i[0]+1,')',i[1]
	print "\nEl costo es: %s" % str(p.cost)
if __name__ == '__main__':
	main()
