#!/usr/bin/env python2

from vp3 import vp3
import sys

if len(sys.argv) != 3:
	sys.exit("Usage: %s <file.vp3> <output.svg>" % sys.argv[0])


a = vp3()
a.open(sys.argv[1])

svg = open(sys.argv[2],"w+")
out = ""
maxX, maxY = (0,0)
for i in a.colors:
	out += '  <polyline points="'
	x, y = ( 0, 0)
	out += str(x)+","+str(y)+" "
	for dx,dy in i["stitches"]:
		x += dx
		y += dy
		if y>maxY:
			maxY = y
		if x>maxX:
			maxX = x
		out += str(x)+","+str(y)+" "
	
	out +='"\n  style="fill:none;stroke:rgb('+str(i["rColor"])+','+str(i["gColor"])+','+str(i["bColor"])+')" />'

svg.write('<svg height="'+str(maxY)+'" width="'+str(maxX)+'">\n')
svg.write(out)
	
svg.write('\n</svg>')

svg.close()
