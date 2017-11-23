#from z80 import Z80
import funciones

c = 10
a = 5

while (a != 10):
	print(c, a)
	c -= 1
	a += 1
	if c == 0:
		break