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