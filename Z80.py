""" Contiene las operaciones ya funcionando pero sin tomar en cuenta la modificacion
    de banderas """
import memoria
import funciones

class Z80:
	#Registros
	B = "00"
	C = "00"
	D = "00"
	E = "00"
	H = "00"
	L = "00"
	A = "00"
	F = "00"
	SP = "0000"
	IX = "0000"
	IY = "0000"
	PC = "0000"
	IFF1 = "1"
	IFF2 = "1"
	I = "00"
	R = "00"
	mem = memoria.Memoria()
	
	# Metodo para mandar llamar a otro de los metodos del procesador mediante el nombre de la operacion a realizar
	# Si no hay operandos, se manda una cadena vacia
		
	@staticmethod
	def callMethod(object, name, opr):
		lista = ["JP", "JR", "CALL"]
		if (len(opr) == 0):
			getattr(object, name)()
			return
		if(name in lista):
			getattr(object, name)(opr)
			return
		opr = opr.split(",")	
		if (len(opr) == 1):
			getattr(object, name)(opr[0])
		else:
			getattr(object, name)(opr[0], opr[1])
	
	@staticmethod
	def hexToBin(numHex):
		return bin(int(numHex, 16))[2:].zfill(8)
	
	@staticmethod
	def binToHex(numBin):
		return hex(int(numBin, 2))[2:].zfill(2)
	
	# Funcion para cambiar las banderas, mandar indice del bit a cambiar y el valor nuevo
	@staticmethod
	def changeFlag(bitIndex, val):
		Z80.F = Z80.hexToBin(Z80.F)
		Z80.F = Z80.F[:7 - bitIndex] + val + Z80.F[7 - bitIndex + 1:]
		Z80.F = Z80.binToHex(Z80.F)
	
	# Funcion para obtener alguna de las banderas
	@staticmethod
	def getFlagBit(bitIndex):
		Z80.F = Z80.hexToBin(Z80.F)
		estado = int(Z80.F[7 - bitIndex])
		Z80.F = Z80.binToHex(Z80.F)
		return estado

	# Mandar en decimal el resultado para checar acarreo
	@staticmethod
	def carry(res):
		res = funciones.tobin(res,16)
		pos = res.find("1")
		res = res[pos:]
		
		if (len(res) > 8):
			Z80.changeFlag(0,'1')
		else:
			Z80.changeFlag(0,'0')

	# Mandar el resultado en decimal para checar si es cero
	@staticmethod
	def zero(res):
		if (int(res) == 0):
			Z80.changeFlag(6,'1')
		else:
			Z80.changeFlag(6,'0')
	
	# Mandar resultado en decimal para checar paridad
	@staticmethod
	def parity(res):
		res = funciones.tobin(res, 8)
		cont = res.count('1')
		if ((cont % 2) == 0):
			Z80.changeFlag(2,'1')
		else:
			Z80.changeFlag(2,'0')
		
    # Mandar el resultado en decimal para comprobar sobrepasamiento
	@staticmethod
	def overflow(res):
		if res in range(-128, 128):
			Z80.changeFlag(2, "0")
		else:
			Z80.changeFlag(2, "1")
			
	# Mandar resultado en decimal para comprobar el signo:
	@staticmethod
	def sign(res):
		if (res < 0):
			Z80.changeFlag(7, "1")
		else:
			Z80.changeFlag(7, "0")
    
	@staticmethod
	# Mandar ambos operandos en hexadecimal para comprobar medio acarreo y el signo de la operacion a realizar como cadena
	def halfCarry(op1, op2, o):
		op1 = str(int(op1[1], 16))
		op2 = str(int(op2[1], 16))
		res = eval(op1+o+op2)
		if res in range(0, 16):
			Z80.changeFlag(4, "0")
		else:
			Z80.changeFlag(4, "1")
		
	""" Metodo que se encarga de obtener el valor hexadecimal de s para las instrucciones que lo ocupan
	s puede ser n, r, (HL), (IX+d) e (IY+d)"""
	@staticmethod
	def obtenerS(op2):
		# Si se trata de un registro, se obtiene su valor
		if (len(op2) == 1):
			s = getattr(Z80, op2)
		# En caso de tratarse de la direccion apuntada por IX o IY, se obtiene su contenido
		elif (op2.find("IX+") != -1 or op2.find("IY+") != -1):
			op2 = op2.replace("(","").replace(")","").replace("H","").split("+")
			reg = getattr(Z80, op2[0])
			des = op2[1]
			s = funciones.tohex(int(reg, 16) + funciones.hextodec(des), 16)
			s = Z80.mem.obtenerContenido(s)
		# Si es la direccion que contiene HL, se obtiene su contenido
		elif (op2 == "(HL)"):
			s = Z80.mem.obtenerContenido(''.join([getattr(Z80,"H"), getattr(Z80,"L")]))
		# El ultimo caso es que sea un numero en hexadecimal
		else:
			s = op2.replace("H","")
		return s
	
	""" Metodo que se encarga de obtener el valor hexadecimal de ss para las instrucciones que lo ocupan
	ss puede ser BC, DE, HL, SP, IX e IY"""
	@staticmethod
	def obtenerSS(op2):
		if ((op2 == "SP") or (op2 == "IX") or (op2 == "IY")):
			ss = getattr(Z80, op2)
		else:
			ss = ''.join([getattr(Z80,op2[0]), getattr(Z80,op2[1])])
		return ss
		
	@staticmethod
	# Resta el contenido de A o HL con el operando 2 y con la bandera de acarreo
	def SBC(op1, op2):
		CY = getFlagBit(0)
		# Operacion de 8 bits
		if (op1 == "A"):
			s = funciones.tohex(int(Z80.obtenerS(op2),16) + int(CY,16), 8)
			Z80.halfCarry(Z80.A, s, "-")
			# Se realiza la operacion y se guarda en el acumulador
			Z80.A = int(Z80.A, 16) - int(s, 16)
			Z80.carry(Z80.A)
			Z80.zero(Z80.A)
			Z80.sign(Z80.A)
			Z80.overflow(Z80.A)
			Z80.A = funciontes.tohex(Z80.A, 8)
			Z80.changeFlag(1, "1")
		# Operacion de 16 bits
		else:
			# Se obtienen los respectivos valores
			HL = ''.join([Z80.H, Z80.L])
			ss = funciones.tohex(int(Z80.obtenerSS(op2),16)+int(CY,16), 8)
			Z80.halfCarry(HL, ss, "-")
			# Se realiza la operacion
			HL = int(HL,16) - int(ss,16)
			Z80.carry(HL)
			Z80.zero(HL)
			Z80.sign(HL)
			Z80.overflow(HL)
			HL = funciones.tohex(HL, 16)
			Z80.changeFlag(1, "1")
			# El primer byte se guarda en H y el segundo en L
			Z80.H = HL[:2]
			Z80.L = HL[2:]
		""" >>>>> N = 1, C = Z = S = H = DE ACUERDO A LA OPERACION, P/V = SOBREPASAMIENTO <<<<< """


	# Realiza operacion AND entre el acumulador (operando 1) con el operando 2
	@staticmethod
	def AND(op1, op2):
		a = getattr(Z80, op1)
		s = Z80.obtenerS(op2)
		a = list(funciones.tobin(int(a, 16), 8))
		s = list(funciones.tobin(int(s, 16), 8))
		for i in range(0, 8):
			# Si los caracteres en a y s son distintos, se cambia a 0 en el acumulador (a)
			if (a[i] != s[i]):
				a[i] = "0"
		Z80.A = int(''.join(a), 2)
		# CAMBIAR BANDERAS AQUI
		Z80.changeFlag(0, "0")
		Z80.changeFlag(1, "0")
		Z80.zero(Z80.A)
		Z80.sign(Z80.A)
		Z80.A = funciones.tohex(Z80.A, 8)
		Z80.parity(Z80.A)
		""" >>>>> C = N = 0, Z = S = H = DE ACUERDO A LA OPERACION, P/V = PARIDAD <<<<< """
	
	# Realiza operacion OR entre el acumulador (operando 1) con el operando 2
	@staticmethod
	def OR(op1, op2):
		a = getattr(Z80, op1)
		s = Z80.obtenerS(op2)
		
		a = list(funciones.tobin(int(a, 16), 8))
		s = list(funciones.tobin(int(s, 16), 8))
		for i in range(0, 8):
			# Si los caracteres en a y s son distintos, se cambia a 0 en el acumulador (a)
			if (a[i] != s[i]):
				a[i] = "1"
		Z80.A = int(''.join(a), 2)
		# CAMBIAR BANDERAS AQUI
		Z80.changeFlag(0, "0")
		Z80.changeFlag(1, "0")
		Z80.zero(Z80.A)
		Z80.sign(Z80.A)
		Z80.A = funciones.tohex(int(Z80.A, 8))
		Z80.parity(Z80.A)
		""" >>>>> C = N = 0, Z = S = H = DE ACUERDO A LA OPERACION, P/V = PARIDAD <<<<< """
	
	# Realiza operacion OR exclusivo entre el acumulador (operando 1) con el operando 2
	@staticmethod
	def XOR(op1, op2):
		a = getattr(Z80, op1)
		s = Z80.obtenerS(op2)
		
		a = list(funciones.tobin(int(a, 16), 8))
		s = list(funciones.tobin(int(s, 16), 8))
		for i in range(0, 8):
			# Si los caracteres en a y s son distintos, se cambia a 0 en el acumulador (a)
			if (a[i] != s[i]):
				a[i] = "1"
			else:
				a[i] = "0"
		Z80.A = int(''.join(a), 2)
		# CAMBIAR BANDERAS AQUI
		Z80.changeFlag(0, "0")
		Z80.changeFlag(1, "0")
		Z80.zero(Z80.A)
		Z80.sign(Z80.A)
		Z80.A = funciones.tohex(Z80.A, 8)
		Z80.parity(int(Z80.A,16))
		""" >>>>> C = N = 0, Z = S = H = DE ACUERDO A LA OPERACION, P/V = PARIDAD <<<<< """
	
	# Compara el contenido del acumulador (operando 1) con el operando 2
	@staticmethod
	def CP(op1, op2):
		a = getattr(Z80, op1)
		s = Z80.obtenerS(op2)
		Z80.halfCarry(a, s, "-")
		a = int(a, 16)
		s = int(s, 16)
		res = a - s
		Z80.zero(res)
		Z80.carry(res)
		Z80.sign(res)
		Z80.overflow(res)
		Z80.changeFlag(1, "1")
		# CAMBIAR BANDERAS CON EL RESULTADO OBTENIDO
		""" >>>>> C = Z = S = H = DE ACUERDO A LA OPERACION, N = 1, P/V = SOBREPASAMIENTO <<<<< """
	
	# Incrementa el contenido del operando dado
	@staticmethod
	def INC(op):
		# Incrementar valor de un registro
		if (len(op) == 1):
			a = Z80.obtenerS(op)
			Z80.halfCarry(a, "01", "+" )
			a = int(a, 16) + 1
			Z80.zero(a)
			Z80.sing(a)
			Z80.changeFlag(1, "0")
			Z80.overflow(a)
			setattr(Z80, op, funciones.tohex(a,8))
			""" >>>>> Z = S = H = DE ACUERDO A LA OPERACION, N = 0, P/V = SOBREPASAMIENTO <<<<< """
		
		# Incrementar valor de SP, IX o IY
		elif ((op == "SP") or (op == "IX") or (op == "IY")):
			a = funciones.tohex(int(Z80.obtenerSS(op), 16) + 1, 16)
			setattr(Z80, op, a)
			""" >>>>> No hay banderas afectadas <<<<< """
		
		# Incrementar (HL), (IX+d), (IY+d)
		elif (op.find('(')!=-1):
			a = Z80.obtenerS(op)
			Z80.halfCarry(a, "01","+")
			a = int(a, 16) + 1
			Z80.zero(a)
			Z80.sing(a)
			Z80.changeFlag(1, "0")
			Z80.overflow(a)
			a = funciones.tohex(a, 8)
			if op[1:3] == "HL":
				Z80.mem.cambiarContenido(a, ''.join([Z80.H, Z80.L]))
			else:
				Z80.mem.cambiarContenido(a, getattr(Z80, op[1:3]))
			""" >>>>> Z = S = H = DE ACUERDO A LA OPERACION, N = 0, P/V = SOBREPASAMIENTO <<<<< """
		
		# Incrementar BC, DE, HL
		else:
			a = funciones.tohex(int(Z80.obtenerSS(op), 16) + 1, 16)
			setattr(Z80, op[0], a[:2])
			setattr(Z80, op[1], a[2:])
			""" >>>>> No hay banderas afectadas <<<<< """

	# Decrementa el contenido del operando dado
	@staticmethod
	def DEC(op):
		# Decrementar valor de un registro
		if (len(op) == 1):
			a = Z80.obtenerS(op)
			Z80.halfCarry(a, "01", "-")
			a = int(a, 16) - 1
			# CAMBIAR BANDERAS AQUI
			Z80.zero(a)
			Z80.sign(a)
			Z80.changeFlag(1, "1")
			Z80.overflow(a)
			a = funciones.tohex(a, 8)
			setattr(Z80, op, a)
			""" >>>>> Z = S = H = DE ACUERDO A LA OPERACION, N = 1, P/V = SOBREPASAMIENTO <<<<< """
		
		# Decrementar valor de SP, IX o IY
		elif ((op == "SP") or (op == "IX") or (op == "IY")):
			a = funciones.tohex(int(Z80.obtenerSS(op), 16) - 1, 16)
			setattr(Z80, op, a)
			""" >>>>> No hay banderas afectadas <<<<< """
		
		# Decrementar (HL), (IX+d), (IY+d)
		elif (op.find('(')!=-1):
			a = Z80.obtenerS(op)
			Z80.halfCarry(a, "01", "-")
			a = int(a, 16) - 1
			# CAMBIAR BANDERAS AQUI
			Z80.zero(a)
			Z80.sign(a)
			Z80.changeFlag(1, "1")
			Z80.overflow(a)
			a = funciones.tohex(a, 8)
			if op[1:3] == "HL":
				Z80.mem.cambiarContenido(a, ''.join([Z80.H, Z80.L]))
			else:
				Z80.mem.cambiarContenido(a, getattr(Z80, op[1:3]))
			""" >>>>> Z = S = H = DE ACUERDO A LA OPERACION, N = 1, P/V = SOBREPASAMIENTO <<<<< """
		
		# Incrementar BC, DE, HL
		else:
			a = funciones.tohex(int(Z80.obtenerSS(op), 16) - 1, 16)
			setattr(Z80, op[0], a[:2])
			setattr(Z80, op[1], a[2:])
			""" >>>>> No hay banderas afectadas <<<<< """
	
	# Niega el contenido de A
	@staticmethod
	def CPL():
		a = list(funciones.tobin(int(Z80.A,16), 8))
		for i in range(0,8):
			if (a[i] == "1"): a[i] = "0"
			else: a[i] = "1"
		Z80.A = funciones.tohex(int(''.join(a),2), 8)
		Z80.changeFlag(1, "1") # Cambia a N
		Z80.changeFlag(4, "1") # Cambia a H
		""" >>>>> Banderas afectadas: N = 1, H = 1 <<<<< """
	
	# Hace negativo el contenido de A
	@staticmethod
	def NEG():
		Z80.halfCarry("00", Z80.A,"-")
		Z80.A = 0 - int(Z80.A, 16)
		# CAMBIAR BANDERAS AQUI
		Z80.carry(Z80.A)
		Z80.zero(Z80.A)
		Z80.sign(Z80.A)
		Z80.overflow(Z80.A)
		Z80. A = funciones.tohex(Z80.A, 8)
		""" >>>>> C = Z = S = H = SE AFECTA DE ACUERDO A LA OPERACION, P/V = SOBREPASAMIENTO, N = 1 <<<<<"""

	# Apaga los flip flops
	@staticmethod
	def DI():
		Z80.IFF1 = "0"
		Z80.IFF2 = "0"
		""" >>>>> No hay banderas afectadas <<<<< """
	
	# Enciende los flip flops
	@staticmethod
	def EI():
		Z80.IFF1 = "1"
		Z80.IFF2 = "1"
		""" >>>>> No hay banderas afectadas <<<<< """
	
	# Niega el bit de acarreo
	@staticmethod
	def CCF():
		flag = funciones.tobin(int(Z80.F, 16), 8)
		CY = flag [7]
		if (CY == "0"): CY = "1"
		else: CY = "0"
		Z80.F = int( CY + flag[1:], 2)
		# CAMBIAR BANDERAS AQUI
		Z80.carry(Z80.F)
		Z80.changeFlag(1, "0")
		Z80.F = funciones.tohex(Z80.F, 8)
		""" >>>>> C = SE AFECTA DE ACUERDO A LA OPERACION, N = 0, H = DESCONOCIDO <<<<<"""
	
	# Enciende el bit de acarreo
	@staticmethod
	def SCF():
		flag = funciones.tobin(int(Z80.F, 16), 8)
		CY = "1"
		Z80.F = funciones.tohex(int( CY + flag[1:], 2), 8)
		Z80.changeFlag(0, "1") # Cambia a C
		Z80.changeFLag(1, "0") # Cambia a N
		Z80.changeFlag(4, "0") # Cambia a H
		""" >>>>> Banderas afectadas: C = 1, N =0  y H = 0 <<<<< """
	
	@staticmethod
	def NOP():
		pass
		""" >>>>> No hay banderas afectadas <<<<< """
	
	@staticmethod
	def HALT():
		pass
		""" >>>>> No hay banderas afectadas <<<<< """
	
	@staticmethod
	def DAA():
		cy = Z80.getFlagBit(0) # Obtiene bandera de acarreo
		hc = Z80.getFlagBit(4)	# Obtiene bandera de medio acarreo
		
		if ((cy == 0) and (hc == 0)):
			if (int(Z80.A[0],16) in range(0, 10) and int(Z80.A[1],16) in range(0, 10)):
				Z80.halfCarry(Z80.A, "00", "+")
				Z80.changeFlag(0, "0")
				Z80.A = int(Z80.A, 16) + int("00", 16)
			
			elif (int(Z80.A[0],16) in range(0, 9) and int(Z80.A[1],16) in range(10, 16)):
				Z80.halfCarry(Z80.A, "06", "+")
				Z80.A = int(Z80.A, 16) + int("06", 16)
				Z80.changeFlag(0, "0")
			
			elif (int(Z80.A[0],16) in range(10, 16) and int(Z80.A[1],16) in range(0, 10)):
				Z80.halfCarry(Z80.A, "60", "+")
				Z80.A = int(Z80.A, 16) + int("60", 16)
				Z80.changeFlag(0, "1")

			elif (int(Z80.A[0],16) in range(9, 16) and int(Z80.A[1],16) in range(10, 16)):
				Z80.halfCarry(Z80.A, "66", "+")
				Z80.A = int(Z80.A, 16) + int("66", 16)
				Z80.changeFlag(0, "1")
		
		elif ((cy == 0) and (hc == 1)):
			if (int(Z80.A[0],16) in range(0, 10) and int(Z80.A[1],16) in range(0, 4)):
				Z80.halfCarry(Z80.A, "06", "+")
				Z80.A = int(Z80.A, 16) + int("06", 16)
				Z80.changeFlag(0, "0")

			elif (int(Z80.A[0],16) in range(10, 16) and int(Z80.A[1],16) in range(0, 4)):
				Z80.halfCarry(Z80.A, "66", "+")
				Z80.A = int(Z80.A, 16) + int("66", 16)
				Z80.changeFlag(0, "1")
				
			elif (int(Z80.A[0],16) in range(0, 9) and int(Z80.A[1],16) in range(6, 16)):
				Z80.halfCarry(Z80.A, "FA", "+")
				Z80.A = int(Z80.A, 16) + int("FA", 16)
				Z80.changeFlag(0, "0")
		
		elif((cy == 1) and (hc == 0)):
			if (int(Z80.A[0],16) in range(0, 3) and int(Z80.A[1],16) in range(0, 10)):
				Z80.halfCarry(Z80.A, "60", "+")
				Z80.A = int(Z80.A, 16) + int("60", 16)
				Z80.changeFlag(0, "1")

			elif (int(Z80.A[0],16) in range(0, 3) and int(Z80.A[1],16) in range(10, 16)):
				Z80.halfCarry(Z80.A, "66", "+")
				Z80.A = int(Z80.A, 16) + int("66", 16)
				Z80.changeFlag(0, "1")
			
			elif (int(Z80.A[0],16) in range(7, 16) and int(Z80.A[1],16) in range(0, 10)):
				Z80.halfCarry(Z80.A, "A0", "+")
				Z80.A = int(Z80.A, 16) + int("A0", 16)
				Z80.changeFlag(0, "1")
		
		elif((cy == 1) and (hc == 1)):
			if (int(Z80.A[0],16) in range(0, 4) and int(Z80.A[1],16) in range(0, 4)):
				Z80.halfCarry(Z80.A, "66", "+")
				Z80.A = int(Z80.A, 16) + int("66", 16)
				Z80.changeFlag(0, "1")

			elif (int(Z80.A[0],16) in range(6, 16) and int(Z80.A[1],16) in range(6, 16)):
				Z80.halfCarry(Z80.A, "9A", "+")
				Z80.A = int(Z80.A, 16) + int("9A", 16)
				Z80.changeFlag(0, "1")
		
		#CAMBIAR BANDERAS AQUI
		Z80.carry(Z80.A)
		Z80.zero(Z80.A)
		Z80.sign(Z80.A)
		Z80.A = funciones.tohex(Z80.A, 8)
		Z80.parity(int(Z80.A, 16))
		""" C = Z = S = H = CAMBIAN SEGUN EL RESULTADO, P/V = PARIDAD """
		
	#Este metodo es el encargado de hacer los brincos por medio del PC, se manda a llamar 
	#desde los metodos JP y JR.
	@staticmethod
	def hexToDecJR(cadenahexa):
		numDec = int(cadenahexa,16)
		if numDec > 127:
			numDec = numDec - 256
		nuevoPC = int(Z80.PC,16) + numDec
		Z80.PC = str(Z80.tohex(nuevoPC,16))
		return 

	# Metodo para dar un brinco absoluto en el programa
	# Actualiza el PC a la dirección en hexadecimal recibida.
	@staticmethod
	def JP(cadena):
		#Sanlto incondicional
		if (cadena.find(",") == -1):
			Z80.PC = cadena.replace("H","")
			print("PC JP"+Z80.PC)
		else:
		#Saltos condicionales
			if(cadena.find("C") == 0):
				if Z80.getFlagBit(0) == 0:
					return
				else:
					Z80.PC = cadena[2:6]
			elif(cadena.find("C") == 1):
				if Z80.getFlagBit(0) == 1:
					return
				else:
					Z80.PC = cadena[3:7]
			elif(cadena.find("Z") == 0):
				if Z80.getFlagBit(6) == 0:
					return
				else:
					Z80.PC = cadena[2:6]
			elif(cadena.find("Z") == 1):
				if Z80.getFlagBit(6) == 1:
					return
				else:
					Z80.PC = cadena[3:7]
			elif(cadena.find("O") == 1):
				if Z80.getFlagBit(2) == 1:
					return
				else:
					Z80.PC = cadena[3:7]
			elif(cadena.find("E") == 1):
				if Z80.getFlagBit(2) == 0:
					return
				else:
					Z80.PC = cadena[3:7]
			elif(cadena.find("P") == 0):
				if Z80.getFlagBit(7) == 1:
					return
				else:
					Z80.PC = cadena[2:6]
			elif(cadena.find("M") == 0):
				if Z80.getFlagBit(7) == 0:
					return
				else:
					Z80.PC = cadena[2:6]

	# Metodo para dar un brinco relativo al valor del PC con un
	# alcance en el rango de e = <-127,129> desde la dirección 
	# del primer código de operación de esta instrucción.
	# Recibe el valor del Brinco un numero hexadecimal en comple
	# mento a dos y lo suma al valor actual del PC.
	@staticmethod
	def JR(cadena):
		# Salto incondicional relativo
		if (cadena.find(",") == -1):  #Es un salto incondicional
			Z80.hexToDecJR(cadena[0:2])
		else:
		# Salto condicional relativo
			if(cadena.find("C") == 0):
				if Z80.getFlagBit(0) == 0:
					return
				else:
					Z80.hexToDecJR(cadena[2:4])
			elif(cadena.find("C") == 1):
				if Z80.getFlagBit(0) == 1:
					return
				else:
					Z80.hexToDecJR(cadena[3:5])
			elif(cadena.find("Z") == 0):
				if Z80.getFlagBit(6) == 0:
					return
				else:
					Z80.hexToDecJR(cadena[2:4])
			elif(cadena.find("Z") == 1):
				if Z80.getFlagBit(6) == 1:
					return
				else:
					Z80.hexToDecJR(cadena[3:5])

	# Metodo DJNZ que da un brinco relativo un número total de
	# veces del valor en el registro B, se decremenata en uno 
	# antes de cada Brinco. 
	@staticmethod
	def DJNZ(cadena):
		Z80.B = str(int(Z80.B)-1)
		if (int(Z80.B) != 0):
			Z80.hexToDecJR(cadena[0:2])
		else:
			print('Se acabo')
			return

	# Metodo que manda a llamar o no al metodo C4LL (CALL) 
	# Si se trata de una llamada incondicional le pasa el 
	# valor que recibe de entrada para actualizar el PC
	# Si se trata de una llamada condicional, verifica la 
	# condición y si la cumple llama a C4LL para actualizar
	# el PC.
	@staticmethod
	def CALL(cadena):
		if (cadena.find(",") == -1):
			Z80.C4LL(cadena)
		else:
			if(cadena.find("C") == 0):
				if Z80.getFlagBit(0) == 0:
					return
				else:
					Z80.C4LL(cadena[2:6])
			elif(cadena.find("C") == 1):
				if Z80.getFlagBit(0) == 1:
					return
				else:
					Z80.C4LL(cadena[3:7])
			elif(cadena.find("Z") == 0):
				if Z80.getFlagBit(6) == 0:
					return
				else:
					Z80.C4LL(cadena[2:6])
			elif(cadena.find("Z") == 1):
				if Z80.getFlagBit(6) == 1:
					return
				else:
					Z80.C4LL(cadena[3:7])
			elif(cadena.find("O") == 1):
				if Z80.getFlagBit(2) == 1:
					return
				else:
					Z80.C4LL(cadena[3:7])
			elif(cadena.find("E") == 1):
				if Z80.getFlagBit(2) == 0:
					return
				else:
					Z80.C4LL(cadena[3:7])
			elif(cadena.find("P") == 0):
				if Z80.getFlagBit(7) == 1:
					return
				else:
					Z80.C4LL(cadena[2:6])
			elif(cadena.find("M") == 0):
				if Z80.getFlagBit(7) == 0:
					return
				else:
					Z80.C4LL(cadena[2:6])

	# Función que almacena el valor del PC en la pila, para despues ser recuperado
	# además que da un brinco absoluto a la dirección que recibe.
	@staticmethod
	def C4LL(cadena):
		Z80.SP = int(Z80.SP,16)
		valorPC = Z80.PC
		print(Z80.SP)
		if (Z80.SP > 65036 and Z80.SP <= 65536):
			Memoria.mem[Z80.SP-1] = valorPC[0:2]
			Memoria.mem[Z80.SP-2] = valorPC[2:4]
			Z80.SP = str(Z80.tohex(Z80.SP - 2,16))
			Z80.PC = cadena
		else: 
			print("Pila llena")

	@staticmethod
	def RET(cadena):
		if (len(cadena) == 0):
			Z80.R3T()
		else:
			if(cadena.find("C") == 0):
				if Z80.getFlagBit(0) == 0:
					return
				else:
					Z80.R3T()
			elif(cadena.find("C") == 1):
				if Z80.getFlagBit(0) == 1:
					return
				else:
					Z80.R3T()
			elif(cadena.find("Z") == 0):
				if Z80.getFlagBit(6) == 0:
					return
				else:
					Z80.R3T()
			elif(cadena.find("Z") == 1):
				if Z80.getFlagBit(6) == 1:
					return
				else:
					Z80.R3T()
			elif(cadena.find("O") == 1):
				if Z80.getFlagBit(2) == 1:
					return
				else:
					Z80.R3T()
			elif(cadena.find("E") == 1):
				if Z80.getFlagBit(2) == 0:
					return
				else:
					Z80.R3T()
			elif(cadena.find("P") == 0):
				if Z80.getFlagBit(7) == 1:
					return
				else:
					Z80.R3T()
			elif(cadena.find("M") == 0):
				if Z80.getFlagBit(7) == 0:
					return
				else:
					Z80.R3T()

	# Regresa el PC almacenado en la pila al PC y pone ceros ('00')
	# además actualiza el valor del SP
	@staticmethod
	def R3T():
		Z80.SP = int(Z80.SP,16)
		if (Z80.SP >= 65035 and Z80.SP <= 65534):
			Z80.PC = Memoria.mem[Z80.SP+1]+Memoria.mem[Z80.SP]
			Memoria.mem[Z80.SP+1] = '--'
			Memoria.mem[Z80.SP] = '--'
			Z80.SP = str(Z80.tohex(Z80.SP + 2,16))
		else:
			print("Pila Vacia")

	# Metodo que utiliza el modo de direccionamienro de pagina cero
	# util ya que con un solo byte te permite dirigirte a varias 
	# posiciones de la pagina cero de la memoria donde usualmente 
	# suelen estar las subrutinas más utilizadas.
	@staticmethod
	def RST(cadena):
		cadena = cadena[0:2]
		Z80.SP = int(Z80.SP,16)
		valorPC = Z80.PC
		if (Z80.SP > 65036 and Z80.SP <= 65536):
			Memoria.mem[Z80.SP-1] = valorPC[0:2]
			Memoria.mem[Z80.SP-2] = valorPC[2:4]
			Z80.SP = str(Z80.tohex(Z80.SP - 2,16))
			Z80.PC = '00'+cadena
		else: 
			print("Pila llena")
	
	@staticmethod
	def obtenerCont(op2):
		if (op2.find('IX+')!=-1 or op2.find('IX+')!=-1):
			op2 = op2.replace("(","").replace(")","").replace("H","").split("+")
			reg = getattr(Z80, op2[0])
			des = op2[1]
			s = funciones.tohex(int(reg, 16) + funciones.hextodec(des), 16)
			cont = Z80.mem.obtenerContenido(s)
		elif op2.find('H)') != -1:
			op2 = op2.replace('(', '').replace(')', '').replace('H', '')
			cont = Z80.mem.obtenerContenido(op2)
		else:
			d = int(getattr(Z80, op2[0]) + getattr(Z80, op2[1]), 16)
			cont = Z80.mem.obtenerContenido(op2)
		return cont

	@staticmethod
	def obtenerPosicion(op1):
		if (op1.find("IX+") != -1 or op1.find("IY+") != -1):
			op1 = op1.replace("(","").replace(")","").replace("H","").split("+")
			reg = getattr(Z80, op1[0])
			des = op1[1]
			pos = funciones.tohex(int(reg, 16) + funciones.hextodec(des), 16)
		# Si es la direccion que contiene HL, se obtiene su contenido
		elif (op1 == "(HL)" or op1 == "(BC)" or op1 == "(DE)"):
			op1 = op1.replace('(','').replace(')','')
			pos = getattr(Z80, op1[0]) + getattr(Z80, op1[1])
		# El ultimo caso es que sea un numero en hexadecimal
		else:
			pos = op1.replace('(','').replace(')','').replace('H','')
		return pos

	@staticmethod
	def LD(op1, op2):
		if len(op1) == 1:
			if op2.find('C)') != -1 or op2.find('E)') != -1 or op2.find('H)') != -1:
				cont  = Z80.obtenerCont(op2)
				Z80.A = cont
			else:
				s = Z80.obtenerS(op2)
				setattr(Z80, op1, s)

		else:
			if op1.find('(') != -1 and len(op2) == 1:
				pos = Z80.obtenerPosicion(op1)
				s = getattr(Z80, op2)
				Z80.mem.cambiarContenido(s, pos)
			elif op1.find('(') != -1 and op2.find('H') != 1:
				pos = Z80.obtenerPosicion(op1)
				op2 = op2.replace('H','')
				Z80.mem.cambiarContenido(op2, pos)
			elif op1.find('('):
				ss = Z80.obtenerSS(op2)
				pos = Z80.obtenerPosicion(op1)
				Z80.mem.cambiarContenido(ss[0], pos + 1)
				Z80.mem.cambiarContenido(ss[1], pos)
			elif op1 == 'SP':
				ss = Z80.obtenerSS(op2)
				setattr(Z80, op1, ss)
			else:
				if op1 == 'IX' or op1 == 'IY':
					if op2.find('('):
						pos = Z80.obtenerPosicion(op2)
						a1 = Z80.mem.obtenerContenido(pos)
						a2 = Z80.mem.obtenerContenido(pos + 1)
						setattr(Z80, op1, a2 + a1)
					else:
						op2 = op2.replace('H', '')
						setattr(Z80, op1, op2)
				else:
					if op2.find('('):
						pos = Z80.obtenerPosicion(op2)
						a1 = Z80.mem.obtenerContenido(pos)
						a2 = Z80.mem.obtenerContenido(pos + 1)
						setattr(Z80, op1[0], a2)
						setattr(Z80, op1[1], a1)
					else:
						op2 = op2.replace('H', '')
						setattr(Z80, op1[0], op2[0])
						setattr(Z80, op1[1], op2[1])

	@staticmethod
	def PUSH(arg):
		Z80.SP = int(Z80.SP, 16)
		if Z80.SP >= 65034 and Z80.SP <= 65536:
			if arg == 'IX' or arg == 'IY':
				arg = getattr(Z80, arg)
				Z80.mem.cambiarContenido(arg[:2], hex(Z80.SP - 1)[2:])
				Z80.mem.cambiarContenido(arg[2:], hex(Z80.SP - 2)[2:])
				Z80.SP = funciones.tohex(Z80.SP - 2, 16)
			else:
				qL = getattr(Z80, arg[1])
				qH = getattr(Z80, arg[0])
				Z80.mem.cambiarContenido(qH, hex(Z80.SP - 1)[2:])
				Z80.mem.cambiarContenido(qL, hex(Z80.SP - 2)[2:])
				Z80.SP = funciones.tohex(Z80.SP - 2, 16)
		else: print('ERROR: Memoria llena')

	@staticmethod
	def POP(arg):
		Z80.SP = int(Z80.SP, 16)
		if Z80.SP >= 65034 and Z80.SP < 65536:
			if arg == 'IX':
				Z80.IX = Z80.mem.obtenerContenido(hex(Z80.SP + 1)[2:]) + Z80.mem.obtenerContenido(hex(Z80.SP)[2:])
				Z80.SP = hex(Z80.SP + 2)[2:].zfill(5).upper()
			elif arg == 'IY':
				Z80.IY = Z80.mem.obtenerContenido(hex(Z80.SP + 1)[2:]) + Z80.mem.obtenerContenido(hex(Z80.SP)[2:])
				Z80.SP = hex(Z80.SP + 2)[2:].zfill(5).upper()
			else:
				setattr(Z80, arg[0], Z80.mem.obtenerContenido(hex(Z80.SP + 1)[2:]))
				setattr(Z80, arg[1], Z80.mem.obtenerContenido(hex(Z80.SP)[2:]))
				Z80.SP = hex(Z80.SP + 2)[2:].zfill(5).upper()
		else: print('ERROR: Memoria Vacía')

	@staticmethod
	def intercambio(arg1, arg2):
		if arg2.rfind('\'') != -1:
			arg2 = arg2.replace('\'', '')
		aux = getattr(Z80, arg1[0])
		setattr(Z80, arg1[0], getattr(Z80, arg2[0]))
		setattr(Z80, arg2[0], aux)

		aux = getattr(Z80, arg1[1])
		setattr(Z80, arg1[1], getattr(Z80, arg2[1]))
		setattr(Z80, arg2[1], aux)

	@staticmethod
	def EX(arg1, arg2):
		# DE <-> HL o AF <-> A_F_
		if len(arg1) == 2:
			Z80.intercambio(arg1, arg2)
		# IX <-> (SP) o IY <-> (SP)
		elif arg2 == 'IX' or arg2 == 'IY':
			aux = getattr(Z80, arg2)
			Z80.POP(arg2)
			aux2 = getattr(Z80, arg2)
			setattr(Z80, arg2, aux)
			Z80.PUSH(arg2)
			setattr(Z80, arg2, aux2)
		# (SP) <-> HL
		else:
			aux = Z80.H + Z80.L
			Z80.POP(arg2)
			aux2 = Z80.H + Z80.L
			Z80.H = aux[:2]
			Z80.L = aux[2:]
			Z80.PUSH(arg2)
			Z80.H = aux2[:2]
			Z80.L = aux2[2:]

	@staticmethod
	def EXX():
		# BC <-> B_C_
		Z80.intercambio('BC', ['B_', 'C_'])

		# DE <-> D_E_
		Z80.intercambio('DE', ['D_', 'E_'])
		# HL <-> H_L_
		Z80.intercambio('HL', ['H_', 'L_'])

	@staticmethod
	def transferencia(sign):
		# (DE) <- (HL)
		dir1 = int(Z80.D + Z80.E, 16)
		dir2 = int(Z80.H + Z80.L, 16)
		con = Z80.mem.obtenerContenido(hex(dir2)[2:])
		Z80.mem.cambiarContenido(con, hex(dir1)[2:])
		# DE <- DE + 1 o DE <- DE - 1
		dir1 = eval(str(dir1) + sign + '1')
		dir1 = funciones.tohex(dir1, 16)
		Z80.D = dir1[:2]
		Z80.E = dir1[2:]
		# HL <- HL + 1 o  HL <- HL - 1
		dir2 = eval(str(dir2) + sign + '1')
		dir2 = funciones.tohex(dir2, 16)
		Z80.H = dir2[:2]
		Z80.L = dir2[2:]
		# BC <- BC - 1
		dir1 = int(Z80.B + Z80.C, 16) - 1
		if dir1 == 0:
			Z80.changeFlag(2, '0')
		else:
			Z80.changeFlag(2, '1')
		dir1 = funciones.tohex(dir1, 16)
		Z80.B = dir1[:2]
		Z80.C = dir1[2:]

	@staticmethod
	def LDI():
		Z80.changeFlag(1,'0')
		Z80.changeFlag(4,'0')
		Z80.transferencia('+')

	@staticmethod
	def LDIR():
		Z80.changeFlag(1,'0')
		Z80.changeFlag(4,'0')
		c = int(Z80.B + Z80.C, 16)
		while c != 0:
			Z80.transferencia('+')
			c -= 1

	@staticmethod
	def LDD():
		Z80.changeFlag(1,'0')
		Z80.changeFlag(4,'0')
		Z80.transferencia('-')

	@staticmethod
	def LDDR():
		Z80.changeFlag(1,'0')
		Z80.changeFlag(4,'0')
		c = int(Z80.B + Z80.C, 16)
		while c != 0:
			Z80.transferencia('-')
			c -= 1

	@staticmethod
	def busqueda(o):
		# BC <- BC - 1
		v = int(Z80.B + Z80.C, 16) - 1
		if v == 0:
			Z80.changeFlag(2, '0')
		else:
			Z80.changeFlag(2, '1')
		v = funciones.tohex(v, 16)
		Z80.B = v[:2]
		Z80.C = v[2:]
		# HL <- HL + 1 o HL <- HL - 1
		HL = Z80.H + Z80.L
		v = eval(str(int(HL, 16)) + o + '1')
		v = funciones.tohex(v, 16)
		Z80.H = v[:2]
		Z80.L = v[2:]
		# A - (HL)
		cont = Z80.mem.obtenerContenido(HL)
		Z80.halfCarry(Z80.A, cont, '-')
		Z80.changeFlag(1, '1')
		cont = int(Z80.A, 16) - int(cont, 16)
		Z80.sign(cont)
		if Z80.A == Z80.mem.obtenerContenido(HL):
			Z80.changeFlag(6, '1')
			return False
		else:
			Z80.changeFlag(6, '0')
			return True

	@staticmethod
	def CPI():
		Z80.busqueda('+')

	@staticmethod
	def CPIR():
		c = int(Z80.B + Z80.C, 16)
		while c != 0:
			b = Z80.busqueda('+')
			if b == False:
				break
			else:
				c -= 1

	@staticmethod
	def CPD():
		Z80.busqueda('-')

	@staticmethod
	def CPDR():
		c = int(Z80.B + Z80.C, 16)
		while c != 0:
			b = Z80.busqueda('-')
			if b == False:
				break
			else:
				c -= 1

	@staticmethod
	def ADD(op1, op2):
		if op1 == 'A':
			s = Z80.obtenerS(op2)
			Z80.halfCarry(Z80.A, s, '+')
			s = int(Z80.A, 16) + int(s, 16)
			Z80.carry(s)
			Z80.zero(s)
			Z80.overflow(s)
			Z80.sign(s)
			Z80.changeFlag(1,'0')
			Z80.A = funciones.tohex(s, 8)
		elif op1 == 'IX' or op1 == 'IY':
			s = int(getattr(Z80, op1), 16) + int(Z80.obtenerSS(op2), 16)
			Z80.carry(s)
			Z80.changeFlag(1,'0')
			s = funciones.tohex(s, 16)
			setattr(Z80, op1, s)
		else:
			HL = ''.join([Z80.H, Z80.L])
			ss = Z80.obtenerSS(op2)
			HL = int(HL, 16) + int(ss, 16)
			Z80.carry(HL)
			Z80.changeFlag(1,'0')
			HL = funciones.tohex()
			Z80.H = HL[:2]
			Z80.L = HL[2:]

	@staticmethod
	def ADC(op1, op2):
		CY = bin(int(Z80.F,16))[2:].zfill(8)[0]
		if (op1 == "A"):
			s = Z80.obtenerS(op2)
			Z80.halfCarry(Z80.A, s, '+')
			s = int(Z80.A, 16) + int(s, 16) + int(CY, 16)
			Z80.carry(s)
			Z80.zero(s)
			Z80.overflow(s)
			Z80.sign(s)
			Z80.changeFlag(1,'0')
			Z80.A = funciones.tohex(s, 8)
		else:
			HL = ''.join([Z80.H, Z80.L])
			ss = Z80.obtenerSS(op2)
			HL = int(HL,16) + int(ss,16) + int(CY, 2)
			Z80.carry(s)
			Z80.zero(s)
			Z80.overflow(s)
			Z80.sign(s)
			Z80.changeFlag(1,'0')
			HL = funciones.tohex(HL, 16)
			# El primer byte se guarda en H y el segundo en L
			Z80.H = HL[:2]
			Z80.L = HL[2:]

	@staticmethod
	def SUB(op1, op2):
		s = Z80.obtenerS(op2)
		Z80.halfCarry(Z80.A, s, '-')
		s = int(Z80.A, 16) - int(s, 16)
		Z80.carry(s)
		Z80.zero(s)
		Z80.overflow(s)
		Z80.sign(s)
		Z80.changeFlag(1,'1')
		Z80.A = funciones.tohex(s)

"""procesador = Z80()
procesador.callMethod(procesador, "DAA","")
print(procesador.A)
print(bin(int(procesador.F,16)))"""