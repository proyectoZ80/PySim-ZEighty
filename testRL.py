from z80 import Z80 as z
from Instrucciones import Instrucciones
from memoria import Memoria as m

#test RL
print("\ntest1\n")

z.B = "8F"
z.changeFlag(0,"0")
Instrucciones.checkFlags()
Instrucciones.RL("B")
print(z.B)
Instrucciones.checkFlags()

print("\ntest2\n")
z.B = "0F"
z.changeFlag(0, "1")
Instrucciones.checkFlags()
Instrucciones.RL("B")
print(z.B)
Instrucciones.checkFlags()

print("\ntest3\n")
z.B = "FF"
z.changeFlag(0, "0")
Instrucciones.checkFlags()
Instrucciones.RL("B")
print(z.B)
Instrucciones.checkFlags()

print("\ntest4\n")
z.B = "00"
z.changeFlag(0, "0")
Instrucciones.checkFlags()
Instrucciones.RL("B")
print(z.B)
Instrucciones.checkFlags()

print("\ntest 5\n")
#decir que si no inicializa con cero entonces tendré errores
memoryAddress = "1002"
z.IX = "1000"
m.cambiarContenido("7F", memoryAddress)
z.changeFlag(0, "1")
Instrucciones.checkFlags()
Instrucciones.RL("(IX+2h)")
print(m.obtenerContenido(memoryAddress))
Instrucciones.checkFlags()

print("\ntest 6 RLC8\n")
#decir que si no inicializa con cero entonces tendré errores
memoryAddress = "1022"
z.IY = "1020"
m.cambiarContenido("7F", memoryAddress)
z.changeFlag(0, "1")
Instrucciones.checkFlags()
Instrucciones.RL("(IY+2h)")
print(m.obtenerContenido(memoryAddress))
Instrucciones.checkFlags()
