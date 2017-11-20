from z80 import Z80

Z80.PUSH('IX')
Z80.POP('DE')

print(getattr(Z80, 'D'))
print(getattr(Z80, 'E'))
