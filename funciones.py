<<<<<<< HEAD
# Funcion que convierte un numero decimal a hexadecimal
=======
>>>>>>> Angel
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
<<<<<<< HEAD
  return c[len(c)-2:].upper()

# Funcion para llenar el diccionario con las instrucciones de la tabla
def llenaDiccionario():
	file = open('tablaCompleta.txt','r')
	table = {}
	for line in file.readlines():
		line = line.replace('\n','').split('|')
		table[line[1]] = line[0].split(':')
	return table

# Funcion para cargar el contenido del archivo en la memoria
def cargaMemoria(mem, dirCarga):
	code = open('archivo.txt', 'r')
	for line in code.readlines():
		line = line.replace(':','')
		# El desensamble termina al encontrar la ultima linea del codigo objeto
		if line != '00000001FF':
			start = line[2:6]
			line = list(map(''.join, zip(*[iter(line)]*2)))
			
			# Vemos que el checksum coincida con el resultado del codigo objeto
			checksum = line[len(line)-1]
			line = line[:len(line)-1]
			sum = compDos(eval('+'.join([str(int(num,16)) for num in line])))
			
			line = line[4:]
			
			if sum == checksum:
				i = int(dirCarga,16) + int(start,16)
				while(len(line)>0):
					mem[i] = line[0]
					line = line[1:]
					i += 1
			else: 
				print ('Codigo violado') 
				return
	return mem

def desensamblado(mem, dirEjec, table):
	j = int(dirEjec,16)
	act = ''
	while(act != '--'):
		act += mem[j]
		j += 1
		if act == 'DDCB' or act == 'FDCB':
			des = line[j]
			act += 'V'+line[j+1]
			j += 2
			inst = table.get(act)[0]
			inst = inst.replace('V',des+'H')
			act = ''
			print (hex(j-4)[2:].zfill(4).upper(), inst)
		elif act in table:
			inst = table.get(act)[0]
			long = int(table.get(act)[1])
			longact = len(act)/2
			# Bandera para saber cuando poner la H en los numeros al desensamblar
			flagh = 0
			while(long != longact) :
				act = mem[j]
				longact += 1
				j += 1
				if inst.find('WW') != -1:
					inst = (act+'H').join(inst.rsplit('W',1))
					flagh = 1
				elif inst.find('V') != -1:
					inst = inst.replace('V', act+'H')
				elif inst.find('W') != -1:
					if flagh == 1: inst = inst.replace('W', act)
					else: inst = inst.replace('W', act+'H')
			print (hex(j-long)[2:].zfill(4).upper(), inst)
			act = ''
=======
  return c[len(c)-2:].upper()
>>>>>>> Angel
