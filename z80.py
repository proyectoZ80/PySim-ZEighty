import desensamblador
from memoria import Memoria

class Z80(object):
    # Registros son declarados como cadenas en hexadecimal
    B = "12"
    C = "35"
    D = "00"
    E = "00"
    H = "00"
    L = "00"
    A = "00"
    F = "00"
    SP = "10000"
    IX = "1312"
    IY = "2134"
    PC = "00"
    IFF1 = "00"
    IFF2 = "00"
    I = "00"
    R = "00"
    # Registros auxiliares
    B_ = "12"
    C_ = "35"
    D_ = "00"
    E_ = "00"
    H_ = "00"
    L_ = "00"
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
        Z80.F = Z80.F[:bitIndex] + val + Z80.F[bitIndex+1:]
        Z80.F = Z80.binToHex(Z80.F)
        return Z80.F

    """@staticmethod
    def LD(arg1, arg2):
        if arg1.find('('):"""

    @staticmethod
    def PUSH(arg):
        Z80.SP = int(Z80.SP, 16)
        if Z80.SP >= 65035 and Z80.SP <= 65536:
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
        if arg1 == 'DE':
            aux = Z80.D
            Z80.D = Z80.H
            Z80.H = aux
            aux = Z80.E
            Z80.E = Z80.L
            Z80.L = aux
        elif arg1 == 'AF':
            aux = Z80.A
            Z80.A = Z80.A_
            Z80.A_ = aux
            aux = Z80.F
            Z80.F = Z80.F_
            Z80.F_ = aux
        else:
            if arg2 == 'IX' or arg2 == 'IY':
                aux = getattr(Z80, arg2)
                Z80.SP = int(Z80.SP, 16)
                a = Memoria.mem[Z80.SP]
                Memoria.mem[Z80.SP] = aux[2:]
                aux[2:] = a
                a = Memoria.mem[Z80.SP + 1]
                Memoria.mem[Z80.SP] = aux[:2]
                aux[:2] = a
                setattr(Z80, arg2, aux)
                Z80.SP = hex(Z80.SP)[2:].zfill(5).upper()

            else:
                Z80.SP = int(Z80.SP, 16)
                a = Z80.H
                Z80.H = Memoria.mem[Z80.SP + 1]
                Memoria.mem[Z80.SP + 1] = a
                a = Z80.L
                Z80.L = Memoria.mem[Z80.SP]
                Memoria.mem[Z80.SP] = a
                Z80.SP = hex(Z80.SP)[2:].zfill(5).upper()

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