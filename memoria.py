class Memoria:

	mem = ['00']*65536

	""" Metodo para obtener el contenido de una localidad de memoria
	dada en HEXADECIMAL """
	@staticmethod
	def obtenerContenido(localidad):
		localidad = int(localidad, 16)
		contenido = Memoria.mem[localidad]
		return contenido

	""" Metodo para cambiar el contenido de las localidades de memoria"""
	@staticmethod
	def cambiarContenido(contenido, localidad):
		localidad = int(localidad, 16)
		Memoria.mem[localidad] = contenido
		return

	@staticmethod
	def limpiarMemoria(inicio, fin):
		for i in range(inicio, fin):
			Memoria.mem[i] = '--'
		return
