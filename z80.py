import funciones
import memoria

class Z80(object):
    # Registros son declarados como cadenas en hexadecimal
    B = "00"
    C = "02"
    D = "FF"
    E = "FE"
    H = "FF"
    L = "FC"
    A = "00"
    F = "00"
    SP = "10000" # El apuntador de pila inicia en la localidad 65536
    IX = "1234"
    IY = "2540"
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

    """ Metodo que cambia las banderas de un bit de terminado
        por un valor dado """
    @staticmethod
    def changeFlag(bitIndex, val):
        Z80.F = funciones.hexToBin(Z80.F)
        Z80.F = Z80.F[:7 - bitIndex] + val + Z80.F[7 - bitIndex + 1:]
        Z80.F = funciones.binToHex(Z80.F)

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

    """@staticmethod
    def LD(arg1, arg2):
        if arg1.find('('):"""

    @staticmethod
    def PUSH(arg):
        Z80.SP = int(Z80.SP, 16)
        if Z80.SP >= 65034 and Z80.SP <= 65536:
            if arg == 'IX' or arg == 'IY':
                arg = getattr(Z80, arg)
                Z80.mem.cambiarContenido(arg[:2], Z80.SP - 1)
                Z80.mem.cambiarContenido(arg[2:], Z80.SP - 2)
                Z80.SP = Z80.tohex(Z80.SP - 2, 16)
            else:
                qL = getattr(Z80, arg[1])
                qH = getattr(Z80, arg[0])
                Z80.mem.cambiarContenido(qH, Z80.SP - 1)
                Z80.mem.cambiarContenido(qL, Z80.SP - 2)
                Z80.SP = Z80.tohex(Z80.SP - 2, 16)
        else: print('ERROR: Memoria llena')

    @staticmethod
    def POP(arg):
        Z80.SP = int(Z80.SP, 16)
        if Z80.SP >= 65034 and Z80.SP < 65536:
            if arg == 'IX':
                Z80.IX = Z80.mem.obtenerContenido(Z80.SP + 1) + Z80.mem.obtenerContenido(Z80.SP)
                Z80.SP = hex(Z80.SP + 2)[2:].zfill(5).upper()
            elif arg == 'IY':
                Z80.IY = Z80.mem.obtenerContenido(Z80.SP + 1) + Z80.mem.obtenerContenido(Z80.SP)
                Z80.SP = hex(Z80.SP + 2)[2:].zfill(5).upper()
            else:
                setattr(Z80, arg[0], Z80.mem.obtenerContenido(Z80.SP + 1))
                setattr(Z80, arg[1], Z80.mem.obtenerContenido(Z80.SP))
                Z80.SP = hex(Z80.SP + 2)[2:].zfill(5).upper()
        else: print('ERROR: Memoria Vacía')

    @staticmethod
    def intercambio(arg1, arg2):
        aux = getattr(Z80, arg1[0])
        setattr(Z80, arg1[0], arg2[0])
        setattr(Z80, arg2[0], aux)

        aux = getattr(Z80, arg1[1])
        setattr(Z80, arg1[1], arg2[1])
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
    def LDI():
        Z80.F = Z80.changeFlag(1, '0')
        Z80.F = Z80.changeFlag(4, '0')
        # (DE) <- (HL) 
        dir1 = int(Z80.D + Z80.E, 16)
        dir2 = int(Z80.H + Z80.L, 16)
        Memoria.mem[dir1] = Memoria.mem[dir2]
        # DE <- DE + 1
        dir1 = Z80.tohex(dir1 + 1, 16)
        Z80.D = dir1[:2]
        Z80.E = dir1[2:]
        # HL <- HL + 1
        dir2 = Z80.tohex(dir2 + 1, 16)
        Z80.H = dir2[:2]
        Z80.L = dir2[2:]
        # BC <- BC - 1
        dir1 = int(Z80.B + Z80.C, 16) - 1
        if dir1 == 0:
            Z80.F = Z80.changeFlag(2, '0')
            dir1 = Z80.tohex(dir1, 16)
            Z80.B = dir1[:2]
            Z80.C = dir1[2:]
        else:
            Z80.F = Z80.changeFlag(2, '1')
            dir1 = Z80.tohex(dir1, 16)
            Z80.B = dir1[:2]
            Z80.C = dir1[2:]
    @staticmethod
    def LDIR():
        c = int(Z80.B + Z80.C, 16)
        while c != 0:
            # (DE) <- (HL) 
            dir1 = int(Z80.D + Z80.E, 16)
            dir2 = int(Z80.H + Z80.L, 16)
            Memoria.mem[dir1] = Memoria.mem[dir2]
            # DE <- DE + 1
            dir1 = Z80.tohex(dir1 + 1, 16)
            Z80.D = dir1[:2]
            Z80.E = dir1[2:]
            # HL <- HL + 1
            dir2 = Z80.tohex(dir2 + 1, 16)
            Z80.H = dir2[:2]
            Z80.L = dir2[2:]
            # BC <- BC - 1
            c = c - 1
            dir3 = Z80.tohex(c, 16)
            Z80.B = dir3[:2]
            Z80.C = dir3[2:]
        Z80.F = Z80.changeFlag(1, '0')
        Z80.F = Z80.changeFlag(4, '0')
        Z80.F = Z80.changeFlag(2, '0')

    @staticmethod
    def LDD():
        Z80.F = Z80.changeFlag(1, '0')
        Z80.F = Z80.changeFlag(4, '0')
        # (DE) <- (HL) 
        dir1 = int(Z80.D + Z80.E, 16)
        dir2 = int(Z80.H + Z80.L, 16)
        Memoria.mem[dir1] = Memoria.mem[dir2]
        # DE <- DE - 1
        dir1 = Z80.tohex(dir1 - 1, 16)
        Z80.D = dir1[:2]
        Z80.E = dir1[2:]
        # HL <- HL - 1
        dir2 = Z80.tohex(dir2 - 1, 16)
        Z80.H = dir2[:2]
        Z80.L = dir2[2:]
        # BC <- BC - 1
        dir1 = int(Z80.B + Z80.C, 16) - 1
        if dir == 0:
            Z80.F = Z80.changeFlag(2, '0')
            dir1 = Z80.tohex(dir1, 16)
            Z80.B = dir1[:2]
            Z80.C = dir1[2:]
        else:
            Z80.F = Z80.changeFlag(2, '1')
            dir1 = Z80.tohex(dir1, 16)
            Z80.B = dir1[:2]
            Z80.C = dir1[2:]

    @staticmethod
    def LDDR():
        c = int(Z80.B + Z80.C, 16)
        while c != 0:
            # (DE) <- (HL) 
            dir1 = int(Z80.D + Z80.E, 16)
            dir2 = int(Z80.H + Z80.L, 16)
            Memoria.mem[dir1] = Memoria.mem[dir2]
            # DE <- DE - 1
            dir1 = Z80.tohex(dir1 - 1, 16)
            Z80.D = dir1[:2]
            Z80.E = dir1[2:]
            # HL <- HL - 1
            dir2 = Z80.tohex(dir2 - 1, 16)
            Z80.H = dir2[:2]
            Z80.L = dir2[2:]
            # BC <- BC - 1
            c = c - 1
            dir3 = Z80.tohex(c, 16)
            Z80.B = dir3[:2]
            Z80.C = dir3[2:]
        Z80.F = Z80.changeFlag(1, '0')
        Z80.F = Z80.changeFlag(4, '0')
        Z80.F = Z80.changeFlag(2, '0')

    @staticmethod
    def CPI():
        # A - (HL)
        HL = int(Z80.H + Z80.L, 16)
        if int(Z80.A, 16) - Memoria.mem[HL] == 0:
            Z80.F = Z80.changeFlag(6, 1)
        else:
            Z80.F = Z80.changeFlag(6, 0)
        # HL <- HL + 1
        v = int(Z80.H + Z80.L, 16) + 1
        v = Z80.tohex(v, 16)
        Z80.H = v[:2]
        Z80.L = v[2:]
        # BC <- BC - 1
        v = int(Z80.B + Z80.C, 16) - 1
        if v == 0:
            Z80.F = Z80.changeFlag(2, 0)
        else:
            Z80.F = Z80.changeFlag(2, 1)
        v = Z80.tohex(v, 16)
        Z80.B = v[:2]
        Z80.C = v[2:]

    @staticmethod
    def CPIR():
        c = int(Z80.B + Z80.C, 16)
        while c != 0:
            # A - (HL)
            HL = int(Z80.H + Z80.L, 16)
            if int(Z80.A, 16) - Memoria.mem[HL] == 0:
                Z80.F = Z80.changeFlag(6, 1)
                break
            else:
                Z80.F = Z80.changeFlag(6, 0)
            # HL <- HL + 1
            v = int(Z80.H + Z80.L, 16) + 1
            v = Z80.tohex(v, 16)
            Z80.H = v[:2]
            Z80.L = v[2:]
            # BC <- BC - 1
            c -= 1
            v = Z80.tohex(c, 16)
            Z80.B = v[:2]
            Z80.C = v[2:]
            if c == 0:
                Z80.F = Z80.changeFlag(2, 0)
            else:
                Z80.F = Z80.changeFlag(2, 1)

    @staticmethod
    def CPD():
        # A - (HL)
        HL = int(Z80.H + Z80.L, 16)
        if int(Z80.A, 16) - Memoria.mem[HL] == 0:
            Z80.F = Z80.changeFlag(6, 1)
        else:
            Z80.F = Z80.changeFlag(6, 0)
        # HL <- HL - 1
        v = int(Z80.H + Z80.L, 16) - 1
        v = Z80.tohex(v, 16)
        Z80.H = v[:2]
        Z80.L = v[2:]
        # BC <- BC - 1
        v = int(Z80.B + Z80.C, 16) - 1
        if v == 0:
            Z80.F = Z80.changeFlag(2, 0)
        else:
            Z80.F = Z80.changeFlag(2, 1)
        v = Z80.tohex(v, 16)
        Z80.B = v[:2]
        Z80.C = v[2:]

    @staticmethod
    def CPDR():
        c = int(Z80.B + Z80.C, 16)
        while c != 0:
            # A - (HL)
            HL = int(Z80.H + Z80.L, 16)
            if int(Z80.A, 16) - Memoria.mem[HL] == 0:
                Z80.F = Z80.changeFlag(6, 1)
            else:
                Z80.F = Z80.changeFlag(6, 0)
            # HL <- HL - 1
            v = int(Z80.H + Z80.L, 16) - 1
            v = Z80.tohex(v, 16)
            Z80.H = v[:2]
            Z80.L = v[2:]
            # BC <- BC - 1
            c -= 1
            v = Z80.tohex(c, 16)
            Z80.B = v[:2]
            Z80.C = v[2:]
            if c == 0:
                Z80.F = Z80.changeFlag(2, 0)
                break
            else:
                Z80.F = Z80.changeFlag(2, 1)

    @staticmethod
    def ADD(op1, op2):
        if op1 == 'A':
            s = Z80.obtenerS(op2)
            Z80.A = funciones.tohex(int(Z80.A, 16) + int(s, 16))
        elif op1 == 'IX' or op1 == 'IY':
            s = funciones.tohex(int(getattr(Z80, op1), 16) + int(Z80.obtenerSS(op2), 16), 16)
            setattr(Z80, op1, s)
        else:
            HL = ''.join([Z80.H, Z80.L])
            ss = Z80.obtenerSS(op2)
            HL = funciones.tohex(int(HL, 16) + int(ss, 16))
            Z80.H = HL[:2]
            Z80.L = HL[2:]

    @staticmethod
    def SBC(op1, op2):
        CY = bin(int(Z80.F,16))[2:].zfill(8)[0]
        if (op1 == "A"):
            s = Z80.obtenerS(op2)
            Z80.A = funciones.tohex(int(Z80.A, 16) + int(s, 16) + int(CY, 16), 8)
        else:
            HL = ''.join([Z80.H, Z80.L])
            ss = Z80.obtenerSS(op2)
            HL = funciones.tohex(int(HL,16) + int(ss,16) + int(CY, 2), 16)
            # El primer byte se guarda en H y el segundo en L
            Z80.H = HL[:2]
            Z80.L = HL[2:]

    @staticmethod
    def SUB(op1, op2):
        s = Z80.obtenerS(op2)
        Z80.A = funciones.tohex(int(Z80.A, 16) + int(s, 16))