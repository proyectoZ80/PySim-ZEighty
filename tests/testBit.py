from z80 import Z80 as z
from Libraries import Libraries as Library
from memoria import Memoria as m
#test BIT
print("\ntest 1\n")
z.B = "20"
Library.checkFlags()
z.BIT(["5","B"])
Library.checkFlags()

print("\ntest 2\n")
z.B = "00"
Library.checkFlags()
z.BIT(["5", "B"])
Library.checkFlags()

print("\ntest 1 BIT8\n")
z.H = "28"
z.L = "28"
m.cambiarContenido("88", z.H + z.L)
Library.checkFlags()
z.BIT(["7","(HL)"])
Library.checkFlags()

print("\ntest 2 BIT8\n")

memoryAddress = "1002"
z.IX = "1000"
m.cambiarContenido("88", memoryAddress)
Library.checkFlags()
z.BIT(["7","(IX+2h)"])
Library.checkFlags()

print("\ntest 3 BIT8\n")
#decir que si no inicializa con cero entonces tendré errores
memoryAddress = "1022"
z.IY = "1020"
m.cambiarContenido("01", "1022")
Library.checkFlags()
z.BIT(["1","(IY+2h)"])
Library.checkFlags()
