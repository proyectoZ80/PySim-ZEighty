<<<<<<< HEAD
import z80
=======
import Z80
>>>>>>> Angel

class Libraries(object):

    @staticmethod
    def ObtainFlag(position):
<<<<<<< HEAD
        flags  = z80.Z80.hexToBin(z80.Z80.F)
=======
        flags  = Z80.Z80.hexToBin(Z80.Z80.F)
>>>>>>> Angel
        return flags[7-position]

    @staticmethod
    def checkFlags():
        print("SZXHXPNC")
<<<<<<< HEAD
        print(z80.Z80.hexToBin(z80.Z80.F))
=======
        print(Z80.Z80.hexToBin(Z80.Z80.F))
>>>>>>> Angel

    @staticmethod
    def getDisplacement(register):
        return register[4:len(register)-2]

    @staticmethod
    def isHL_IX_IY(registro):
        registro = registro.strip()
        #print("displacement "+ Libraries.getDisplacement(registro))
        if registro == "(HL)":
            #print("es HL")
<<<<<<< HEAD
            memoryAddress = getattr(z80.Z80,"H") + getattr(z80.Z80,"L")
        elif "IX" in registro:
            #print("es IX")
            memoryAddress = hex(int(getattr(z80.Z80,"IX"), 16) + int(Libraries.getDisplacement(registro), 16))[2:]
        else:
            #print("es IY")
            memoryAddress = hex(int(getattr(z80.Z80,"IY"), 16) + int(Libraries.getDisplacement(registro), 16))[2:]
=======
            memoryAddress = getattr(Z80.Z80,"H") + getattr(Z80.Z80,"L")
        elif "IX" in registro:
            #print("es IX")
            memoryAddress = hex(int(getattr(Z80.Z80,"IX"), 16) + int(Libraries.getDisplacement(registro), 16))[2:]
        else:
            #print("es IY")
            memoryAddress = hex(int(getattr(Z80.Z80,"IY"), 16) + int(Libraries.getDisplacement(registro), 16))[2:]
>>>>>>> Angel
        #print("memory Address " + memoryAddress )
        return memoryAddress

    @staticmethod
    def CircularLeftRotation(numberInHEX):
        """ función para hacer rotacion circular hacia la izquierda y set la bandera C
        con la posición 7 de la representación binario del número en Hexadecimal"""
        #convierte el valor del registro  a binario
<<<<<<< HEAD
        numberInBIN = z80.Z80.hexToBin(numberInHEX)
=======
        numberInBIN = Z80.Z80.hexToBin(numberInHEX)
>>>>>>> Angel
        #tmp toma el valor del bit 7
        tmp = numberInBIN[0]
        #pasar el valor del bit 7 a la posición 0 y dezplazar las demás posiciones
        #excepto la del bit 7
        numberInBIN = numberInBIN[1:] + tmp
<<<<<<< HEAD
        z80.Z80.changeFlag(0,tmp)
=======
        Z80.Z80.changeFlag(0,tmp)
>>>>>>> Angel
        return numberInBIN

    @staticmethod
    def LeftRotation(numberInHEX):
<<<<<<< HEAD
        numberInBIN = z80.Z80.hexToBin(numberInHEX)
=======
        numberInBIN = Z80.Z80.hexToBin(numberInHEX)
>>>>>>> Angel
        #print("registro en binario "+numberInBIN)
        tmp = numberInBIN[0]
        #print("numero en binario antes de la rotación " + numberInBIN)
        #print("C " + Libraries.ObtainFlag(0))
        numberInBIN = numberInBIN[1:] + Libraries.ObtainFlag(0)
        #print("numero en binario después de la rotación "+numberInBIN)
        #C is data from bit 7 of source register
<<<<<<< HEAD
        z80.Z80.changeFlag(0,tmp)
=======
        Z80.Z80.changeFlag(0,tmp)
>>>>>>> Angel
        return numberInBIN

    @staticmethod
    def CircularRightRotation(numberInHEX):
        #convierte el valor del registro  a binario
<<<<<<< HEAD
        numberInBIN = z80.Z80.hexToBin(numberInHEX)
=======
        numberInBIN = Z80.Z80.hexToBin(numberInHEX)
>>>>>>> Angel
        #tmp toma el valor del Bit 0
        tmp = numberInBIN[7]
        #pasar el valor del bit 0 a la posición 7 y desplazar las demás posiciones
        #excepto la del bit 0
        numberInBIN = tmp + numberInBIN[:7]
        #C is data from bit 0 of source register
<<<<<<< HEAD
        z80.Z80.changeFlag(0, tmp)
=======
        Z80.Z80.changeFlag(0, tmp)
>>>>>>> Angel
        return numberInBIN

    @staticmethod
    def RightRotation(numberInHEX):
        #convierte el valor del registro  a binario
<<<<<<< HEAD
        numberInBIN = z80.Z80.hexToBin(numberInHEX)
=======
        numberInBIN = Z80.Z80.hexToBin(numberInHEX)
>>>>>>> Angel
        #tmp toma el valor del Bit 0
        tmp = numberInBIN[7]
        #pasar el valor del bit 0 a la bandera C y desplazar las demás posiciones
        #excepto la del bit 0 y poner en el bit 7 el valor previo de C
        numberInBIN = Libraries.ObtainFlag(0) + numberInBIN[:7]
        #C is data from bit 0 of source register
<<<<<<< HEAD
        z80.Z80.changeFlag(0, tmp)
=======
        Z80.Z80.changeFlag(0, tmp)
>>>>>>> Angel
        return numberInBIN

    @staticmethod
    def ShiftLeft(numberInHEX):
<<<<<<< HEAD
        numberInBIN = z80.Z80.hexToBin(numberInHEX)
=======
        numberInBIN = Z80.Z80.hexToBin(numberInHEX)
>>>>>>> Angel
        print("number bin "+ numberInBIN)
        tmp = numberInBIN[0]
        print("tmp " + tmp)
        numberInBIN = numberInBIN[1:] + "0"
<<<<<<< HEAD
        z80.Z80.changeFlag(0, tmp)
=======
        Z80.Z80.changeFlag(0, tmp)
>>>>>>> Angel
        return numberInBIN

    @staticmethod
    def RightArithmeticShift(numberInHEX):
<<<<<<< HEAD
        numberInBIN = z80.Z80.hexToBin(numberInHEX)
=======
        numberInBIN = Z80.Z80.hexToBin(numberInHEX)
>>>>>>> Angel
        print("number bin " + numberInBIN)
        tmp = numberInBIN[7]
        print("tmp " + tmp)
        numberInBIN = numberInBIN[0] + numberInBIN[:7]
        print("number bin con shift aritmetico " + numberInBIN)
<<<<<<< HEAD
        z80.Z80.changeFlag(0, tmp)
=======
        Z80.Z80.changeFlag(0, tmp)
>>>>>>> Angel
        return numberInBIN

    @staticmethod
    def RightLogicalShift(numberInHEX):
<<<<<<< HEAD
        numberInBIN = z80.Z80.hexToBin(numberInHEX)
=======
        numberInBIN = Z80.Z80.hexToBin(numberInHEX)
>>>>>>> Angel
        print("number bin " + numberInBIN)
        tmp = numberInBIN[7]
        print("tmp " + tmp)
        numberInBIN = "0" + numberInBIN[:7]
        print("number bin con shift aritmetico " + numberInBIN)
<<<<<<< HEAD
        z80.Z80.changeFlag(0, tmp)
=======
        Z80.Z80.changeFlag(0, tmp)
>>>>>>> Angel
        return numberInBIN


    @staticmethod
    def ChangeS(numberInBIN):
        if numberInBIN[0] == "1":
<<<<<<< HEAD
            z80.Z80.changeFlag(7, "1")
        else:
            z80.Z80.changeFlag(7, "0")
=======
            Z80.Z80.changeFlag(7, "1")
        else:
            Z80.Z80.changeFlag(7, "0")
>>>>>>> Angel

    @staticmethod
    def ChangeP(numberInBIN):
        #contando la occurencias de unos dentro del numero en Binario
        setP = numberInBIN.count("1")
        #si el registro tiene numero par de unos
        #set la bandera P
        #si no reset la bandera P
        if (setP % 2 == 0):
<<<<<<< HEAD
            z80.Z80.changeFlag(2, "1")
        else:
            z80.Z80.changeFlag(2, "0")
=======
            Z80.Z80.changeFlag(2, "1")
        else:
            Z80.Z80.changeFlag(2, "0")
>>>>>>> Angel

    @staticmethod
    def ChangeZ(numberInBIN):
        if numberInBIN == "00000000" :
<<<<<<< HEAD
            z80.Z80.changeFlag(6, "1")
        else:
            z80.Z80.changeFlag(6, "0")
=======
            Z80.Z80.changeFlag(6, "1")
        else:
            Z80.Z80.changeFlag(6, "0")
>>>>>>> Angel
