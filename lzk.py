#!/usr/bin/python3

import sys
import enum

P = enum.Enum('P', 'START SEARCH')


def compress(l, diStart = 256):
	lc = bytearray()
	d = dict()
	di = diStart
	state = P.START
	for i in range(len(l)):
		if (state == P.START):
			c = bytearray()
			c.append(l[i])
			state = P.SEARCH
			partFound = None
		elif (state == P.SEARCH):
			c.append(l[i])
			found = None
			for j in range(diStart, di):
				if d[j] == c:
					partFound = j
					found = j
					break
			if (found == None):
				d[di] = c
				di += 1
				if partFound == None:
					#partFound = l[i-1]
					partFound = c[0]
				print("{}, {}".format(partFound, l[i]))
				lc.append(partFound)
				lc.append(l[i])
				state = P.START
	print(d)
	print("{}, [{}]".format(len(l), l))
	print("{}, [{}]".format(len(lc), lc))
	return [d, l, lc]

def compress_str(l, diStart=128):
	return compress(bytes(l,'ascii'), diStart)



def decompress(dOrig, l, diStart=256):
	ld = bytearray()
	d = dict()
	di = diStart
	c = bytearray()
	for i in range(len(l)):
		if l[i] < diStart:
			print(chr(l[i]), end='')
			c.append(l[i])
		else:
			d[di] = c
			di += 1
			print(dOrig[l[i]], end='')

	print()
	print(d)

l = sys.argv[1]
[d, l, lc] = compress_str(l)
decompress(d, lc, 128)

