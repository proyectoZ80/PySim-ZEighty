from z80 import Z80 as z
from Libraries import Libraries as Library
#test RLCA
print("\nprueba1\n")
z.A = "88"
z.RLCA()
print(z.A)
Library.checkFlags()

print("\nprueba2\n")
z.A = "FE"
z.RLCA()
print(z.A)
print(z.F)
Library.checkFlags()

print("\nprueba3\n")
z.A = "7F"
z.RLCA()
print(z.A)
print(z.F)
Library.checkFlags()
