#!/usr/bin/python3

import sys
import enum

P = enum.Enum('P', 'START SEARCH')

l = sys.argv[1]

d = dict()
diStart = di = 128
state = P.START
for i in range(len(l)):
	if (state == P.START):
		c = l[i]
		state = P.SEARCH
		partFound = None
	if (state == P.SEARCH):
		c += l[i]
		found = None
		for j in range(diStart, di):
			if d[j] == c:
				partFound = j
				found = j
				break
		if (found == None):
			d[di] = c
			di += 1
			print("{}, {}".format(partFound, l[i]))
			state = P.START

print(d)


