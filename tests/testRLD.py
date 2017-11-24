from z80 import Z80 as z
from Libraries import Libraries as Library
from memoria import Memoria as m
#test RLD
print("\ntest 1 RLD\n")

z.H = "28"
z.L = "28"
z.A = "7A"
m.cambiarContenido("31", z.H + z.L)
Library.checkFlags()
z.RLD()
print(m.obtenerContenido(z.H + z.L))
print(z.A)
Library.checkFlags()
