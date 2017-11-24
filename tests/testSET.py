from z80 import Z80 as z
from Libraries import Libraries as Library
from memoria import Memoria as m
#test SET

for i in range(8):
    print("\n"+z.A)
    z.SET([str(i), "A"])
    print(z.A+"\n")

print("\n" + z.A)
z.SET(["7", "A"])
print(z.A + "\n")

for i in range(8):
    print("\n" + z.B)
    z.SET([str(i), "B"])
    print(z.B + "\n")

print("\ntest 1 SET8\n")
z.H = "28"
z.L = "28"
memoryAddress = "2828"
m.cambiarContenido("00", z.H + z.L)
Library.checkFlags()

for i in range(8):
    #print("\n" + m.obtenerContenido(memoryAddress))
    z.SET([str(i), "(HL)"])
    #print(m.obtenerContenido(memoryAddress) + "\n")
print(m.obtenerContenido(memoryAddress))

print("\ntest 2 SET8\n")

memoryAddress = "1002"
z.IX = "1000"
m.cambiarContenido("00", memoryAddress)
Library.checkFlags()

for i in range(8):
    #print("\n" + m.obtenerContenido(memoryAddress))
    z.SET([str(i), "(IX+2h)"])
    #print(m.obtenerContenido(memoryAddress) + "\n")
print(m.obtenerContenido(memoryAddress))

print("\ntest 3 SET8\n")
#decir que si no inicializa con cero entonces tendré errores
memoryAddress = "1022"
z.IY = "1020"
m.cambiarContenido("00", "1022")
for i in range(8):
    #print("\n" + m.obtenerContenido(memoryAddress))
    z.SET([str(i), "(IY+2h)"])
    #print(m.obtenerContenido(memoryAddress) + "\n")
print(m.obtenerContenido(memoryAddress))

for i in range(8):
    print("\n"+z.A)
    z.SET([str(i), "A"])
    print(z.A+"\n")

print("\n" + z.A)
z.SET(["7", "A"])
print(z.A + "\n")

for i in range(8):
    print("\n" + z.B)
    z.SET([str(i), "B"])
    print(z.B + "\n")

print("\ntest 1 RES8\n")
z.H = "28"
z.L = "28"
memoryAddress = "2828"
m.cambiarContenido("00", z.H + z.L)
Library.checkFlags()

for i in range(8):
    #print("\n" + m.obtenerContenido(memoryAddress))
    z.SET([str(i), "(HL)"])
    #print(m.obtenerContenido(memoryAddress) + "\n")
print(m.obtenerContenido(memoryAddress))

print("\ntest 2 RES8\n")

memoryAddress = "1002"
z.IX = "1000"
m.cambiarContenido("00", memoryAddress)
Library.checkFlags()

for i in range(8):
    #print("\n" + m.obtenerContenido(memoryAddress))
    z.SET([str(i), "(IX+2h)"])
    #print(m.obtenerContenido(memoryAddress) + "\n")
print(m.obtenerContenido(memoryAddress))

print("\ntest 3 RES8\n")
#decir que si no inicializa con cero entonces tendré errores
memoryAddress = "1022"
z.IY = "1020"
m.cambiarContenido("00", "1022")
for i in range(8):
    #print("\n" + m.obtenerContenido(memoryAddress))
    z.SET([str(i), "(IY+2h)"])
    #print(m.obtenerContenido(memoryAddress) + "\n")
print(m.obtenerContenido(memoryAddress))


####################################tests RES
for i in range(8):
    print("\n" + z.A)
    z.RES([str(i), "A"])
    print(z.A + "\n")

print("\n" + z.A)
z.RES(["7", "A"])
print(z.A + "\n")

for i in range(8):
    print("\n" + z.B)
    z.RES([str(i), "B"])
    print(z.B + "\n")

print("\ntest 1 BIT8\n")
z.H = "28"
z.L = "28"
memoryAddress = "2828"
m.cambiarContenido("00", z.H + z.L)
Library.checkFlags()

for i in range(8):
    #print("\n" + m.obtenerContenido(memoryAddress))
    z.RES([str(i), "(HL)"])
    #print(m.obtenerContenido(memoryAddress) + "\n")
print(m.obtenerContenido(memoryAddress))

print("\ntest 2 BIT8\n")

memoryAddress = "1002"
z.IX = "1000"
m.cambiarContenido("00", memoryAddress)
Library.checkFlags()

for i in range(8):
    #print("\n" + m.obtenerContenido(memoryAddress))
    z.RES([str(i), "(IX+2h)"])
    #print(m.obtenerContenido(memoryAddress) + "\n")
print(m.obtenerContenido(memoryAddress))

print("\ntest 3 BIT8\n")
#decir que si no inicializa con cero entonces tendré errores
memoryAddress = "1022"
z.IY = "1020"
m.cambiarContenido("00", "1022")
for i in range(8):
    #print("\n" + m.obtenerContenido(memoryAddress))
    z.RES([str(i), "(IY+2h)"])
    #print(m.obtenerContenido(memoryAddress) + "\n")
print(m.obtenerContenido(memoryAddress))
