import desensamblador
import funciones
import memoria

class Z80(object):
    # Registros son declarados como cadenas en hexadecimal
    B = "DE"
    C = "02"
    D = "FF"
    E = "FE"
    H = "FF"
    L = "FD"
    A = "00"
    F = "00"
    SP = "10000" # El apuntador de pila inicia en la localidad 65536
    IX = "0000 "
    IY = "1224"
    PC = "00"
    IFF1 = "1"
    IFF2 = "1"
    I = "00"
    R = "00"
    # Registros auxiliares
    B_ = "17"
    C_ = "18"
    D_ = "19"
    E_ = "1A"
    H_ = "1B"
    L_ = "1C"
    A_ = "00"
    F_ = "00"
    mem = memoria.Memoria()

    # Metodo para mandar llamar a otro de los metodos del procesador mediante el nombre de la operacion a realizar
    # Si no hay operandos, se manda una cadena vacia
    @staticmethod
    def callMethod(object, name, opr):
        if (opr == ""):
            getattr(object, name)()
        elif (len(opr) == 1):
            getattr(object, name)(opr)
        else:
            opr = opr.split(",")
            getattr(object, name)(opr[0], opr[1])

    """ Metodo que cambia las banderas de un bit de terminado
        por un valor dado """
    @staticmethod
    def changeFlag(bitIndex, val):
        Z80.F = funciones.hexToBin(Z80.F)
        Z80.F = Z80.F[:7 - bitIndex] + val + Z80.F[7 - bitIndex + 1:]
        Z80.F = funciones.binToHex(Z80.F)

    # Funcion para obtener alguna de las banderas
    @staticmethod
    def getFlagBit(bitIndex):
        Z80.F = funciones.hexToBin(Z80.F)
        estado = int(Z80.F[7 - bitIndex])
        Z80.F = funciones.binToHex(Z80.F)
        return estado

    # Mandar en decimal el resultado para checar acarreo
    @staticmethod
    def carry(res):
        res = funciones.tobin(res, 16)
        pos = res.find('1')
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
        s puede ser n, r, (HL), (IX+d) e (IY+d) """
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
    def obtenerCont(op2):
        if op2.find('IX+') or op2.find('IX+'):
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
                Z80.mem.cambiarContenido(s, hex(pos)[2:])
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