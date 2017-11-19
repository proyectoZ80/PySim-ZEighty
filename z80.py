class Z80(object):
    #Registros
    B = "0"
    C = "0"
    D = "0"
    E = "0"
    H = "0"
    L = "0"
    A = "0"
    F = "0"
    sp = "0"
    ix = "0"
    iy = "0"

    #funcion para convertir un número hexadecimal a binario
    @staticmethod
    def toHEXtoBIN(numberInHEX):
        numberInHEX = int(numberInHEX, 16)
        numberInBIN = bin(numberInHEX)[2:].zfill(8)
        return numberInBIN
    #metodo para cambiar las banderas
    #indices de banderas [S Z X H X P/V N C]
    #                                    [7 6 5 4  3   2     1  0]
    @staticmethod
    def cambiarBanderas(bitIndex,value):
        banderas = list(Z80.toHEXtoBIN(Z80.F)
        origin/instrucciones
        #print(banderas)
        length  = len(banderas) - 1
        if(value == banderas[length - bitIndex]):
            return
        if(banderas[length - bitIndex] != "0"):
            banderas[length - bitIndex] = "0"
        else:
            banderas[length - bitIndex] = "1"
        print(banderas)
        Z80.F = hex(int("".join(banderas),2))[2:]

#print(Z80.toHEXtoBIN(Z80.F))
for i in range(8):
    Z80.cambiarBanderas(i)
print(Z80.F) # agregue esta linea
for i in range(8):
    Z80.cambiarBanderas(i)
print(Z80.F)
#print(int(Z80.F,16))
#print(hex(int("1",16)+int("F",16)))
