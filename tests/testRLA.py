from z80 import Z80 as z
from Libraries import Libraries as Library
#test RLA
print("\nprueba1\n")
z.A = "88"
z.RLA()
print(z.A)
Library.checkFlags()

print("\nprueba2\n")
z.A = "FE"
z.RLA()
print(z.A)
print(z.F)
Library.checkFlags()

print("\nprueba3\n")
z.A = "7F"
z.RLA()
print(z.A)
print(z.F)
Library.checkFlags()