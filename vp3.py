from struct import unpack, pack

class vp3():
	def __init__(self):

		self.header = {"unknown1":2, "unknown2":0}
		self.colors = []
		self.binfor = { -2:">h", -1:">b", 1: ">B", 2:">H", 4:">I", 8:">Q"}
		self.offset = 0
		self.headeroff = 0

	def bini(self, typ, data, offset=None):
		if offset == None:
			offset = self.offset
		length = abs(typ)
		out = unpack(self.binfor[typ], data[offset:offset+length])[0]
		#print "bin", length ,hex(offset), hex(offset-self.headeroff), data[offset:offset+length], out
		self.offset = offset + length
		return out

	def stri(self, data, offset=None):
		if offset == None:
			offset = self.offset
		strlen = self.bini(2, data, offset=offset)
		offset = self.offset
		out =  data[offset:offset+strlen]
		#print "str", strlen ,hex(offset), hex(offset-self.headeroff), out
		self.offset = offset + strlen
		return out
	
	def parse(self, data):
		if data[0:6] != "%vsm%\x00":
			raise Exception("Not an VP3 File")

		print " == Header =="
		#File Header Information
		self.header["info"] = self.stri(data,offset=6)
		self.headeroff = self.offset
		self.header["unknown1"] = self.bini(2, data)#, offset=8+strlen)
		self.header["unknown2"] = self.bini(1, data)
		self.header["outer size"] = self.bini(4, data)  # <- bytes remaining brak builder 
		self.header["comment"] = self.stri(data)

		print "info: ", self.header["info"]
		print "comment: ", self.header["comment"]

		#Hoop Configuration
		self.header["+xImage"] = self.bini(4, data)#, offset=self.offset+strlen)
		self.header["+yImage"] = self.bini(4, data)
		self.header["-xImage"] = self.bini(4, data)
		self.header["-yImage"] = self.bini(4, data)
		self.header["unknown3"] = self.bini(4, data)
		self.header["unknown4"] = self.bini(4, data)
		self.header["unknown5"] = self.bini(4, data)
		self.bini(4, data) # <- bytes remaining brak builder
		self.header["xOffset"] = self.bini(4, data)
		self.header["yOffset"] = self.bini(4, data)
		self.header["unknown6"] = self.bini(1, data)
		self.header["unknown7"] = self.bini(1, data)
		self.header["unknown8"] = self.bini(1, data)
		self.header["+xCenter"] = self.bini(4, data)
		self.header["+yCenter"] = self.bini(4, data)
		self.header["-xCenter"] = self.bini(4, data)
		self.header["-yCenter"] = self.bini(4, data)
		self.header["width"] = self.bini(4, data)
		self.header["height"] = self.bini(4, data)
		self.header["str"] = self.stri(data)

		self.header["unknown9"] = self.bini(2, data)
		self.header["unknown10"] = self.bini(4, data)
		self.header["unknown11"] = self.bini(4, data)
		self.header["unknown12"] = self.bini(4, data)
		self.header["unknown13"] = self.bini(4, data)
		self.headeroff = self.offset

		#Stitch Section Header 
		if data[self.offset:self.offset+6] != "xxPP\x01\x00":
			raise Exception("Stitch Section Header not found")
		self.header["str2"] = self.stri(data, offset=self.offset+6)
		self.header["numColor"] = self.bini(2, data)

		#Color Section
		for i in range(self.header["numColor"]):
			if i >= 1:
				self.bini(1, data)
			print " == Color =="
			color = {}
			color["unknown1"] = self.bini(2, data)
			color["unknown2"] = self.bini(1, data)
			color["nextcolor"] = self.bini(4, data) + self.offset + 2 # <- brack builder
			color["xOffset"] = self.bini(4, data)
			color["yOffset"] = self.bini(4, data)
			tableSize = self.bini(1, data)
			print tableSize
			color["bColor"] = self.bini(1, data)
			color["rColor"] = self.bini(1, data)
			color["gColor"] = self.bini(1, data)
			color["bColor"] = self.bini(1, data)
			print color["rColor"],  color["gColor"], color["bColor"]
			color["table"] = data[self.offset:self.offset+(6*tableSize)]
			self.offset = self.offset+(6*tableSize)-1
			color["str1"] = self.stri(data)
			color["str2"] = self.stri(data)
			color["str3"] = self.stri(data)
			color["UxOffset"] = self.bini(4, data)
			color["UyOffset"] = self.bini(4, data)
			color["str4"] = self.stri(data)
			print color["str1"], color["str2"], color["str3"]
			stitchBytes = self.bini(4, data)
			color["unknown3"] = self.bini(2, data)
			color["unknown4"] = self.bini(1, data)
			count = 0
			stitches = []
			while count < (stitchBytes-3):
				x = self.bini(-1, data)
				y = self.bini(-1, data)
				count += 2
				if x == 0x80: #special stitch
					if (y == 0) or (y == 3):
						continue
					elif y == 1:
						x = self.bini(-2, data)
						y = self.bini(-2, data)
						if self.bini(-2, data) != 0x8002:
							raise Exception("Special stitch not match")
						count += 6
					else:
						raise Exception("Unknown stitch")
				stitches.append((x,y))
			color["stitches"] = stitches
			self.colors.append(color)

	
	def open(self, path):
		self.parse(open(path).read())

	def build(self):
		pass

	def save(self, path):
		pass
