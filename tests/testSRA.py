from z80 import Z80 as z
from Libraries import Libraries as Library
from memoria import Memoria as m
#test SRA4
print("\ntest 1\n")

z.B = "B1"
Library.checkFlags()
z.SRA(["B"])
print(getattr(z, "B"))
Library.checkFlags()

print("\ntest 2\n")

Library.checkFlags()
z.SRA(["B"])
print(getattr(z, "B"))
Library.checkFlags()

print("\ntest 3\n")

z.B = "44"
Library.checkFlags()
z.SRA(["B"])
print(getattr(z, "B"))
Library.checkFlags()

print("\ntest 4\n")

z.B = "01"

Library.checkFlags()
z.SRA(["B"])
print(getattr(z, "B"))
Library.checkFlags()

#test SRA8
print("\ntest 1 SRA8\n")

z.H = "28"
z.L = "28"
m.cambiarContenido("88", z.H + z.L)
Library.checkFlags()
z.SRA(["(HL)"])
print(m.obtenerContenido(z.H + z.L))
Library.checkFlags()

print("\ntest 2 SRA8\n")

memoryAddress = "1002"
z.IX = "1000"
m.cambiarContenido("88", memoryAddress)
Library.checkFlags()
z.SRA(["(IX+2h)"])
print(m.obtenerContenido(memoryAddress))
Library.checkFlags()

print("\ntest 3 SRA8\n")
#decir que si no inicializa con cero entonces tendré errores
memoryAddress = "1022"
z.IY = "1020"
m.cambiarContenido("7F", "1022")
Library.checkFlags()
z.SRA(["(IY+2h)"])
print(m.obtenerContenido("1022"))
Library.checkFlags()