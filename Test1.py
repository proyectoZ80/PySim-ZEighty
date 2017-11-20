from z80 import Z80
#test para evaluar  función Z80.changeFlag
#cambiar banderas correctamente
for i in range(8):
    Z80.changeFlag(i, "1")
    Z80.changeFlag(i, "1")
    print(Z80.F)
for i in range(8):
    Z80.changeFlag(i, "0")
    Z80.changeFlag(i, "0")
    print(Z80.F)
