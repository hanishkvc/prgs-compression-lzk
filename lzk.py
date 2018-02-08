#!/usr/bin/python3

import sys
import enum

P = enum.Enum('P', 'START SEARCH')


def compress(l):
	d = dict()
	diStart = di = 128
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
					partFound = l[i-1]
					partFound = c[0]
				print("{}, {}".format(partFound, l[i]))
				state = P.START
	print(d)



l = sys.argv[1]
compress(bytes(l,'utf-8'))

