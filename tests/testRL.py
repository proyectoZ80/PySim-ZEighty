from z80 import Z80 as z
from Libraries import Libraries as Library
from memoria import Memoria as m
#test RL4
print("\ntest 1\n")

z.B = "88"
z.changeFlag(0, "0")
Library.checkFlags()
z.RL(["B"])
print(getattr(z, "B"))
Library.checkFlags()

print("\ntest 2\n")
z.C = "FE"
z.changeFlag(0, "0")
Library.checkFlags()
z.RL(["C"])
print(getattr(z, "C"))
Library.checkFlags()

print("\ntest3\n")
z.C = "00"
#cambiando la bandera N
z.changeFlag(1, "1")
#cambiando la bandera H
z.changeFlag(4, "1")
Library.checkFlags()
z.RL(["C"])
print(getattr(z, "C"))
Library.checkFlags()

##test getDisplacement
#
#print("\ntest1\n")
#print(Instrucciones.getDisplacement("(IX+88h)"))
#
##test RL8
print("\ntest 1 RL8\n")

z.H = "28"
z.L = "28"
m.cambiarContenido("88", z.H + z.L)
Library.checkFlags()
z.RL(["(HL)"])
print(m.obtenerContenido(z.H + z.L))
Library.checkFlags()

print("\ntest 2 RL8\n")

memoryAddress = "1002"
z.IX = "1000"
m.cambiarContenido("88", memoryAddress)
Library.checkFlags()
z.RL(["(IX+2h)"])
print(m.obtenerContenido(memoryAddress))
Library.checkFlags()

print("\ntest 3 RL8\n")
#decir que si no inicializa con cero entonces tendré errores
memoryAddress = "1022"
z.IY = "1020"
m.cambiarContenido("7F", "1022")
Library.checkFlags()
z.RL(["(IY+2h)"])
print(m.obtenerContenido("1022"))
Library.checkFlags()
