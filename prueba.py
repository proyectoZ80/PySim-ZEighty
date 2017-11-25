from Z80 import Z80
import funciones

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
	code = open('P1.txt', 'r')
	for line in code.readlines():
		line = line.replace(':','').replace("\n", "")
		# El desensamble termina al encontrar la ultima linea del codigo objeto
		if (line != '00000001FF'):
			start = line[2:6]
			line = list(map(''.join, zip(*[iter(line)]*2)))
			
			# Vemos que el checksum coincida con el resultado del codigo objeto
			checksum = line[len(line)-1]
			line = line[:len(line)-1]
			sum = funciones.compDos(eval('+'.join([str(int(num,16)) for num in line])))
			
			line = line[4:]
			
			if (sum == checksum):
				i = int(dirCarga,16) + int(start,16)
				while(len(line)>0):
					mem.cambiarContenido(line[0], funciones.tohex(i,8))
					line = line[1:]
					i += 1
			else: 
				print ('Codigo violado', checksum, sum) 
				return
		else:
			return mem

def desensamblado(mem, dirEjec, dirFinal, table):
	dict = {}
	j = int(dirEjec,16)
	dirFinal= int(dirFinal,16)
	act = ''
	while(act != '76'):
		if j != dirFinal+1:
			act += mem.obtenerContenido(funciones.tohex(j,8))
			j += 1
			if act == 'DDCB' or act == 'FDCB':
				des = line[j]
				act += 'V'+line[j+1]
				j += 2
				inst = table.get(act)[0]
				inst = inst.replace('V', des+'H')
				long = int(table.get(act)[1])
				dict[hex(j-4)[2:].zfill(4).upper()] = [act, inst, hex(j-4+long)[2:].zfill(4).upper()]
				act = ''
			elif act in table:
				temp = act
				inst = table.get(act)[0]
				long = int(table.get(act)[1])
				longact = len(act)/2
				# Bandera para saber cuando poner la H en los numeros al desensamblar
				flagh = 0
				while(long != longact) :
					act = mem.obtenerContenido(funciones.tohex(j,8))
					temp += act
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
				dict[hex(j-long)[2:].zfill(4).upper()] = [temp, inst, hex(j)[2:].zfill(4).upper()]
				act = ''
				tem = ''
		else:
			return dict
			break

def ejecutar(procesador, dirEjec):
	procesador.PC = dirEjec
	act = dict[procesador.PC]
	inst = act[1].split(" ")
	print("INICIO")
	print(procesador.PC)
	print(inst)
	print(procesador.A)
	if inst[0] != "HALT":
		procesador.PC = act[2]
		if (len(inst) == 1):
			procesador.callMethod(procesador, inst[0], "")
			print("FIN"+" "+procesador.PC)
		else:
			procesador.callMethod(procesador, inst[0], inst[1])
			print("FIN"+" "+procesador.PC)
		ejecutar(procesador, procesador.PC)
	return
	
tabla = llenaDiccionario()
cargaMemoria(Z80.mem, "0000")
Z80.PC = "0000"
dict = desensamblado(Z80.mem, "0000", "0024",tabla)
print(dict)
ejecutar(Z80, "0000")