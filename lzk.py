#!/usr/bin/python3

import sys
import enum

P = enum.Enum('P', 'START SEARCH')


def dprint(o=None, end='\n'):
	pass


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
	dprint(d)
	dprint("{}, [{}]".format(len(l), l))
	dprint("{}, [{}]".format(len(lc), lc))
	return [d, l, lc]


def decompress(l, diStart = 256):
	ld = bytearray()
	d = dict()
	di = diStart
	state = P.START
	for i in range(len(l)):
		# The dictionary index
		# 0 to diStart-1 entries of the dictionary are implicit and themselves
		if (state == P.START):
			c = bytearray()
			if l[i] < diStart:
				c.append(l[i])
				ld.append(l[i])
			else:
				c.extend(d[l[i]])
				ld.extend(d[l[i]])
			state = P.SEARCH
			partFound = None
		# The next/this char/byte/groupOfBits which made this sequence (dict[dictIndex]+next/this_char/byte/groupOfBits) unique
		# and thus not already in dictionary, so forced this char/byte/groupOfBits to be explicitly here
		elif (state == P.SEARCH):
			c.append(l[i])
			if l[i] < diStart:
				d[di] = c
				di += 1
				ld.append(l[i])
				state = P.START
			else:
				print("DBG:LOGICALERROR:THINKINGERROR_GOOFUP")
				exit()
	print(d)
	dprint("{}, [{}]".format(len(l), l))
	dprint("{}, [{}]".format(len(ld), ld))
	return [d, l, ld]


def compress_asciistr(l, diStart=128):
	return compress(bytes(l,'ascii'), diStart)


def decompress_easy(dOrig, l, diStart=256):
	ld = bytearray()
	d = dict()
	di = diStart
	c = bytearray()
	for i in range(len(l)):
		if l[i] < diStart:
			dprint(chr(l[i]), end='')
			ld.append(l[i])
			c.append(l[i])
		else:
			d[di] = c
			di += 1
			dprint(dOrig[l[i]], end='')
			ld.extend(dOrig[l[i]])
			c = bytearray()
	dprint()
	dprint(d)
	dprint(ld)
	return [d, l, ld]



l = sys.argv[1]
[d, l, lc] = compress_asciistr(l)
[d, lc, ld] = decompress_easy(d, lc, 128)
print("{}, [{}]".format(len(l), l))
print("{}, [{}]".format(len(lc), lc))
print("{}, [{}]".format(len(ld), ld))
[d, lc, ld] = decompress(lc, 128)
print(ld)

