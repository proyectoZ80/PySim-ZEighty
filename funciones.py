def tohex(num, nbits):
	return hex((num + (1 << nbits)) % (1 << nbits))[2:].upper().zfill(int(nbits/4))

# Funcion que convierte un numero decimal a binario
def tobin(num, nbits):
	return bin((num + (1 << nbits)) % (1 << nbits))[2:].zfill(nbits).zfill(nbits)

# Convierte un numero de 8 bits hexadecimal a decimal (de -128 a 127)
def hextodec(num):
	return int(num, 16) - ((int(num, 16) >> 7) *256)
	
# Funcion que obtiene el valor de checksum de la linea a desensamblar
def compDos(N):
  n = len(bin(N)[2:])
  c = hex((2 ** n) - N)[2:].zfill(2)
  return c[len(c)-2:].upper()