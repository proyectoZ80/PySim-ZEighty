from z80 import Z80 as z
from Libraries import Libraries as Library
#test RRA
print("\nprueba1\n")
z.A = "88"
z.RRA()
print(z.A)
Library.checkFlags()

print("\nprueba2\n")
z.A = "FE"
z.RRA()
print(z.A)
print(z.F)
Library.checkFlags()

print("\nprueba3\n")
z.A = "7F"
z.RRA()
print(z.A)
print(z.F)
Library.checkFlags()
