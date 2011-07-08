pVerticies = "8;22;(91,111);(0,266);(162,429);(283,495);(401,559);(619,689);(679,567);(876,165);(853,564);(1051,531);(1188,508);(1341,579);(1471,519);(1589,465);(1827,491);(1807,303);(1795,184);(1752,0);(1579,15);(1447,3);(1327,63);(1267,123)".split(';')

nVerticiesSize = pVerticies.pop(0)
nVerticies = int(pVerticies.pop(0))

pSegmentInfo = "2;21;16384;45824;8193;45824;8193;45824;8193;45824;8193;45824;8193;45824;8193;45824;1;45824;1;45824;1;45824;32768".split(';')

nSegmentInfoSize = pSegmentInfo.pop(0)
nSegmentInfo = int(pSegmentInfo.pop(0))

while nSegmentInfo > 0:
	nSeg = int(pSegmentInfo.pop(0))
	if nSeg == 0x0001: # lineto
		nX, nY = pVerticies.pop(0).strip('()').split(',')
		print "line to: x = %s, y = %s" % (nX, nY)
	elif nSeg == 0x4000: # moveto
		nX, nY = pVerticies.pop(0).strip('()').split(',')
		print "move to: x = %s, y = %s" % (nX, nY)
	elif nSeg == 0x2001: # curveto
		ret = []
		for i in range(3):
			nX, nY = pVerticies.pop(0).strip('()').split(',')
			ret.append("x = %s, y = %s" % (nX, nY))
		print "curve to: %s" % "; ".join(ret)
	elif nSeg == 0xb300:
		print "arcto"
		pass
	elif nSeg == 0xac00:
		pass
	elif nSeg == 0xaa00:
		pass
	elif nSeg == 0xab00:
		pass
	elif nSeg == 0x6001:
		pass
	elif nSeg == 0x8000:
		pass
	else:
		print "unhandled segment '%x' in the path" % nSeg
	nSegmentInfo -= 1
print "endsubpath"
