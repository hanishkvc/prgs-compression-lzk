#!/usr/bin/python3

import sys
import enum

P = enum.Enum('P', 'START SEARCH')


def dprint(o=None, end='\n'):
	pass


# this compress concept is generic but bcas of bytes|bytearray usage,
# it has restriction that it can process and or store data only in units of bytes
# In turn the values in the input byte stream cann't have a value larger than or equal to diStart.
# And the amount of dictionary elements that can be stored before it overflows is 256-diStart
# For example With a diStart of 128
#     we can store a array of ascii characters directly and
#     there can be 128 dictionary elements (which are nothing but sequences of 7bit values).

def compress_Xin8(l, diStart = 128):
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
				dprint("{}, {}".format(partFound, l[i]))
				lc.append(partFound)
				lc.append(l[i])
				state = P.START
	dprint(d)
	dprint("{}, [{}]".format(len(l), l))
	dprint("{}, [{}]".format(len(lc), lc))
	return [d, l, lc]


def decompress_Xin8(l, diStart = 128):
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
	dprint(d)
	dprint("{}, [{}]".format(len(l), l))
	dprint("{}, [{}]".format(len(ld), ld))
	return [d, l, ld]


def compress_asciistr(l):
	return compress_Xin8(bytes(l,'ascii'), 128)


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
[dc, l, lc] = compress_asciistr(l)
[dd, lc, ld] = decompress_Xin8(lc, 128)
print("{}, [{}]".format(len(l), l))
print("{}, [{}]".format(len(lc), lc))
print("{}, [{}]".format(len(ld), ld))

