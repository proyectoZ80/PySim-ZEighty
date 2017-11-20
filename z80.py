import desensamblador
from memoria import Memoria

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
    IFF1 = "00"
    IFF2 = "00"
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

    @staticmethod
    def tohex(num, nbits):
        return hex((num + (1 << nbits)) % (1 << nbits))[2:].upper()
    
    @staticmethod
    def hexToBin(numHex):
        return bin(int(numHex, 16))[2:].zfill(8)
    @staticmethod
    def binToHex(numBin):
        return hex(int(numBin, 2))[2:].zfill(2)

    @staticmethod
    def changeFlag(bitIndex, val):
        Z80.F = Z80.hexToBin(Z80.F)
        Z80.F = Z80.F[:7 - bitIndex] + val + Z80.F[7 - bitIndex + 1:]
        Z80.F = Z80.binToHex(Z80.F)
        return Z80.F

    """@staticmethod
    def LD(arg1, arg2):
        if arg1.find('('):"""

    @staticmethod
    def PUSH(arg):
        Z80.SP = int(Z80.SP, 16)
        if Z80.SP > 65034 and Z80.SP <= 65536:
            if arg == 'IX' or arg == 'IY':
                arg = getattr(Z80, arg)
                Memoria.mem[Z80.SP-1] = arg[:2]
                Memoria.mem[Z80.SP-2] = arg[2:]
                Z80.SP = Z80.tohex(Z80.SP - 2, 16)
            else:
                qL = getattr(Z80, arg[1])
                qH = getattr(Z80, arg[0])
                Memoria.mem[Z80.SP-1] = qH
                Memoria.mem[Z80.SP-2] = qL
                Z80.SP = Z80.tohex(Z80.SP - 2, 16)
        else: print('ERROR: Memoria llena')

    @staticmethod
    def POP(arg):
        Z80.SP = int(Z80.SP, 16)
        if Z80.SP >= 65035 and Z80.SP < 65536:
            if arg == 'IX':
                Z80.IX = Memoria.mem[Z80.SP+1] + Memoria.mem[Z80.SP]
                Z80.SP = hex(Z80.SP + 2)[2:].zfill(5).upper()
            elif arg == 'IY':
                Z80.IY = Memoria.mem[Z80.SP+1] + Memoria.mem[Z80.SP]
                Z80.SP = hex(Z80.SP + 2)[2:].zfill(5).upper()
            else:
                setattr(Z80, arg[0], Memoria.mem[Z80.SP + 1])
                setattr(Z80, arg[1], Memoria.mem[Z80.SP])
                Z80.SP = hex(Z80.SP + 2)[2:].zfill(5).upper()
        else: print('ERROR: Memoria Vacía')

    @staticmethod
    def EX(arg1, arg2):
        # DE <-> HL
        if arg1 == 'DE':
            aux = Z80.D
            Z80.D = Z80.H
            Z80.H = aux
            aux = Z80.E
            Z80.E = Z80.L
            Z80.L = aux
        elif arg1 == 'AF':
            # AF <-> A_F_
            aux = Z80.A
            Z80.A = Z80.A_
            Z80.A_ = aux
            aux = Z80.F
            Z80.F = Z80.F_
            Z80.F_ = aux
        else:
            # IX <-> (SP) o IY <-> (SP)
            if arg2 == 'IX' or arg2 == 'IY':
                aux = getattr(Z80, arg2)
                Z80.POP(arg2)
                aux2 = getattr(Z80, arg2)
                setattr(Z80, arg2, aux)
                Z80.PUSH(arg2)
                setattr(Z80, arg2, aux2)
            else:
                # (SP) <-> HL
                aux1 = getattr(Z80, arg2[0])
                aux2 = getattr(Z80, arg2[1])
                Z80.POP(arg2)
                aux3 = getattr(Z80, arg2[0])
                aux4 = getattr(Z80, arg2[1])
                setattr(Z80, arg2[0], aux1)
                setattr(Z80, arg2[1], aux2)
                Z80.PUSH(arg2)
                setattr(Z80, arg2[0], aux3)
                setattr(Z80, arg2[1], aux4)

    @staticmethod
    def EXX():
        # BC <-> B_C_
        aux = Z80.B
        Z80.B = Z80.B_
        Z80.B_ = aux
        aux = Z80.C
        Z80.C = Z80.C_
        Z80.C_ = aux

        # DE <-> D_E_
        aux = Z80.D
        Z80.D = Z80.D_
        Z80.D_ = aux
        aux = Z80.E
        Z80.E = Z80.E_
        Z80.E_ = aux

        # HL <-> H_L_
        aux = Z80.H
        Z80.H = Z80.H_
        Z80.H_ = aux
        aux = Z80.L
        Z80.L = Z80.L_
        Z80.L_ = aux

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

